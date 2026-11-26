"""Market terminal: a dashboard of the sector library, with a chat that answers from it and can add sectors.

Start it with:  .venv/bin/python terminal.py   then open http://127.0.0.1:8001
While it runs, it pulls new EPO patents every 6 hours, keeps filling in older ones (5 years back), and refreshes sectors older than 3 days.
"""

import asyncio
from datetime import date
import json
import re
import threading
from contextlib import asynccontextmanager

import uvicorn
from claude_agent_sdk import AssistantMessage, ResultMessage, StreamEvent, ToolUseBlock, create_sdk_mcp_server, query, tool
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel

import library
import patents
import profiles
import research
from run import OUTPUT_DIR, PARTS, ROOT, agent_options, check_subscription, save_disclosure, start_run

CHAT_PROMPT = """You are the assistant in Aalto Innovation's market terminal. You answer questions about market \
sectors and can add new sectors to the library.

The sector library is in ./library: one folder per sector, each with memory.md (the full knowledge file with \
sources), data.json (metrics, signals, funding calls, companies) and the patent database behind the Patents tab. For patent questions use epo_patents (worldwide search) and epo_patent (one patent's family, grant status, legal events and claims); research_trend shows how active a research topic is. Current sectors: {sectors}.

- Read the relevant library files before answering. Use web search, epo_patents and the other data tools to check \
or add recent facts.
- Always give sources as Markdown links. Keep answers short and plain, and say when the library has no data.
- When someone asks for a new sector dataset, agree on a short name and scope with them if it is unclear, then call \
add_sector. Pick an id (lowercase-with-dashes), a 4-letter code, the closest Aalto research area (Digitalisation and \
AI, Materials, Art and design, Business and economics, Energy solutions, Living environments, Health and well-being) \
and an EPO CQL patent query such as cpc=H01M or ta="vertical farming". Tell them it takes a few minutes to build.
- When an invention brief is open on screen, its folder is named in the message. Read its reports (market.md, ip.md for \
patents, funding.md, nabc.md for the summary), scores.json and check.json (the checker's notes) before answering. \
run_info.txt names the disclosure file, which you may read. The disclosure is confidential: never put its \
distinctive details into web searches or online tools; stored_patents and stored_companies run on this computer.
- The first time you name a company or a person, write the name as a link so it can be clicked for a profile: \
[Nokia](#company/Nokia) or [Antti Laaksonen](#person/Antti%20Laaksonen), with %20 for spaces. Use these links only \
for companies and people, and keep normal source links as they are."""

updating = set()  # sector ids being updated right now
briefing = {}  # run id -> the task making that invention brief (kept so Python does not drop it before it ends)


class Message(BaseModel):
    message: str
    session: str | None = None  # continue this conversation
    sector: str | None = None  # the sector open on screen
    brief: str | None = None  # the invention brief open on screen


async def refresh(sector_id):
    if sector_id in updating:
        return
    updating.add(sector_id)
    try:
        await library.update(sector_id)
        await asyncio.to_thread(patents.build_companies)  # its profiled companies show up in the Companies tab
    except Exception as error:
        print(f"[{sector_id}] update failed: {error}")
    finally:
        updating.discard(sector_id)


async def keep_fresh():  # one sector at a time, so the subscription usage stays spread out
    while True:
        for sector_id in library.stale():
            await refresh(sector_id)
        await asyncio.sleep(3600)


@asynccontextmanager
async def lifespan(app):
    task = asyncio.create_task(keep_fresh())  # sector updates while running
    threading.Thread(target=patents.keep_pulling, daemon=True).start()  # EPO only, no Claude usage; ends with the app
    threading.Thread(target=research.keep_up, daemon=True).start()  # ACRIS papers, screened here; analysed when asked
    profiles.reset()
    yield
    task.cancel()


app = FastAPI(lifespan=lifespan)


@tool("add_sector", "Add a new sector to the library and start building its dataset.", {
    "type": "object",
    "properties": {name: {"type": "string"} for name in ["id", "code", "name", "aalto_area", "scope", "patent_query"]},
    "required": ["id", "code", "name", "aalto_area", "scope", "patent_query"],
})
async def add_sector(args):
    sectors = library.sectors()
    sector_id = re.sub(r"[^a-z0-9-]", "-", args["id"].lower()).strip("-")
    if any(s["id"] == sector_id for s in sectors):
        return {"content": [{"type": "text", "text": f"A sector with the id {sector_id} already exists."}], "is_error": True}
    sectors.append({**args, "id": sector_id, "code": args["code"].upper()[:4]})
    library.SECTORS_FILE.write_text(json.dumps(sectors, indent=2, ensure_ascii=False) + "\n")
    asyncio.create_task(refresh(sector_id))
    return {"content": [{"type": "text", "text": f"Added {args['name']} ({sector_id}). Building its dataset now."}]}


@app.get("/")
def page():
    return FileResponse(ROOT / "terminal.html", headers={"Cache-Control": "no-cache"})  # always show the latest page


