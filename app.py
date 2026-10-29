"""Web page for analysing invention disclosures: drop a file to run the agents, read the reports,
and chat with an assistant about them.

Start it with:  .venv/bin/python app.py   then open http://127.0.0.1:8000
Like run.py, it only runs on your Claude subscription login.
"""

import asyncio
import json
import re
from pathlib import Path

import uvicorn
from claude_agent_sdk import AssistantMessage, ResultMessage, StreamEvent, ToolResultBlock, ToolUseBlock, UserMessage, query
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, PlainTextResponse, StreamingResponse
from pydantic import BaseModel

from run import AGENTS_DIR, OUTPUT_DIR, ROOT, TOOLS, agent_options, check_subscription, start_run

DISCLOSURES_DIR = ROOT / "disclosures"
FILE_TYPES = {".pdf", ".md", ".txt", ".png", ".jpg", ".jpeg", ".gif", ".webp"}  # what the agents can read

CHAT_PROMPT = """You help an innovation advisor at Aalto Innovation work with the results of one analysis run.

The run's folder is {folder}. It holds one Markdown report per agent, and run_info.txt, which lists the input files.

- Answer questions from the reports and input files. Read them when you need them; never guess what they say.
- When asked to change a report, edit the file in the run folder, then say in one or two sentences what you changed. \
You can only edit files in this folder.
- When asked to check something, verify it with web search or the data tools and say what you found, with links. \
Point out anything in the reports that looks wrong.
- Keep answers short and in plain language.

The invention disclosure is confidential and unpublished. When searching the web or using data tools, use general \
terms and never paste distinctive details of the invention."""

app = FastAPI()
sessions = {}  # run id -> chat session id, so each run keeps its own conversation until the server stops
analyses = set()  # running analyses, kept here so Python does not drop them before they finish


class ChatRequest(BaseModel):
    run: str
    message: str
    viewing: str | None = None  # the report open on screen


def run_folder(run):
    folder = (OUTPUT_DIR / run).resolve()
    if folder.parent != OUTPUT_DIR.resolve() or not folder.is_dir():
        raise HTTPException(404, "No such run")
    return folder


@app.get("/")
def page():
    return FileResponse(ROOT / "ui.html")


@app.get("/api/runs")
def runs():
    """All runs, newest first, with their report names and run_info.txt."""
    found = []
    for folder in sorted((f for f in OUTPUT_DIR.iterdir() if f.is_dir()), reverse=True):
        info = folder / "run_info.txt"
        found.append({
            "id": folder.name,
            "reports": sorted(p.stem for p in folder.glob("*.md")),
            "info": info.read_text() if info.exists() else "",
        })
    return found


@app.post("/api/runs")
async def new_run(request: Request, name: str):
    """Save an uploaded disclosure in disclosures/ and start all agents on it in the background."""
    filename = re.sub(r"[^\w.-]", "_", Path(name).name)
    suffix = Path(filename).suffix.lower()
    if suffix not in FILE_TYPES:
        raise HTTPException(400, "Use a PDF, text, Markdown or image file. Save Word files as PDF first.")
    data = await request.body()
    if not data:
        raise HTTPException(400, "The file is empty.")
    try:
        check_subscription()
    except RuntimeError as error:
        raise HTTPException(503, str(error))
    path, n = DISCLOSURES_DIR / filename, 2
    while path.exists() and path.read_bytes() != data:  # never overwrite a different file with the same name
        path, n = DISCLOSURES_DIR / f"{Path(filename).stem}-{n}{suffix}", n + 1
    path.write_bytes(data)
    out_dir, work = start_run([str(path)], sorted(p.stem for p in AGENTS_DIR.glob("*.md")))
    task = asyncio.create_task(work)
    analyses.add(task)
    task.add_done_callback(analyses.discard)
    return {"id": out_dir.name}


@app.get("/api/runs/{run}/{name}", response_class=PlainTextResponse)
def report(run: str, name: str):
    path = run_folder(run) / f"{name}.md"
    if path.parent != run_folder(run) or not path.exists():
        raise HTTPException(404, "No such report")
    return path.read_text()


@app.post("/api/chat/{run}/reset")
def reset(run: str):
    sessions.pop(run, None)


@app.post("/api/chat")
async def chat(request: ChatRequest):
    folder = run_folder(request.run)
    check_subscription()
    options = agent_options(
        CHAT_PROMPT.format(folder=folder),
        ["Edit", "Write", "WebSearch", "WebFetch", *TOOLS],
        allowed=["Read", "WebSearch", "WebFetch", f"Edit(./outputs/{request.run}/**)"],  # edits only inside this run
        resume=sessions.get(request.run),
        include_partial_messages=True,  # stream the reply word by word
    )
    prompt = f"[Report open on my screen: {request.viewing}.md]\n\n{request.message}" if request.viewing else request.message

    def event(**fields):
        return json.dumps(fields) + "\n"

    async def stream():
        try:
            async for message in query(prompt=prompt, options=options):
                if isinstance(message, StreamEvent) and message.event.get("delta", {}).get("type") == "text_delta":
                    yield event(type="text", text=message.event["delta"]["text"])
                elif isinstance(message, AssistantMessage):
                    for block in message.content:
                        if isinstance(block, ToolUseBlock):
                            detail = next((v for v in block.input.values() if isinstance(v, str)), "")
                            detail = Path(detail).name if detail.startswith("/") else detail[:80]
                            yield event(type="tool", id=block.id, name=block.name.replace("mcp__data__", ""), detail=detail)
                elif isinstance(message, UserMessage) and isinstance(message.content, list):
                    for block in message.content:
                        if isinstance(block, ToolResultBlock) and block.is_error:
                            yield event(type="tool_failed", id=block.tool_use_id)
                elif isinstance(message, ResultMessage):
                    sessions[request.run] = message.session_id
        except Exception as error:
            sessions.pop(request.run, None)  # start a fresh conversation next time
            yield event(type="error", text=str(error))

    return StreamingResponse(stream(), media_type="application/x-ndjson")


if __name__ == "__main__":
    check_subscription()
    print("Open http://127.0.0.1:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000)
