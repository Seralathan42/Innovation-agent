"""Missed research: earlier Aalto papers checked against today's patents and companies, to find research that
others have since turned into business while Aalto did not.

1. fetch() and fetch_abstracts(): Aalto papers from ACRIS, Aalto's research portal, through Aalto's API gateway
   (the "Research API Public" product; its user key goes in .env as ACRIS_API_KEY). The list gives title, year,
   authors, department and citations; each abstract is a separate request. Kept in library/research.db.
2. screen(): code only, on this computer. Compares each paper with the stored patents (library/patents.db): how
   much of the paper's distinctive wording the closest patents share, who owns them, and whether the paper's own
   authors are among the inventors.
3. analyse(paper_id): only when asked, a Sonnet agent checks one paper in depth (worldwide patents at the EPO, companies, Aalto's
   own follow-up) and gives a verdict with sources.

Usage:
    python research.py              # one round: fetch more papers, screen the new ones
    python research.py <paper id>   # analyse one paper now
"""

import asyncio
import json
import math
import re
import sqlite3
import sys
import time
import unicodedata
from collections import Counter
from datetime import date, datetime, timedelta

from claude_agent_sdk import HookMatcher, ResultMessage, query

import epo
import library
import patents
from run import agent_options, check_subscription
from tools import _clean, _get

DB = library.LIBRARY / "research.db"
YEARS = (2012, 2021)  # old enough to see what happened since
MAX_AUTHORS = 25  # bigger author lists are mostly international collaborations, not Aalto inventions
CLOSE = 0.3  # a patent is close when it contains at least 30% of the paper's distinctive words (weighted by rarity)
ACRIS = "https://research.api.aalto.fi/api/acris/v1"  # Aalto's gateway in front of ACRIS (Pure)
DEPTH = {"WebSearch": 10, "WebFetch": 4, "epo_patents": 5, "search_papers": 2}  # the least an analysis must search before its verdict
TYPES = ("contributiontojournal/article", "contributiontobookanthology/conference")  # journal and conference papers
LIST_FIELDS = ("uuid,title.value,type.uri,publicationStatuses.current,publicationStatuses.publicationDate.year,"
               "totalNumberOfAuthors,totalScopusCitations,managingOrganisationalUnit.name.text.value,"
               "personAssociations.name.firstName,personAssociations.name.lastName,info.portalUrl,language.uri")

OVERLAP = ("CASE WHEN p.closeness >= 0.5 THEN 'Very close (50% or more)' WHEN p.closeness >= 0.3 THEN 'Close (30 to 50%)' "
           "WHEN p.closeness >= 0.2 THEN 'Some (20 to 30%)' WHEN p.screened IS NULL THEN 'Not screened yet' ELSE 'Little (under 20%)' END")
FACETS = {  # facet id -> (SQL for its value, JSON list column or None), as in patents.py
    "verdict": ("CASE WHEN p.analysing = 1 THEN 'Being analysed' ELSE coalesce(p.verdict, 'Not analysed yet') END", None),
    "overlap": (OVERLAP, None),
    "own": ("CASE p.own_patent WHEN 1 THEN 'Authors are inventors on a close patent' ELSE 'No patent by the authors found' END", None),
    "companies": ("CASE WHEN p.companies = 0 THEN 'None' WHEN p.companies <= 2 THEN '1 to 2' WHEN p.companies <= 5 THEN '3 to 5' "
                  "ELSE 'More than 5' END", None),
    "area": ("coalesce(p.area, 'Not given')", None),  # the department in ACRIS
    "year": ("CAST(p.year AS TEXT)", None),
}
SORTS = {"promising": "p.own_patent ASC, p.closeness * (1 + p.companies) DESC", "overlap": "p.closeness DESC",
         "companies": "p.companies DESC, p.closeness DESC", "cited": "p.citations DESC", "analysed": "p.analysed DESC",
         "year": "p.year DESC"}
