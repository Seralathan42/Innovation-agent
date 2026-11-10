"""Patent database: every EP and WO patent in each sector's field (sectors.json patent_query), pulled from the
EPO and kept up to date, plus Aalto's own patents in each field. Stored in library/patents.db (SQLite).

- pull_new(sector): everything published since the last pull (with a week of overlap for late indexing).
- backfill(sector): one older week at a time, until BACKFILL_MONTHS are covered, pausing when this week's
  EPO usage reaches WEEKLY_BUDGET_MB (it carries on after the weekly reset).
- search(...): filtering and facet counts for the Patents tab, done here so the browser never loads it all.
- build_companies() and company_search(...): the Companies tab. Every patent applicant, merged with the companies
  the sector agent profiled, in a companies table rebuilt after each round.

Usage:
    python patents.py              # one round: new patents for every sector, then a little backfill
"""

import json
import re
import sqlite3
import time
from datetime import date, datetime, timedelta
from urllib.parse import quote

import epo
import library

DB = library.LIBRARY / "patents.db"
PULL_EVERY_HOURS = 6  # EP publishes on Wednesdays and WO on Thursdays, so this catches each batch the same day
BACKFILL_MONTHS = 60  # how far back to fill in older patents (5 years)
BACKFILL_WEEKS_PER_ROUND = 8  # older weeks fetched per sector each hour
WEEKLY_BUDGET_MB = 3000  # stop backfilling at this EPO usage; the free allowance is 4,000 MB a week

KIND = "CASE WHEN kind IN ('A1','A2') THEN 'Application' WHEN kind IN ('A3','A4') THEN 'Search report' " \
       "WHEN kind LIKE 'B%' OR kind LIKE 'C%' THEN 'Granted patent' WHEN kind LIKE 'U%' OR kind LIKE 'Y%' " \
       "THEN 'Utility model' ELSE 'Other' END"
NAME = "CASE WHEN j.value LIKE '% [__]' THEN substr(j.value, 1, length(j.value) - 5) ELSE j.value END"
FACETS = {  # facet id -> (SQL for its value, JSON list column it comes from or None)
    "sector": ("p.sector", None),
    "aalto": ("CASE p.aalto WHEN 1 THEN 'Aalto patent' ELSE 'Not Aalto' END", None),
    "authority": ("substr(p.number, 1, 2)", None),
    "type": (KIND, None),
    "year": ("substr(p.date, 1, 4)", None),
    "applicant": (NAME, "applicants"),
    "applicant_country": ("CASE WHEN j.value LIKE '% [__]' THEN substr(j.value, length(j.value) - 2, 2) END", "applicants"),
    "inventor": (NAME, "inventors"),
    "cpc": (None, "cpc"),  # depends on the chosen level
    "added": ("p.first_seen", None),
}
AALTO = re.compile(r"AALTO.*(UNIV|KORKEAKOULU)|UNIV.*AALTO")  # Aalto University's spellings, not people named Aalto
COMPANY_FACETS = {
    "sector": ("j.value", "sectors"),
    "source": ("CASE p.profiled WHEN 1 THEN 'Profiled by sector agent' ELSE 'Patent applicant only' END", None),
    "type": ("p.type", None),
    "country": ("p.country", None),
    "finnish": ("CASE p.country WHEN 'FI' THEN 'Finnish' ELSE 'Not Finnish' END", None),
    "aalto": ("CASE WHEN p.aalto = 1 THEN 'Co-applicant on Aalto patents' WHEN lower(p.name || ' ' || p.what) LIKE '%aalto%' "
              "THEN 'Aalto mentioned' ELSE 'No Aalto link found' END", None),
    "patents": ("CASE WHEN p.patents = 0 THEN '0' WHEN p.patents = 1 THEN '1' WHEN p.patents <= 5 THEN '2 to 5' WHEN p.patents <= 20 "
                "THEN '6 to 20' WHEN p.patents <= 100 THEN '21 to 100' ELSE 'Over 100' END", None),
    "latest": ("substr(p.latest, 1, 4)", None),
}
COMPANY_SORTS = {"patents": "p.patents DESC, p.name", "name": "p.name COLLATE NOCASE", "latest": "p.latest DESC, p.patents DESC",
                 "profiled": "p.profiled DESC, p.patents DESC"}