@app.get("/api/sectors")
def sectors():
    return [{**s, "data": library.load(s["id"]), "patents": patents.summary(s["id"]), "updating": s["id"] in updating}
            for s in library.sectors()]


class PatentQuery(BaseModel):
    q: str = ""
    include: dict = {}
    exclude: dict = {}
    sort: str = "newest"
    cpc_level: str = "subclass"
    find: dict = {}
    limit: int = 50
    facets: list | None = None  # the facets open on the page; the others are not counted
    part: str = "all"  # "items" or "facets", so the page can show patents before the counts


class Similar(BaseModel):
    text: str


@app.post("/api/patents/similar")
def similar_patents(query: Similar):
    """The stored patents closest to a description. Searched on this computer; the text is not sent anywhere."""
    return patents.similar(query.text)


SUMMARY_PROMPT = """You summarise a technology topic for an innovation advisor at Aalto Innovation, in plain language \
and without em dashes. Write about 200 words in Markdown, with no title or headings (bold lead-ins are fine): what the topic covers and where it is used, what the \
patents below show is being protected and by whom (main applicants and countries), how filing activity has changed \
over the years, and where there may be room for new research or a new company. Base what you say about patents \
only on the list below, and say so if the list looks off-topic. Today is {today}.

Topic as written: {text}

Top applicants among the 100 closest stored patents: {applicants}
First filings per year: {years}
Main CPC classes: {classes}
Closest patents:
{items}"""


@app.post("/api/patents/summary")
async def similar_summary(request: Similar):
    """A short Sonnet summary of the topic written in the Similar tab, based on the closest stored patents."""
    check_subscription()
    found = patents.similar(request.text)
    items = "\n".join(f"- {p['title']} ({p['number']}, first filed {p['priority'] or p['date']}), {', '.join(p['applicants'][:3])}"
                      for p in found["items"][:30])
    prompt = SUMMARY_PROMPT.format(today=date.today(), text=request.text[:2000], items=items or "(none found)",
                                   **{k: ", ".join(f"{v} ({n})" for v, n in found[k]) for k in ("applicants", "years", "classes")})
    result = None
    async for message in query(prompt=prompt, options=agent_options("You write short, plain summaries.", [], disallowed_tools=["Read"])):
        if isinstance(message, ResultMessage):
            result = message
    if result is None or result.is_error:
        raise HTTPException(502, "The summary could not be written. Try again in a moment.")
    return {"summary": result.result}


@app.post("/api/patents/search")
def patent_search(query: PatentQuery):
    """Filtered patents and facet counts for the Patents tab."""
    return patents.search(**query.model_dump())


class CompanyQuery(BaseModel):
    q: str = ""
    include: dict = {}
    exclude: dict = {}
    sort: str = "patents"
    find: dict = {}
    limit: int = 50
    facets: list | None = None


@app.post("/api/companies/search")
def company_search(query: CompanyQuery):
    """Filtered companies (patent applicants and profiled companies) and facet counts for the Companies tab."""
    return patents.company_search(**query.model_dump())


class PaperQuery(BaseModel):
    q: str = ""
    include: dict = {}
    exclude: dict = {}
    sort: str = "promising"
    find: dict = {}
    limit: int = 50
    facets: list | None = None


@app.post("/api/research/search")
def research_search(query: PaperQuery):
    """Filtered Aalto papers and facet counts for the Research tab."""
    return research.search(**query.model_dump())


@app.get("/api/research/{paper_id}")
def research_paper(paper_id: str):
    found = research.paper(paper_id)
    if not found:
        raise HTTPException(404, "No such paper")
    return found


@app.post("/api/research/{paper_id}/analyse")
async def research_analyse(paper_id: str):
    """Start the in-depth check of one paper (Sonnet, a few minutes). The page polls the paper until it is done."""
    found = research.paper(paper_id)
    if not found:
        raise HTTPException(404, "No such paper")
    if not found["analysing"]:
        async def run():
            try:
                await research.analyse(paper_id)
            except Exception as error:
                print(f"[research] {paper_id} failed: {error}")
        asyncio.create_task(run())
    return {"analysing": True}


class ProfileRequest(BaseModel):
    kind: str  # company or person
    name: str
    context: str = ""  # the text around the name, so the agent finds the right one
    update: bool = False


@app.get("/api/profile")
def profile(kind: str, name: str):
    """A stored company or person profile and its status: missing, building, ready or failed."""
    return profiles.get(kind, name)


@app.post("/api/profile")
async def profile_build(request: ProfileRequest):
    """Build a profile when it is clicked for the first time (or on Update). The page polls until it is ready."""
    if request.kind not in profiles.SCHEMAS or not request.name.strip():
        raise HTTPException(400, "Unknown profile")
    found = profiles.get(request.kind, request.name)
    if found["status"] in ("missing", "failed") or (request.update and found["status"] != "building"):
        asyncio.create_task(profiles.build(request.kind, request.name.strip(), request.context[:600]))
        return {"status": "building"}
    return found


def brief_folder(run):
    folder = (OUTPUT_DIR / run).resolve()
    if folder.parent != OUTPUT_DIR.resolve() or not folder.is_dir():
        raise HTTPException(404, "No such brief")
    return folder