COLUMNS = {"title": "p.title COLLATE NOCASE {d}", "closeness": "p.closeness {d}", "close_patents": "p.close_patents {d}",
           "companies": "p.companies {d}", "verdict": "p.verdict IS NULL, p.verdict {d}"}

VERDICTS = ["Missed opportunity", "Partly missed", "Followed up by Aalto or the authors", "No commercial use found"]
ITEM = library.ITEM
SCHEMA = {
    "type": "object",
    "properties": {
        "verdict": {"type": "string", "enum": VERDICTS},
        "confidence": {"type": "string", "enum": ["low", "medium", "high"]},
        "summary": {"type": "string"},
        "what_it_is": {"type": "string"},
        "similar_patents": ITEM("number", "owner", "first_filed", "status", "why_similar", "link"),
        "similar_research": ITEM("title", "who", "year", "relation", "link"),
        "companies": ITEM("name", "what", "success", "link"),
        "aalto_follow_up": {"type": "string"},
        "today": {"type": "string"},
    },
    "required": ["verdict", "confidence", "summary", "what_it_is", "similar_patents", "similar_research", "companies",
                 "aalto_follow_up", "today"],
    "additionalProperties": False,
}
PROMPT = """You review earlier research from Aalto University for Aalto Innovation, the unit that helps commercialise \
Aalto research. The question: did Aalto miss a commercial opportunity with this work? That is, has the same idea, \
or something very close to it, since become a successful patent or business for someone else, while Aalto and the \
authors did not protect or commercialise it? Today is {today}.

The paper:
Title: {title}
Year: {year}
Authors: {authors}
Field: {area}
Link: {link}
Abstract: {abstract}

A first screening in our local patent store found these as the closest patents. "Overlap" is the share of the \
paper's distinctive words that the patent also uses, so treat it as a hint, not proof:
{matches}

The local store is small: recent EP and WO patents in a few fields only. Most of what matters is probably not in it, \
so do not rely on it. Search online for everything below, whether or not the screening found anything, and describe \
the idea in several different wordings, since others often use other terms for the same thing.

The advisor asked for this analysis because they want depth, so be thorough: plan on 25 or more searches. Cover every \
step below, search each one in at least three wordings (technical terms, the application or product, and the \
problem it solves), and open the most promising pages to read them. A verdict of "No commercial use found" needs the \
same full search as any other. Your answer is refused until you have searched enough.

Check it properly:
1. Work out in plain words what the research could be sold as.
2. Patents: search the European Patent Office worldwide with epo_patents (keywords with ta=, the CPC classes of good \
hits, and the main applicants), and use web search on Google Patents for more. For the most similar ones use \
epo_patent to see whether they were granted and where. Note each patent's first filing date: patents filed after the \
paper was published came later than this work.
3. Similar research: use search_papers, research_trend and web search for later work on the same idea by others, \
especially work that led to patents, start-ups or products, and whether the field has grown since.
4. Companies: use web search to find companies anywhere that sell or develop the same thing, including start-ups \
and spin-offs of other universities, and evidence of success (products on the market, revenue, funding rounds, \
customers, acquisitions). Check company websites, funding news and databases you can reach.
5. Aalto's own follow-up: search epo_patents for patents by the authors (in=surname) and by Aalto (pa=aalto), and \
web search for spin-offs, licences or industry projects built on this work.

Verdict:
- Missed opportunity: others now hold patents on or sell essentially the same idea with clear commercial success, \
and neither Aalto nor the authors patented or commercialised it.
- Partly missed: similar commercial activity exists, but the overlap is partial, the success is unclear, or Aalto \
followed up only in part.
- Followed up by Aalto or the authors: they patented, licensed or spun out the idea.
- No commercial use found: nothing similar has turned into a patent or business that you can find.

Return: verdict; confidence (low, medium or high); summary (2 to 3 sentences); what_it_is; similar_patents (number, \
owner, first filed YYYY-MM-DD, status such as granted in EP or application, why it is similar, Espacenet link); \
similar_research (title, who did it, year, how it relates, for example "built on this paper" or "same idea, \
independently", link); companies (name, what they sell, the evidence of success, link); aalto_follow_up (what you found, or "None found"); \
today (what Aalto could still do now, for example follow-up research that is not yet public, or partners to talk to; \
the paper itself is published, so its own content can no longer be patented). Give a link for every claim. Say \
clearly when you could not find something rather than guessing."""