COUNTRIES = {"finland": "FI", "sweden": "SE", "norway": "NO", "denmark": "DK", "estonia": "EE", "germany": "DE", "france": "FR",
             "uk": "GB", "united kingdom": "GB", "netherlands": "NL", "switzerland": "CH", "israel": "IL", "china": "CN",
             "japan": "JP", "korea": "KR", "south korea": "KR", "us": "US", "usa": "US", "united states": "US"}
SUFFIXES = {"inc", "ltd", "limited", "oy", "oyj", "ab", "gmbh", "ag", "corp", "corporation", "co", "company", "llc", "sa", "sas",
            "plc", "bv", "nv", "kk", "asa", "as", "spa", "srl", "pte", "pty", "se"}
UNIVERSITY = re.compile(r"\bUNIV|KORKEAKOULU|\bCOLLEGE\b|\bSCHOOL\b")
RESEARCH = re.compile(r"\b(INST|INSTITUTE|FORSCH\w*|FRAUNHOFER|CNRS|COMMISSARIAT|COUNCIL|ACAD\w*|FOUNDATION|HOSPITAL|VTT|RES)\b")
COMPANY = re.compile(r"\b(INC|LTD|LIMITED|OYJ?|AB|GMBH|AG|CORP|CORPORATION|CO|COMPANY|LLC|SAS?|SRL|SPA|BV|NV|PLC|KK|ASA?|APS|SE|"
                     r"PTE|PTY|HOLDINGS?|GROUP|TECH|TECHNOLOGIES)\b")
CPC_LEVEL = {"section": "substr(j.value, 1, 1)", "class": "substr(j.value, 1, 3)", "subclass": "substr(j.value, 1, 4)", "group": "j.value"}
SORTS = {"newest": "max(p.date) DESC", "oldest": "max(p.date) ASC", "title": "max(p.title) ASC", "seen": "max(p.first_seen) DESC, max(p.date) DESC"}


def db():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    con.executescript("""
        PRAGMA journal_mode = WAL;  -- the page can read while the pull writes
        CREATE TABLE IF NOT EXISTS patents (sector TEXT, number TEXT, kind TEXT, title TEXT, abstract TEXT, date TEXT,
            applicants TEXT, inventors TEXT, cpc TEXT, link TEXT, aalto INTEGER DEFAULT 0, first_seen TEXT,
            PRIMARY KEY (sector, number));
        CREATE INDEX IF NOT EXISTS patents_date ON patents (date);
        CREATE TABLE IF NOT EXISTS companies (name TEXT, applicant TEXT, country TEXT, type TEXT, sectors TEXT,
            patents INTEGER, latest TEXT, aalto INTEGER, what TEXT, link TEXT, profiled INTEGER);
        CREATE TABLE IF NOT EXISTS pulls (sector TEXT PRIMARY KEY, newest TEXT, oldest TEXT, pulled TEXT,
            total_12m INTEGER, aalto_total INTEGER);""")
    return con


def is_aalto(patent):
    return any(AALTO.search(a.upper()) for a in patent["applicants"])


def save(con, sector_id, found):
    today = date.today().isoformat()
    con.executemany("""INSERT INTO patents VALUES (:sector, :number, :kind, :title, :abstract, :date, :applicants,
            :inventors, :cpc, :link, :aalto, :today)
        ON CONFLICT (sector, number) DO UPDATE SET kind = excluded.kind, title = excluded.title, abstract = excluded.abstract,
            date = excluded.date, applicants = excluded.applicants, inventors = excluded.inventors, cpc = excluded.cpc,
            aalto = excluded.aalto""",
        [{**p, "sector": sector_id, "aalto": int(is_aalto(p)), "today": today, "kind": p.get("kind", p["number"][-2:]),
          "applicants": json.dumps(p["applicants"]), "inventors": json.dumps(p.get("inventors", [])), "cpc": json.dumps(p["cpc"])}
         for p in found])
    con.commit()


def fetch(query, start, end):
    """Every EP and WO patent published between two dates. OPS gives at most 2,000 per query, so bigger windows are split."""
    q = f'{query} and (pn=EP or pn=WO) and pd within "{start:%Y%m%d} {end:%Y%m%d}"'
    total, found = epo.search(q, 100)
    if total > 2000 and start < end:
        middle = start + (end - start) / 2
        return fetch(query, start, middle) + fetch(query, middle + timedelta(days=1), end)
    for offset in range(101, min(total, 2000) + 1, 100):
        found += epo.search(q, 100, offset)[1]
    return found


