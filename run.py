"""Run specialist Claude agents on invention disclosures, using your Claude subscription only.

Before any agent runs, the script checks that Claude Code is signed in with your claude.ai
subscription and stops otherwise, so it never uses an API key, token or cloud account billed per token.

Each file in agents/ is one agent. Each run gets its own folder, outputs/<date>_<time>_<first file name>/,
with one report per agent and a run_info.txt listing the inputs and how each agent is doing.

Usage:
    python run.py disclosures/example.md                  # all agents
    python run.py disclosures/example.md -a market nabc   # chosen agents
    python run.py disclosure.pdf extra_data.csv           # extra input files
"""

import argparse
import asyncio
import functools
import json
import os
import re
import shutil
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

import claude_agent_sdk
from claude_agent_sdk import ClaudeAgentOptions, ResultMessage, create_sdk_mcp_server, query

from tools import TOOLS

# Each of these would make Claude Code bill per token or send requests somewhere other than Anthropic.
for var in ("ANTHROPIC_API_KEY", "ANTHROPIC_AUTH_TOKEN", "ANTHROPIC_BASE_URL"):
    os.environ.pop(var, None)

# The Claude Code program the agents run on. The subscription check runs this same program.
BUNDLED_CLI = Path(claude_agent_sdk.__file__).parent / "_bundled" / "claude"
CLI = str(BUNDLED_CLI) if BUNDLED_CLI.exists() else shutil.which("claude")

ROOT = Path(__file__).parent
AGENTS_DIR = ROOT / "agents"
OUTPUT_DIR = ROOT / "outputs"
DISCLOSURES_DIR = ROOT / "disclosures"
FILE_TYPES = {".pdf", ".md", ".txt", ".png", ".jpg", ".jpeg", ".gif", ".webp"}  # what the agents can read

TASK = """Input files (read them all first):
{files}

Our own data, kept on this computer: stored_patents finds the patents in our database closest to a description, \
stored_companies looks up the companies and patent applicants we track, and library/<sector>/memory.md holds our \
latest research on each sector ({sectors}). Use what fits alongside your online searches, and say which findings \
come from our own data.

The invention disclosure is confidential and unpublished. When searching the web or using online data tools, use \
general terms (field, product type, company names) and never paste distinctive details of the invention. \
stored_patents and stored_companies run on this computer, so they may be given the full description.

Return the whole finished report in the report field. Only that field is saved, so do not write the report \
elsewhere and point to it."""

FIVE = {"type": "integer", "enum": [1, 2, 3, 4, 5]}
PARTS = ["market", "ip", "funding", "nabc"]  # shown as Market, Patents, Funding and Summary
SCHEMAS = {  # what an agent returns, chosen with 'output:' in its header
    "report": {"type": "object", "properties": {
        "report": {"type": "string", "description": "The complete report in Markdown, with every section and link. "
                   "Only this field is saved: text written outside it is lost, so never refer to it."},
        "score": FIVE, "reason": {"type": "string", "description": "One sentence: why this score"}},
        "required": ["report", "score", "reason"], "additionalProperties": False},
    "check": {"type": "object", "properties": {
        "title": {"type": "string", "description": "The invention's name in a few words"},
        "summary": {"type": "string", "description": "Two or three sentences: the overall picture and how far to trust the reports"},
        "parts": {"type": "array", "items": {"type": "object", "properties": {
            "part": {"type": "string", "enum": PARTS}, "agrees": {"type": "boolean"}, "score": FIVE,
            "note": {"type": "string"}}, "required": ["part", "agrees", "score", "note"], "additionalProperties": False}},
        "issues": {"type": "array", "items": {"type": "object", "properties": {
            "part": {"type": "string", "enum": PARTS}, "claim": {"type": "string"}, "problem": {"type": "string"},
            "link": {"type": "string"}}, "required": ["part", "claim", "problem", "link"], "additionalProperties": False}}},
        "required": ["title", "summary", "parts", "issues"], "additionalProperties": False},
}


@functools.cache
def check_subscription():
    """Raise unless Claude Code is signed in with the claude.ai subscription (anything else could bill per token)."""
    status = subprocess.run([CLI, "auth", "status"], capture_output=True, text=True).stdout
    method = json.loads(status or "{}").get("authMethod")
    if method != "claude.ai":
        raise RuntimeError(
            f"Claude Code is not using your Claude subscription (auth method: {method}). "
            "Sign in with: claude auth login"
        )


MODEL = "claude-sonnet-5-5"  # every agent uses this unless its file names another model: it uses less of the allowance


def agent_options(system_prompt, tool_names, allowed=None, **extra):
    """Options for one agent: Read plus the named tools and nothing else.

    tool_names mixes Claude Code's own tools (e.g. WebSearch) and data tools from tools.py.
    allowed replaces the list of Claude Code tools that run without asking (default: all of them).
    """
    built_in = ["Read"] + [n for n in tool_names if n not in TOOLS]
    data_tools = [TOOLS[n] for n in tool_names if n in TOOLS]
    extra["model"] = extra.get("model") or MODEL
    return ClaudeAgentOptions(
        system_prompt=system_prompt,
        tools=built_in,
        mcp_servers={"data": create_sdk_mcp_server("data", tools=data_tools)} if data_tools else {},
        allowed_tools=(allowed or built_in) + [f"mcp__data__{t.name}" for t in data_tools],
        env={"ENABLE_TOOL_SEARCH": "false"},  # few tools, so show them all to the agent up front
        permission_mode="dontAsk",  # deny anything not allowed instead of waiting for approval
        setting_sources=[],  # ignore ~/.claude settings, memory and plugins
        strict_mcp_config=True,
        cwd=ROOT,
        cli_path=CLI,
        **extra,
    )