def db():
    con = sqlite3.connect(DB, timeout=30)  # wait for the other writer instead of failing
    con.row_factory = sqlite3.Row
    con.executescript("""
        PRAGMA journal_mode = WAL;
        CREATE TABLE IF NOT EXISTS papers (id TEXT PRIMARY KEY, source TEXT, title TEXT, abstract TEXT, year INTEGER,
            authors TEXT, area TEXT, link TEXT, citations INTEGER DEFAULT 0, fetched TEXT, screened TEXT, closeness REAL DEFAULT 0,
            close_patents INTEGER DEFAULT 0, companies INTEGER DEFAULT 0, own_patent INTEGER DEFAULT 0, matches TEXT,
            verdict TEXT, analysed TEXT, analysis TEXT, analysing INTEGER DEFAULT 0);
        CREATE TABLE IF NOT EXISTS fetching (source TEXT PRIMARY KEY, position TEXT, done INTEGER DEFAULT 0);""")
    return con


def acris_key():
    return epo.setting("ACRIS_API_KEY")


def _text(value):
    """A Pure text field, {"value": ...} or {"text": [{"locale": ..., "value": ...}]}, as plain text, English first."""
    if isinstance(value, dict) and "text" in value:
        texts = value["text"] or [{}]
        value = next((t for t in texts if t.get("locale") == "en_GB"), texts[0]).get("value")
    elif isinstance(value, dict):
        value = value.get("value")
    return _clean(value or "")


def acris(path, params):
    return json.loads(_get(f"{ACRIS}/{path}", {"locale": "en_GB", **params},
                           headers={"USER-KEY": acris_key(), "Accept": "application/json"}))


def first_offset():
    """Where the newest year in YEARS starts in the newest-first list, found by halving (about 18 small requests)."""
    def year(offset):
        items = acris("research-outputs", {"size": 1, "offset": offset, "order": "-publicationYear",
                                           "fields": "publicationStatuses.publicationDate.year"}).get("items") or [{}]
        return ((items[0].get("publicationStatuses") or [{}])[0].get("publicationDate") or {}).get("year") or 0
    low, high = 0, acris("research-outputs", {"size": 1, "fields": "uuid"})["count"]
    while low < high:
        middle = (low + high) // 2
        low, high = (middle + 1, high) if year(middle) > YEARS[1] else (low, middle)
    return low