def state(con, sector_id):
    row = con.execute("SELECT * FROM pulls WHERE sector = ?", (sector_id,)).fetchone()
    return dict(row) if row else {"sector": sector_id, "newest": None, "oldest": None, "pulled": None, "total_12m": 0, "aalto_total": 0}


def put_state(con, s):
    con.execute("INSERT OR REPLACE INTO pulls VALUES (:sector, :newest, :oldest, :pulled, :total_12m, :aalto_total)", s)
    con.commit()


def pull_new(sector_id):
    """New publications since the last pull, Aalto's patents in the field and the 12-month count. Returns the number saved."""
    info, con, today = library.sector(sector_id), db(), date.today()
    s = state(con, sector_id)
    start = date.fromisoformat(s["newest"]) - timedelta(days=7) if s["newest"] else today - timedelta(days=7)
    found = fetch(info["patent_query"], start, today)
    save(con, sector_id, found)
    found_total, aalto = epo.search(f"{info['patent_query']} and pa=aalto", 100)
    for offset in range(101, min(found_total, 2000) + 1, 100):
        aalto += epo.search(f"{info['patent_query']} and pa=aalto", 100, offset)[1]
    aalto = [p for p in aalto if is_aalto(p)]  # pa=aalto also finds people and firms named Aalto
    save(con, sector_id, aalto)
    year_ago = today.replace(year=today.year - 1)
    total_12m = epo.search(f'{info["patent_query"]} and (pn=EP or pn=WO) and pd within "{year_ago:%Y%m%d} {today:%Y%m%d}"', 1)[0]
    put_state(con, {**s, "newest": today.isoformat(), "oldest": s["oldest"] or start.isoformat(),
                    "pulled": datetime.now().isoformat(timespec="minutes"), "total_12m": total_12m, "aalto_total": len(aalto)})
    return len(found)


def backfill(sector_id, weeks=BACKFILL_WEEKS_PER_ROUND):
    """Fetch older weeks until BACKFILL_MONTHS are covered. Returns the number saved."""
    info, con, saved = library.sector(sector_id), db(), 0
    limit = date.today() - timedelta(days=30 * BACKFILL_MONTHS)
    for _ in range(weeks):
        if epo.week_used_mb() >= WEEKLY_BUDGET_MB:  # keep room for new publications and chat searches
            break
        s = state(con, sector_id)
        if not s["oldest"] or date.fromisoformat(s["oldest"]) <= limit:
            break
        end = date.fromisoformat(s["oldest"]) - timedelta(days=1)
        start = max(end - timedelta(days=6), limit)
        found = fetch(info["patent_query"], start, end)
        save(con, sector_id, found)
        con.execute("UPDATE pulls SET oldest = ? WHERE sector = ?", (start.isoformat(), sector_id))  # leaves the rest as it is now
        con.commit()
        saved += len(found)
    return saved


def due(sector_id):
    s = state(db(), sector_id)
    return not s["pulled"] or datetime.now() - datetime.fromisoformat(s["pulled"]) >= timedelta(hours=PULL_EVERY_HOURS)


def backfill_left(sector_id):
    s = state(db(), sector_id)
    return not s["oldest"] or date.fromisoformat(s["oldest"]) > date.today() - timedelta(days=30 * BACKFILL_MONTHS)


def run_round(log=print):
    """One round for every sector: new publications when due, then a few older weeks.
    Returns True while older patents are still missing and this week's EPO budget has room."""
    if not epo.credentials():
        return False
    for s in library.sectors():
        if not s.get("patent_query"):
            continue
        try:
            if due(s["id"]):
                log(f"[{s['code']}] {pull_new(s['id'])} new or updated patents")
            added = backfill(s["id"])
            if added:
                log(f"[{s['code']}] backfill: {added} older patents, stored back to {state(db(), s['id'])['oldest']}, "
                    f"EPO usage this week {epo.week_used_mb():.0f} MB")
        except Exception as error:  # EPO busy or down: try again next round
            log(f"[{s['code']}] patent pull failed: {error}")
    build_companies()
    return epo.week_used_mb() < WEEKLY_BUDGET_MB and any(backfill_left(s["id"]) for s in library.sectors() if s.get("patent_query"))


def keep_pulling():
    """Runs for as long as the terminal does: rounds a minute apart while older patents are missing, hourly after that."""
    build_companies()
    while True:
        time.sleep(60 if run_round() else 3600)


