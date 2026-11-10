"""Sector library: one memory file per market sector (sectors.json), kept up to date by a research agent.

Each update starts from the sector's previous memory, so knowledge builds up over time instead of being
rewritten from scratch. Only public information is used, so no invention details are involved.

Usage:
    python library.py              # update every sector older than MAX_AGE_DAYS, one at a time
    python library.py energy       # update one sector now
"""

import asyncio
import json
import sys
from datetime import date, datetime
from pathlib import Path

from claude_agent_sdk import ResultMessage, query

from run import ROOT, agent_options, check_subscription

LIBRARY = ROOT / "library"
SECTORS_FILE = ROOT / "sectors.json"
MAX_AGE_DAYS = 3
TOOLS = ["WebSearch", "WebFetch", "eurostat_search", "eurostat_data", "finnish_companies",
         "eu_funding_calls", "eu_call_details", "research_projects", "search_papers", "google_patent", "epo_patents"]

def ITEM(*fields):  # JSON schema for a list of objects with these text fields
    return {"type": "array", "items": {"type": "object", "properties": {f: {"type": "string"} for f in fields},
                                       "required": list(fields), "additionalProperties": False}}


SCHEMA = {
    "type": "object",
    "properties": {
        "headline": {"type": "string"},
        "outlook": {"type": "string", "enum": ["positive", "neutral", "negative"]},
        "outlook_reason": {"type": "string"},
        "metrics": ITEM("label", "value", "year", "source"),
        "signals": ITEM("date", "title", "detail", "impact", "source"),
        "funding_calls": ITEM("id", "title", "deadline", "budget", "link"),
        "companies": ITEM("name", "country", "what", "link"),
        "aalto_links": ITEM("what", "link"),
        "memory": {"type": "string"},
    },
    "required": ["headline", "outlook", "outlook_reason", "metrics", "signals", "funding_calls", "companies",
                 "aalto_links", "memory"],
    "additionalProperties": False,
}

PROMPT = """You are a market analyst for Aalto Innovation, the unit that helps commercialise Aalto University research. \
You keep the knowledge library for one market sector up to date, so advisors can quickly judge the market for \
inventions from Aalto's {aalto_area} research.

Sector: {name}. Scope: {scope}. Today is {today}.

Research the sector with web search and the data tools: Eurostat for official figures, finnish_companies for Finnish \
firms, eu_funding_calls and eu_call_details for open EU calls, research_projects and search_papers for research, and \
epo_patents (European Patent Office search, if available) and google_patent for patents. Focus on Europe and Finland, and on what matters for commercialising university research.

Return:
- headline: one sentence on the state of the sector right now.
- outlook (positive, neutral or negative) and outlook_reason: one sentence.
- metrics: 4 to 8 key figures, such as market size, growth, investment and number of companies, each with year and source link.
- signals: the most important news since the last update (or the last 30 days on a first run): funding rounds, \
deals, regulation, big contracts, spin-offs. Date as YYYY-MM-DD: the day the news was published, never a future \
date. Impact as positive, negative or neutral, with a source link.
- funding_calls: open or upcoming calls that fit university spin-offs and research in this sector, with deadline \
(YYYY-MM-DD) and link. Leave out calls whose deadline has passed.
- companies: 6 to 12 notable companies, including Finnish ones and Aalto spin-offs, with a link.
- aalto_links: Aalto research groups, centres or spin-offs active in the sector, with a link.
- memory: the full knowledge file in Markdown with these sections: Overview, Market size and growth, Key players, \
Trends, Regulation and policy, Opportunities for Aalto inventions, Open questions, Changes since last update. \
This is a living document: keep everything from the previous memory that is still true, correct what has changed, \
and add what is new.

Give a source for every number. In memory, put the sources inline as Markdown links, for example [Fingrid, 2026](https://...), and end with a Sources section listing every link used. If you cannot find reliable data, say so instead of guessing.

Previous memory (empty on the first run):
{memory}"""


def sectors():
    """The sector list, read fresh each time so sectors added from the chat show up straight away."""
    return json.loads(SECTORS_FILE.read_text())


def sector(sector_id):
    return next(s for s in sectors() if s["id"] == sector_id)


def load(sector_id):
    """The sector's latest data, or None if it has never been updated."""
    path = LIBRARY / sector_id / "data.json"
    return json.loads(path.read_text()) if path.exists() else None


def age_days(sector_id):
    data = load(sector_id)
    return (datetime.now() - datetime.fromisoformat(data["updated"])).days if data else None


async def update(sector_id):
    """Research one sector and save memory.md, data.json and a dated copy in history/."""
    check_subscription()
    info, folder = sector(sector_id), LIBRARY / sector_id
    memory = (folder / "memory.md").read_text() if (folder / "memory.md").exists() else ""
    prompt = PROMPT.format(today=date.today(), memory=memory or "(none)", **info)
    options = agent_options(prompt, TOOLS, disallowed_tools=["Read"], output_format={"type": "json_schema", "schema": SCHEMA})
    result = None
    async for message in query(prompt=f"Update the {info['name']} sector library now.", options=options):
        if isinstance(message, ResultMessage):
            result = message
    if result is None or result.is_error or not result.structured_output:
        raise RuntimeError(f"{sector_id}: {result.errors or result.result if result else 'no result'}")
    data = {**result.structured_output, "updated": datetime.now().isoformat(timespec="minutes")}
    (folder / "history").mkdir(parents=True, exist_ok=True)
    (folder / "memory.md").write_text(data.pop("memory"))
    (folder / "data.json").write_text(json.dumps(data, indent=2, ensure_ascii=False))
    (folder / "history" / f"{data['updated'][:10]}.json").write_text(json.dumps(data, indent=2, ensure_ascii=False))
    return data


def stale():
    """Sectors that were never updated or are older than MAX_AGE_DAYS, oldest first."""
    ages = {s["id"]: age_days(s["id"]) for s in sectors()}
    due = [s for s, a in ages.items() if a is None or a >= MAX_AGE_DAYS]
    return sorted(due, key=lambda s: -1 if ages[s] is None else -ages[s])


async def main():
    for sector_id in sys.argv[1:] or stale():
        print(f"Updating {sector_id}...")
        try:
            data = await update(sector_id)
            print(f"  done: {data['headline']}")
        except Exception as error:
            print(f"  failed: {error}")


if __name__ == "__main__":
    asyncio.run(main())