def fetch(pages=50):
    """List Aalto's English journal and conference papers from YEARS, newest year first, 100 a page, carrying on where the last
    call stopped. Abstracts come later, from fetch_abstracts()."""
    if not acris_key():
        return
    con = db()
    state = con.execute("SELECT * FROM fetching WHERE source = 'acris'").fetchone()
    if state and state["done"]:
        return
    offset = int(state["position"]) if state else first_offset()
    for _ in range(pages):
        data = acris("research-outputs", {"size": 100, "offset": offset, "order": "-publicationYear", "fields": LIST_FIELDS})
        found, years = [], []
        for item in data.get("items", []):
            statuses = item.get("publicationStatuses") or [{}]
            year = (next((s for s in statuses if s.get("current")), statuses[0]).get("publicationDate") or {}).get("year")
            years.append(year or 0)
            people = [p.get("name") or {} for p in item.get("personAssociations") or []]
            english = (item.get("language") or {}).get("uri", "en_GB").endswith("en_GB")  # the patents are in English
            if not (year and english and YEARS[0] <= year <= YEARS[1] and item["type"]["uri"].endswith(TYPES)
                    and (item.get("totalNumberOfAuthors") or len(people)) <= MAX_AUTHORS):
                continue
            found.append({"id": item["uuid"], "title": _text(item.get("title")), "year": year,
                          "authors": json.dumps([f"{n.get('firstName', '')} {n.get('lastName', '')}".strip() for n in people], ensure_ascii=False),
                          "area": _text((item.get("managingOrganisationalUnit") or {}).get("name")) or None,
                          "link": (item.get("info") or {}).get("portalUrl") or "", "citations": item.get("totalScopusCitations") or 0})
        con.executemany("""INSERT INTO papers (id, source, title, year, authors, area, link, citations, fetched)
            VALUES (:id, 'acris', :title, :year, :authors, :area, :link, :citations, :today)
            ON CONFLICT (id) DO UPDATE SET title = excluded.title, area = excluded.area, citations = excluded.citations""",
                        [{**p, "today": date.today().isoformat()} for p in found])
        offset += 100
        done = not data.get("items") or (years and max(years) < YEARS[0])  # sorted newest first: past the oldest year
        con.execute("INSERT OR REPLACE INTO fetching VALUES ('acris', ?, ?)", (str(offset), int(done)))
        con.commit()
        if done:
            return


def fetch_abstracts(limit=500):
    """Fetch the abstracts of listed papers. Papers without a real one are dropped, since they cannot be compared."""
    con = db()
    missing = con.execute("SELECT id FROM papers WHERE abstract IS NULL LIMIT ?", (limit,)).fetchall()
    for row in missing:
        abstract = _text(acris(f"research-outputs/{row['id']}", {"fields": "abstract.text.value"}).get("abstract"))
        if len(abstract) >= 200:  # shorter ones are notes such as "13707 total word count", not abstracts
            con.execute("UPDATE papers SET abstract = ? WHERE id = ?", (abstract, row["id"]))
        else:
            con.execute("DELETE FROM papers WHERE id = ?", (row["id"],))
        con.commit()
    return len(missing)


def epodoc(name):
    """A person's name as the EPO writes it: capitals, no accents, ä as AE."""
    name = name.upper()
    for letter, plain in (("Ä", "AE"), ("Ö", "OE"), ("Ü", "UE"), ("Å", "AA")):
        name = name.replace(letter, plain)
    return "".join(c for c in unicodedata.normalize("NFKD", name) if not unicodedata.combining(c))


def screen(paper, pcon, df, total):
    """How close the stored patents come to one paper. Returns the columns screen_all() saves."""
    words = list(dict.fromkeys(w for w in re.findall(r"[a-z][a-z0-9-]{2,}", f"{paper['title']} {paper['abstract']}".lower())
                               if w not in patents.STOP_WORDS))[:80]
    for w in words:
        if w not in df:
            df[w] = pcon.execute("SELECT count(*) FROM patent_text WHERE patent_text MATCH ?", (f'"{w}"',)).fetchone()[0]
    rare = dict(sorted(((w, math.log(total / df[w])) for w in words if 0 < df[w] <= total * 0.02),
                       key=lambda x: -x[1])[:30])  # the paper's 30 most distinctive words that the store knows
    if len(rare) < 8:  # too little distinctive wording to compare fairly
        return {"closeness": 0, "close_patents": 0, "companies": 0, "own_patent": 0, "matches": "[]"}
    weight = sum(rare.values())
    surnames = [n.split()[-1] for n in (epodoc(a) for a in json.loads(paper["authors"])) if n.split()]
    best = {}
    for r in pcon.execute("""SELECT p.* FROM (SELECT rowid, rank FROM patent_text WHERE patent_text MATCH ? ORDER BY rank LIMIT 60) t
            JOIN patents p ON p.rowid = t.rowid""", (" OR ".join(f'"{w}"' for w in rare),)):
        prefixes = {t[:6] for t in re.findall(r"[a-z][a-z0-9-]+", f"{r['title']} {r['abstract']}".lower())}
        closeness = sum(v for w, v in rare.items() if w[:6] in prefixes) / weight
        inventors = json.loads(r["inventors"] or "[]")
        own = any(i.startswith(s + " ") for i in inventors for s in surnames)
        if r["family"] not in best or closeness > best[r["family"]]["closeness"]:
            best[r["family"]] = {"number": r["number"], "title": r["title"], "applicants": json.loads(r["applicants"]),
                                 "date": r["date"], "priority": r["priority"], "link": r["link"], "aalto": r["aalto"],
                                 "own": own, "closeness": round(closeness, 2)}
    found = sorted(best.values(), key=lambda m: -m["closeness"])
    close = [m for m in found if m["closeness"] >= CLOSE]
    owners = {re.sub(r" \[..\]$", "", a) for m in close if not m["aalto"] and not m["own"] for a in m["applicants"]}
    return {"closeness": found[0]["closeness"] if found else 0, "close_patents": len(close),
            "companies": sum(patents.org_type(o) == "Company" for o in owners),
            "own_patent": int(any(m["own"] or m["aalto"] for m in close)), "matches": json.dumps(found[:max(10, len(close))], ensure_ascii=False)}  # every close one, so the company list matches the count


