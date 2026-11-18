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

TASK = """Input files (read them all first):
{files}

The invention disclosure is confidential and unpublished. When searching the web or using data tools, \
use general terms (field, product type, company names) and never paste distinctive details of the invention.

Reply with your finished report in Markdown as your final message."""


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
    return agent_options(prompt, names, model=config.get("model"), effort=config.get("effort"))


async def run_agent(name, files):
    """Run one agent on the input files and return its final reply."""
    check_subscription()
    prompt = TASK.format(files="\n".join(f"- {Path(f).resolve()}" for f in files))
    result = None
    async for message in query(prompt=prompt, options=load_agent(name)):
        if isinstance(message, ResultMessage):
            result = message
    if result is None or result.is_error:
        raise RuntimeError(result.errors or result.result if result else "no result")
    return result.result


def start_run(files, agents):
    """Create the run folder and return it with the coroutine that runs the agents.

    Agents with 'after: reports' in their header wait until the others are done and also get their reports.
    run_info.txt is rewritten whenever an agent starts or finishes, so it always shows the current progress.
    """
    started = datetime.now()
    out_dir = OUTPUT_DIR / f"{started:%Y-%m-%d_%H-%M-%S}_{Path(files[0]).stem}"
    out_dir.mkdir(parents=True)
    later = [a for a in agents if read_agent(a)[0].get("after") == "reports"]
    first = [a for a in agents if a not in later]
    status = {a: f"[{a}] {'waiting' if a in later else 'running'}" for a in agents}
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
            (out_dir / f"{name}.md").write_text(await run_agent(name, agent_files))
            result = f"saved {name}.md"
        except Exception as error:
            result = f"failed: {error}"
        status[name] = f"[{name}] {result} ({time.monotonic() - start:.0f} s)"
        print(status[name])
        save_status()

    async def run_all():
        await asyncio.gather(*(run_and_save(a, files) for a in first))
        reports = [str(out_dir / f"{a}.md") for a in first if (out_dir / f"{a}.md").exists()]
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