def summary(sector_id):
    """What a sector's patents panel shows."""
    con = db()
    s = state(con, sector_id)
    if not s["pulled"]:
        return None
    def rows(sql, *args):
        return [row_dict(r) for r in con.execute(sql, args)]

    return {"query": library.sector(sector_id).get("patent_query"), "fetched": s["pulled"], "covered_from": s["oldest"],
            "recent_total": s["total_12m"], "aalto_total": s["aalto_total"],
            "stored": con.execute("SELECT count(*) FROM patents WHERE sector = ?", (sector_id,)).fetchone()[0],
            "recent": rows("SELECT * FROM patents WHERE sector = ? AND aalto = 0 ORDER BY date DESC LIMIT 25", sector_id),
            "aalto": rows("SELECT * FROM patents WHERE sector = ? AND aalto = 1 ORDER BY date DESC", sector_id)}


def row_dict(row):
    p = dict(row)
    for key in ("applicants", "inventors", "cpc"):
        if key in p:
            p[key] = json.loads(p[key] or "[]")
    return p


def filtered(con, table, facets, text, count, q, include, exclude, find, value=lambda facet, sql: sql):
    """Shared by both searches. Values in one facet combine with OR, facets with AND, excluded values are removed.
    Each facet's counts use every filter except its own, as in Patsnap. Returns (WHERE sql, its args, facet counts)."""
    codes = {s["id"]: s["code"] for s in library.sectors()}
    ids = {code: sector_id for sector_id, code in codes.items()}

    def where(skip=None):
        sql, args = [], []
        for word in q.lower().split():
            sql.append(f"lower({text}) LIKE ?")
            args.append(f"%{word}%")
        for facet, (column_sql, column) in facets.items():
            if facet == skip:
                continue
            for values, negate in ((include.get(facet), False), (exclude.get(facet), True)):
                if not values:
                    continue
                values = [ids.get(v, v) for v in values] if facet == "sector" else values
                marks = ",".join("?" * len(values))
                v = value(facet, column_sql)
                test = f"EXISTS (SELECT 1 FROM json_each(p.{column}) j WHERE {v} IN ({marks}))" if column else f"{v} IN ({marks})"
                sql.append(f"NOT {test}" if negate else test)
                args += values
        return (" WHERE " + " AND ".join(sql)) if sql else "", args

    counts = {}
    for facet, (column_sql, column) in facets.items():
        w, args = where(skip=facet)
        source = f"{table} p, json_each(p.{column}) j" if column else f"{table} p"
        text_find = find.get(facet, "").lower()
        having = " HAVING lower(v) LIKE ?" if text_find else ""
        order = "v DESC" if facet in ("year", "added", "latest") else "n DESC, v"
        rows = con.execute(f"SELECT {value(facet, column_sql)} v, count(DISTINCT {count}) n FROM {source}{w} GROUP BY v{having} "
                           f"ORDER BY {order} LIMIT 60", args + ([f"%{text_find}%"] if text_find else []))
        counts[facet] = [[codes.get(r["v"], r["v"]) if facet == "sector" else r["v"], r["n"]] for r in rows if r["v"]]
    return *where(), counts, codes


def search(q="", include=None, exclude=None, sort="newest", cpc_level="subclass", find=None, limit=50):
    """Filtered patents and facet counts for the Patents tab."""
    con = db()
    text = "p.title || ' ' || p.abstract || ' ' || p.number || ' ' || p.applicants || ' ' || p.inventors"
    w, args, facets, codes = filtered(con, "patents", FACETS, text, "p.number", q, include or {}, exclude or {}, find or {},
                                      value=lambda facet, sql: CPC_LEVEL[cpc_level] if facet == "cpc" else sql)
    total = con.execute(f"SELECT count(DISTINCT p.number) FROM patents p{w}", args).fetchone()[0]
    items = [row_dict(r) for r in con.execute(f"""SELECT p.number, max(p.kind) kind, max(p.title) title, max(p.abstract) abstract,
            max(p.date) date, max(p.applicants) applicants, max(p.inventors) inventors, max(p.cpc) cpc, max(p.link) link,
            max(p.aalto) aalto, min(p.first_seen) first_seen, group_concat(DISTINCT p.sector) sectors
            FROM patents p{w} GROUP BY p.number ORDER BY {SORTS.get(sort, SORTS['newest'])} LIMIT ?""", args + [limit])]
    for p in items:
        p["sectors"] = [codes.get(s, s) for s in p["sectors"].split(",")]
    stored = con.execute("SELECT count(DISTINCT number) FROM patents").fetchone()[0]
    return {"total": total, "stored": stored, "items": items, "facets": facets}