def screen_all(limit=2000):
    """Screen papers never screened, or screened more than a week ago (the patent store keeps growing)."""
    con, pcon = db(), patents.db()
    total = pcon.execute("SELECT count(*) FROM patents").fetchone()[0]
    if not total:
        return 0
    week_ago, df = (date.today() - timedelta(days=7)).isoformat(), {}
    papers = con.execute("SELECT * FROM papers WHERE abstract IS NOT NULL AND (screened IS NULL OR screened < ?) LIMIT ?",
                         (week_ago, limit)).fetchall()
    for paper in papers:
        con.execute("UPDATE papers SET screened = :today, closeness = :closeness, close_patents = :close_patents, "
                    "companies = :companies, own_patent = :own_patent, matches = :matches WHERE id = :id",
                    {**screen(paper, pcon, df, total), "today": date.today().isoformat(), "id": paper["id"]})
    con.commit()
    return len(papers)


def depth_check():
    """A hook that counts the agent's searches and sends its answer back until each tool in DEPTH was used enough."""
    used = Counter()

    async def hook(data, tool_use_id, context):
        name = data["tool_name"].removeprefix("mcp__data__")
        if name != "StructuredOutput":
            used[name] += 1
            return {}
        short = [f"{tool} {used[tool]} of {least}" for tool, least in DEPTH.items() if used[tool] < least]
        used["refused"] += 1
        if not short or used["refused"] > 3:  # give up after three refusals rather than loop
            return {}
        return {"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny", "permissionDecisionReason":
                f"Not yet: the search is too shallow for a verdict (searches so far, of the least needed: {', '.join(short)}). "
                "Keep searching the steps you covered least, in new wordings, then return the result again."}}
    return {"PreToolUse": [HookMatcher(hooks=[hook])]}, used