def read_agent(name):
    """Read agents/<name>.md: an optional 'key: value' header between --- lines, then the system prompt."""
    text = (AGENTS_DIR / f"{name}.md").read_text()
    config = {}
    if text.startswith("---"):
        header, text = text[3:].split("---", 1)
        for line in header.strip().splitlines():
            key, value = line.split(":", 1)
            config[key.strip()] = value.strip()
    return config, text.strip()


def load_agent(name):
    config, prompt = read_agent(name)
    names = [t.strip() for t in config.get("tools", "").split(",") if t.strip()]
    schema = SCHEMAS[config.get("output", "report")]
    return agent_options(prompt, names, model=config.get("model"), effort=config.get("effort"),
                         output_format={"type": "json_schema", "schema": schema})


async def run_agent(name, files):
    """Run one agent on the input files and return what it found, in the shape of its schema."""
    check_subscription()
    sectors = ", ".join(s["id"] for s in json.loads((ROOT / "sectors.json").read_text()))
    prompt = TASK.format(files="\n".join(f"- {Path(f).resolve()}" for f in files), sectors=sectors)
    result = None
    async for message in query(prompt=prompt, options=load_agent(name)):
        if isinstance(message, ResultMessage):
            result = message
    if result is None or result.is_error or not result.structured_output:
        raise RuntimeError(result.errors or result.result if result else "no result")
    return result.structured_output


def save_disclosure(name, data):
    """Save an uploaded disclosure in disclosures/, never over a different file with the same name, and return its path."""
    filename = re.sub(r"[^\w.-]", "_", Path(name).name)
    suffix = Path(filename).suffix.lower()
    if suffix not in FILE_TYPES:
        raise ValueError("Use a PDF, text, Markdown or image file. Save Word files as PDF first.")
    if not data:
        raise ValueError("The file is empty.")
    path, n = DISCLOSURES_DIR / filename, 2
    while path.exists() and path.read_bytes() != data:
        path, n = DISCLOSURES_DIR / f"{Path(filename).stem}-{n}{suffix}", n + 1
    path.write_bytes(data)
    return path


def start_run(files, agents):
    """Create the run folder and return it with the coroutine that runs the agents.

    Each report agent saves <name>.md, and its 1 to 5 score goes into scores.json. Agents with 'after: reports' in
    their header (the checker) wait until the others are done and also get their reports and scores; they save <name>.json.
    run_info.txt is rewritten whenever an agent starts or finishes, so it always shows the current progress.
    """
    started = datetime.now()
    out_dir = OUTPUT_DIR / f"{started:%Y-%m-%d_%H-%M-%S}_{Path(files[0]).stem}"
    out_dir.mkdir(parents=True)
    later = [a for a in agents if read_agent(a)[0].get("after") == "reports"]
    first = [a for a in agents if a not in later]
    status = {a: f"[{a}] {'waiting' if a in later else 'running'}" for a in agents}
    scores = {}
    inputs = "\n".join(f"  {Path(f).resolve()}" for f in files)

    def save_status():
        (out_dir / "run_info.txt").write_text(
            f"Started: {started:%Y-%m-%d %H:%M:%S}\nInputs:\n{inputs}\n\n" + "\n".join(status.values()) + "\n"
        )

    async def run_and_save(name, agent_files):
        status[name] = f"[{name}] running"
        save_status()
        start = time.monotonic()
        try:
            found = await run_agent(name, agent_files)
            if "report" in found:
                (out_dir / f"{name}.md").write_text(found["report"])
                scores[name] = {"score": found["score"], "reason": found["reason"]}
                (out_dir / "scores.json").write_text(json.dumps(scores, indent=2, ensure_ascii=False))
                result = f"saved {name}.md"
            else:
                (out_dir / f"{name}.json").write_text(json.dumps(found, indent=2, ensure_ascii=False))
                result = f"saved {name}.json"
        except Exception as error:
            result = f"failed: {error}"
        status[name] = f"[{name}] {result} ({time.monotonic() - start:.0f} s)"
        print(status[name])
        save_status()

    async def run_all():
        await asyncio.gather(*(run_and_save(a, files) for a in first))
        reports = [str(p) for p in [*(out_dir / f"{a}.md" for a in first), out_dir / "scores.json"] if p.exists()]
        await asyncio.gather(*(run_and_save(a, files + reports) for a in later))

    save_status()
    return out_dir, run_all()


async def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("files", nargs="+", help="the disclosure first, then any extra data files")
    parser.add_argument("-a", "--agents", nargs="+", default=sorted(p.stem for p in AGENTS_DIR.glob("*.md")))
    args = parser.parse_args()
    try:
        check_subscription()
    except RuntimeError as error:
        sys.exit(f"Stopped before running any agent: {error}")

    out_dir, work = start_run(args.files, args.agents)
    print(f"Running {', '.join(args.agents)} on {', '.join(args.files)}\nSaving to {out_dir.relative_to(ROOT)}/")
    await work


if __name__ == "__main__":
    asyncio.run(main())
