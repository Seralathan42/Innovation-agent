"""Profiles of companies and people, built the first time someone clicks a name and then kept.

A Sonnet agent researches the name on the web (public, professional information only) and returns a structured
profile. Profiles are stored in library/profiles.db, so a second click opens straight away; Update builds it again.
"""

import asyncio
import json
import sqlite3
from datetime import datetime

from claude_agent_sdk import ResultMessage, query

import library
from run import agent_options, check_subscription
from tools import images_on

DB = library.LIBRARY / "profiles.db"
ITEM = library.ITEM

SCHEMAS = {
    "company": {
        "type": "object",
        "properties": {
            **{k: {"type": "string"} for k in ["name", "summary", "building", "website", "logo", "founded", "headquarters",
                                               "size", "funding"]},
            "people": ITEM("name", "role", "photo", "background", "link"),
            "sources": ITEM("title", "link"),
        },
        "required": ["name", "summary", "building", "website", "logo", "founded", "headquarters", "size", "funding",
                     "people", "sources"],
        "additionalProperties": False,
    },
    "person": {
        "type": "object",
        "properties": {
            **{k: {"type": "string"} for k in ["name", "photo", "headline", "summary"]},
            "current": ITEM("role", "organisation", "since"),
            "past": ITEM("role", "organisation", "years", "highlight"),
            "sources": ITEM("title", "link"),
        },
        "required": ["name", "photo", "headline", "summary", "current", "past", "sources"],
        "additionalProperties": False,
    },
}

RULES = """Use web search and read the pages. Use only public, professional information from sources such as the \
official website, press releases, news, Wikipedia, company registers and public professional profiles. Leave out \
anything private (home address, family, personal contact details, health). For pictures, use page_images on the \
company's team, about or press pages, the person's page or their Wikipedia article, and give the link of the picture \
that matches by alt text or file name; give an empty string if none matches, and never guess a link. Write "Not found" for facts you cannot find. Give the pages you used as \
sources. Today is {today}."""

PROMPTS = {
    "company": """Build a short profile of the company "{name}" for an innovation advisor at Aalto University. It was \
mentioned in this context, which tells you which company is meant: {context}

Return: name (the short name people use, without legal notes); summary (3 to 4 sentences: what they do, for whom, how far they have come); building \
(what they are building or selling now, in more detail: products, technology, stage); website; logo (image link or \
empty; look on the homepage with page_images); founded (the year only); headquarters (city and country only); size \
(for example "about 20 employees"); funding (one or two sentences) (rounds, investors and amounts, or revenue if listed); \
people: the 3 to 6 key people (founders, CEO, CTO, research leads), each with role, photo (image link or empty), \
background (their most impressive past work in one or two sentences, for example earlier roles at well-known \
companies, companies they founded, research or awards) and a link to a page about them; sources.

""" + RULES,
    "person": """Build a short professional profile of "{name}" for an innovation advisor at Aalto University. The \
name was mentioned in this context, which tells you which person is meant: {context}

Return: name; photo (image link or empty); headline (current main role in one line); summary (3 to 4 sentences on \
who they are and what they are known for); current: their current roles (role, organisation, since when); past: \
earlier roles and work, most impressive first (role, organisation, years, highlight: what they achieved there); \
sources.

""" + RULES,
}


def db():
    con = sqlite3.connect(DB, timeout=30)
    con.row_factory = sqlite3.Row
    con.execute("""CREATE TABLE IF NOT EXISTS profiles (key TEXT PRIMARY KEY, kind TEXT, name TEXT, data TEXT, built TEXT,
        building INTEGER DEFAULT 0, error TEXT)""")
    return con


def key(kind, name):
    return f"{kind}:{' '.join(name.lower().split())}"


def get(kind, name):
    """The stored profile, with its status: missing, building, ready or failed."""
    row = db().execute("SELECT * FROM profiles WHERE key = ?", (key(kind, name),)).fetchone()
    if not row:
        return {"status": "missing"}
    status = "building" if row["building"] else "ready" if row["data"] else "failed"
    return {"status": status, "data": json.loads(row["data"]) if row["data"] else None, "built": row["built"], "error": row["error"]}


async def build(kind, name, context=""):
    """Research one company or person with a Sonnet agent and store the profile."""
    check_subscription()
    con, k = db(), key(kind, name)
    con.execute("INSERT INTO profiles (key, kind, name, building) VALUES (?, ?, ?, 1) ON CONFLICT (key) DO UPDATE SET "
                "building = 1, error = NULL", (k, kind, name))
    con.commit()
    try:
        prompt = PROMPTS[kind].format(name=name, context=context or "none given", today=datetime.now().date())
        tools = ["WebSearch", "WebFetch", "page_images"] + (["finnish_companies"] if kind == "company" else [])
        options = agent_options(prompt, tools, disallowed_tools=["Read"],
                                output_format={"type": "json_schema", "schema": SCHEMAS[kind]})
        result = None
        async for message in query(prompt=f"Build the profile of {name} now.", options=options):
            if isinstance(message, ResultMessage):
                result = message
        if result is None or result.is_error or not result.structured_output:
            raise RuntimeError(result.errors or result.result if result else "no result")
        data = result.structured_output
        if kind == "company" and not data["logo"].startswith("https://") and data["website"].startswith("http"):
            data["logo"] = await asyncio.to_thread(site_picture, data["website"])  # the agent found none: use the site's own
        con.execute("UPDATE profiles SET data = ?, built = ?, building = 0 WHERE key = ?",
                    (json.dumps(data, ensure_ascii=False), datetime.now().isoformat(timespec="minutes"), k))
    except Exception as error:
        con.execute("UPDATE profiles SET building = 0, error = ? WHERE key = ?", (str(error)[:300], k))
    con.commit()


def site_picture(website):
    """The logo or preview picture a company's homepage offers, or an empty string."""
    try:
        found = images_on(website)
    except Exception:
        return ""
    logos = [src for alt, src in found if "logo" in (alt + src).lower()]
    return next((src for src in logos + [src for _, src in found[:2]] if src.startswith("https://")), "")


def reset():
    """A build cut off by a restart is not running any more."""
    db().execute("UPDATE profiles SET building = 0").connection.commit()