async def analyse(paper_id):
    """Check one paper in depth with a Sonnet agent and save its verdict."""
    check_subscription()
    con = db()
    paper = con.execute("SELECT * FROM papers WHERE id = ?", (paper_id,)).fetchone()
    con.execute("UPDATE papers SET analysing = 1 WHERE id = ?", (paper_id,))
    con.commit()
    try:
        matches = json.loads(paper["matches"] or "[]")
        listed = "\n".join(f"- {m['number']} (first filed {m['priority'] or '?'}, published {m['date']}) {m['title']}. "
                           f"Applicants: {', '.join(m['applicants'])}. Overlap {m['closeness']:.0%}. {m['link']}" for m in matches)
        prompt = PROMPT.format(today=date.today(), matches=listed or "(no close patents in the local store)",
                               **{k: paper[k] for k in ("title", "year", "area", "link", "abstract")},
                               authors=", ".join(json.loads(paper["authors"])))
        hooks, used = depth_check()
        options = agent_options(prompt, ["WebSearch", "WebFetch", "epo_patents", "epo_patent", "google_patent",
                                         "search_papers", "research_trend", "finnish_companies"],
                                disallowed_tools=["Read"], output_format={"type": "json_schema", "schema": SCHEMA},
                                effort="high", hooks=hooks)
        result = None
        async for message in query(prompt="Review this paper now.", options=options):
            if isinstance(message, ResultMessage):
                result = message
        if result is None or result.is_error or not result.structured_output:
            raise RuntimeError(result.errors or result.result if result else "no result")
        found = {**result.structured_output, "searches": sum(n for tool, n in used.items() if tool != "refused")}
        con.execute("UPDATE papers SET verdict = ?, analysis = ?, analysed = ? WHERE id = ?",
                    (found["verdict"], json.dumps(found, ensure_ascii=False), datetime.now().isoformat(timespec="minutes"), paper_id))
    finally:
        con.execute("UPDATE papers SET analysing = 0 WHERE id = ?", (paper_id,))
        con.commit()
    return found


def keep_up(log=print):
    """Runs for as long as the terminal does: list papers, fetch their abstracts and screen them, a minute apart while
    work is left and every half hour after that. Analysis only happens when asked."""
    db().execute("UPDATE papers SET analysing = 0").connection.commit()  # an analysis cut off by a restart
    while True:
        busy = False
        try:
            fetch()
            busy = fetch_abstracts() > 0
            n = screen_all()
            if n:
                log(f"[research] screened {n} papers")
        except Exception as error:  # ACRIS is down: try again later
            log(f"[research] {error}")
        time.sleep(60 if busy else 1800)


def search(q="", include=None, exclude=None, sort="promising", find=None, limit=50, facets=None):
    """Filtered papers and facet counts for the Research tab."""
    con = db()
    w, args, counts, _ = patents.filtered(con, "papers", FACETS, "p.title || ' ' || p.abstract || ' ' || p.authors", "p.id",
                                          q, include or {}, exclude or {}, find or {}, only=facets, base="p.abstract IS NOT NULL")
    total = con.execute(f"SELECT count(*) FROM papers p{w}", args).fetchone()[0]
    items = [dict(r) for r in con.execute(f"SELECT id, title, year, area, link, citations, closeness, close_patents, companies, "
                                          f"own_patent, verdict, analysing FROM papers p{w} ORDER BY {patents.order(sort, SORTS, COLUMNS, 'promising')} "
                                          f"LIMIT ?", args + [limit])]
    stored = con.execute("SELECT count(*) FROM papers WHERE abstract IS NOT NULL").fetchone()[0]
    waiting = con.execute("SELECT count(*) FROM papers WHERE abstract IS NULL").fetchone()[0]
    return {"total": total, "stored": stored, "waiting": waiting, "items": items, "facets": counts, "connected": bool(acris_key())}


def paper(paper_id):
    row = db().execute("SELECT * FROM papers WHERE id = ?", (paper_id,)).fetchone()
    if not row:
        return None
    p = dict(row)
    for key in ("authors", "matches", "analysis"):
        p[key] = json.loads(p[key]) if p[key] else None
    owners = {re.sub(r" \[..\]$", "", a) for m in p["matches"] or [] if m["closeness"] >= CLOSE and not m["aalto"] and not m["own"]
              for a in m["applicants"]}
    p["companies_found"] = sorted(o for o in owners if patents.org_type(o) == "Company")  # the ones the list counts
    return p


if __name__ == "__main__":
    if sys.argv[1:]:
        print(json.dumps(asyncio.run(analyse(sys.argv[1])), indent=2, ensure_ascii=False))
    else:
        fetch()
        print(f"abstracts fetched for {fetch_abstracts()} papers, screened {screen_all()}")