def brief(folder, reports=False):
    """One invention brief: its disclosure, each agent's state, the scores and the checker's notes (and the reports)."""
    info = (folder / "run_info.txt").read_text() if (folder / "run_info.txt").exists() else ""
    stopped = folder.name not in briefing  # a run cut off by a restart is not running any more
    status = {a: "stopped" if stopped and s in ("running", "waiting") else s for a, s in re.findall(r"^\[(\w+)\] (\w+)", info, re.M)}
    found = {"id": folder.name, "status": status, "file": (re.search(r"Inputs:\n\s+(.+)", info) or [None, ""])[1].split("/")[-1],
             "started": (re.search(r"Started: (.+)", info) or [None, ""])[1],
             "errors": sorted(set(re.findall(r"^\[\w+\] failed: (.+?)(?: \(\d+ s\))?$", info, re.M)))}
    for name in ("scores", "check"):
        path = folder / f"{name}.json"
        found[name] = json.loads(path.read_text()) if path.exists() else None
    if reports:
        found["reports"] = {a: (folder / f"{a}.md").read_text() for a in PARTS if (folder / f"{a}.md").exists()}
    return found


@app.get("/api/briefs")
def briefs():
    return [brief(f) for f in sorted(OUTPUT_DIR.iterdir(), reverse=True) if f.is_dir()]


@app.get("/api/briefs/{run}")
def brief_view(run: str):
    return brief(brief_folder(run), reports=True)


@app.post("/api/briefs")
async def brief_start(request: Request, name: str):
    """Save a dropped disclosure and start the four research agents and the checker on it in the background."""
    try:
        check_subscription()
        path = save_disclosure(name, await request.body())
    except RuntimeError as error:
        raise HTTPException(503, str(error))
    except ValueError as error:
        raise HTTPException(400, str(error))
    out_dir, work = start_run([str(path)], PARTS + ["check"])
    task = briefing[out_dir.name] = asyncio.create_task(work)
    task.add_done_callback(lambda _: briefing.pop(out_dir.name, None))
    return {"id": out_dir.name}


@app.get("/api/sectors/{sector_id}/memory")
def memory(sector_id: str):
    path = library.LIBRARY / sector_id / "memory.md"
    if sector_id not in {s["id"] for s in library.sectors()} or not path.exists():
        raise HTTPException(404, "No memory for this sector yet")
    return {"memory": path.read_text()}


@app.post("/api/sectors/{sector_id}/refresh")
async def refresh_now(sector_id: str):
    library.sector(sector_id)  # raises for an unknown sector
    asyncio.create_task(refresh(sector_id))
    return {"updating": True}


@app.post("/api/chat")
async def chat(message: Message):
    check_subscription()
    names = ", ".join(f"{s['name']} ({s['id']})" for s in library.sectors())
    data_tools = ["WebSearch", "WebFetch", "epo_patents", "epo_patent", "research_trend", "eurostat_search", "eurostat_data", "finnish_companies",
                  "eu_funding_calls", "research_projects", "search_papers", "stored_patents", "stored_companies"]
    readable = ["Read(./library/**)"]  # reads only the library, and the brief open on screen with its disclosure
    if message.brief:
        folder = brief_folder(message.brief)
        readable += [f"Read(./outputs/{folder.name}/**)", "Read(./disclosures/**)"]
    options = agent_options(CHAT_PROMPT.format(sectors=names), data_tools, allowed=readable + ["WebSearch", "WebFetch"],
                            resume=message.session, include_partial_messages=True)
    options.mcp_servers["terminal"] = create_sdk_mcp_server("terminal", tools=[add_sector])
    options.allowed_tools.append("mcp__terminal__add_sector")
    prompt = f"[Sector open on screen: {message.sector}]\n\n{message.message}" if message.sector else message.message
    if message.brief:
        prompt = f"[Invention brief open on screen: folder outputs/{message.brief}]\n\n{message.message}"

    async def stream():
        try:
            async for event in query(prompt=prompt, options=options):
                if isinstance(event, StreamEvent) and event.event.get("delta", {}).get("type") == "text_delta":
                    yield json.dumps({"text": event.event["delta"]["text"]}) + "\n"
                elif isinstance(event, AssistantMessage):
                    for block in event.content:
                        if isinstance(block, ToolUseBlock):
                            name = block.name.split("__")[-1]
                            detail = next((v for v in block.input.values() if isinstance(v, str)), "")
                            yield json.dumps({"tool": name, "detail": detail.split("/")[-1][:80]}) + "\n"
                elif isinstance(event, ResultMessage):
                    yield json.dumps({"session": event.session_id}) + "\n"
        except Exception as error:
            yield json.dumps({"error": str(error)}) + "\n"

    return StreamingResponse(stream(), media_type="application/x-ndjson")


if __name__ == "__main__":
    check_subscription()
    print("Open http://127.0.0.1:8001")
    uvicorn.run(app, host="127.0.0.1", port=8001)