def org_type(name):
    """University or research, Company, or Person or other, guessed from the applicant name."""
    n = name.upper()
    if UNIVERSITY.search(n) or (RESEARCH.search(n) and not COMPANY.search(n)):
        return "University or research"
    return "Company" if COMPANY.search(n) or " " not in n.strip() else "Person or other"


def name_key(name):
    """A company name without punctuation and legal endings, to match "Iceye" with "ICEYE OY"."""
    words = re.sub(r"[^a-z0-9 ]", " ", re.sub(r"\(.*?\)", "", name.lower())).split()
    while len(words) > 1 and words[-1] in SUFFIXES:
        words.pop()
    return " ".join(words)


def build_companies():
    """Rebuild the companies table: every patent applicant, plus the companies the sector agent profiled. A profiled
    company takes over the matching applicant (same name, or the applicant with most patents whose name starts with it)."""
    con = db()
    rows = {}
    for r in con.execute(f"""SELECT {NAME} name, max(CASE WHEN j.value LIKE '% [__]' THEN substr(j.value, length(j.value) - 2, 2)
            ELSE '' END) country, count(DISTINCT p.number) patents, group_concat(DISTINCT p.sector) sectors, max(p.date) latest,
            max(p.aalto) aalto FROM patents p, json_each(p.applicants) j GROUP BY name"""):
        rows[r["name"]] = {**dict(r), "applicant": r["name"], "sectors": r["sectors"].split(","), "type": org_type(r["name"]),
                           "what": "", "profiled": 0,
                           "link": f"https://worldwide.espacenet.com/patent/search?q=pa%3D%22{quote(r['name'])}%22"}
    by_key = {}
    for c in rows.values():
        by_key.setdefault(name_key(c["name"]), []).append(c)
    for s in library.sectors():
        for found in (library.load(s["id"]) or {}).get("companies", []):
            k = name_key(found["name"])
            match = by_key.get(k) or (len(k) >= 3 and [c for key, cs in by_key.items() if key.startswith(k + " ") for c in cs])
            codes = [COUNTRIES[w] for w in re.split(r"\s*[,/]\s*", found["country"].lower()) if w in COUNTRIES]
            c = max(match, key=lambda c: c["patents"]) if match else rows.setdefault(found["name"], {
                "applicant": "", "country": "FI" if "FI" in codes else codes[0] if codes else found["country"], "patents": 0,
                "sectors": [], "latest": None, "aalto": 0, "type": org_type(found["name"])})
            c.update(name=found["name"], what=found["what"], link=found["link"], profiled=1)
            c["sectors"] = sorted(set(c["sectors"]) | {s["id"]})
    con.execute("DELETE FROM companies")
    con.executemany("INSERT INTO companies VALUES (:name, :applicant, :country, :type, :sectors, :patents, :latest, :aalto, :what, "
                    ":link, :profiled)", [{**c, "sectors": json.dumps(c["sectors"])} for c in rows.values()])
    con.commit()


def company_search(q="", include=None, exclude=None, sort="patents", find=None, limit=50):
    """Filtered companies and facet counts for the Companies tab."""
    con = db()
    if not con.execute("SELECT 1 FROM companies LIMIT 1").fetchone():
        build_companies()
    text = "p.name || ' ' || p.applicant || ' ' || p.what || ' ' || p.country"
    w, args, facets, codes = filtered(con, "companies", COMPANY_FACETS, text, "p.rowid", q, include or {}, exclude or {}, find or {})
    total = con.execute(f"SELECT count(*) FROM companies p{w}", args).fetchone()[0]
    items = [dict(r) for r in con.execute(f"SELECT * FROM companies p{w} ORDER BY {COMPANY_SORTS.get(sort, COMPANY_SORTS['patents'])} "
                                          f"LIMIT ?", args + [limit])]
    for c in items:
        c["sectors"] = [codes.get(s, s) for s in json.loads(c["sectors"])]
    stored = con.execute("SELECT count(*) FROM companies").fetchone()[0]
    return {"total": total, "stored": stored, "items": items, "facets": facets}


if __name__ == "__main__":
    run_round()
