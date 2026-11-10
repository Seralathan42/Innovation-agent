"""Market terminal: a dashboard of the sector library, with a chat that answers from it and can add sectors.

Start it with:  .venv/bin/python terminal.py   then open http://127.0.0.1:8001
While it runs, it pulls new EPO patents every 6 hours, keeps filling in older ones (5 years back), and refreshes sectors older than 3 days.
"""

import asyncio
import json
import re
import threading
from contextlib import asynccontextmanager

import uvicorn
from claude_agent_sdk import AssistantMessage, ResultMessage, StreamEvent, ToolUseBlock, create_sdk_mcp_server, query, tool
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel

import library
import patents
from run import ROOT, agent_options, check_subscription

CHAT_PROMPT = """You are the assistant in Aalto Innovation's market terminal. You answer questions about market \
sectors and can add new sectors to the library.

The sector library is in ./library: one folder per sector, each with memory.md (the full knowledge file with \
sources), data.json (metrics, signals, funding calls, companies) and the patent database behind the Patents tab (use epo_patents for patent questions). Current sectors: {sectors}.

- Read the relevant library files before answering. Use web search, epo_patents and the other data tools to check \
or add recent facts.
- Always give sources as Markdown links. Keep answers short and plain, and say when the library has no data.
- When someone asks for a new sector dataset, agree on a short name and scope with them if it is unclear, then call \
add_sector. Pick an id (lowercase-with-dashes), a 4-letter code, the closest Aalto research area (Digitalisation and \
AI, Materials, Art and design, Business and economics, Energy solutions, Living environments, Health and well-being) \
and an EPO CQL patent query such as cpc=H01M or ta="vertical farming". Tell them it takes a few minutes to build."""

updating = set()  # sector ids being updated right now


class Message(BaseModel):
    message: str
    session: str | None = None  # continue this conversation
    sector: str | None = None  # the sector open on screen


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


@app.post("/api/companies/search")
def company_search(query: CompanyQuery):
    """Filtered companies (patent applicants and profiled companies) and facet counts for the Companies tab."""
    return patents.company_search(**query.model_dump())


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
    data_tools = ["WebSearch", "WebFetch", "epo_patents", "eurostat_search", "eurostat_data", "finnish_companies",
                  "eu_funding_calls", "research_projects", "search_papers"]
    options = agent_options(CHAT_PROMPT.format(sectors=names), data_tools,
                            allowed=["Read(./library/**)", "WebSearch", "WebFetch"],  # reads only the library
                            resume=message.session, include_partial_messages=True)
    options.mcp_servers["terminal"] = create_sdk_mcp_server("terminal", tools=[add_sector])
    options.allowed_tools.append("mcp__terminal__add_sector")
    prompt = f"[Sector open on screen: {message.sector}]\n\n{message.message}" if message.sector else message.message

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
