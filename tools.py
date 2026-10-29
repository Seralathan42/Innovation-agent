"""Free data sources the agents can call as tools. None of them needs an API key.

To give an agent a tool, add the tool's name to the 'tools:' line at the top of its file in agents/.
"""

import asyncio
import functools
import html
import json
import os
import re
import urllib.parse
import urllib.request
import uuid
from datetime import date

from claude_agent_sdk import ToolAnnotations, tool

READ_ONLY = ToolAnnotations(readOnlyHint=True)  # lets an agent run several lookups at once


def _get(url, params=None, data=None, headers=None):
    """Download a URL and return the body as text."""
    if params:
        url += "?" + urllib.parse.urlencode(params, doseq=True)
    request = urllib.request.Request(url, data=data, headers={"User-Agent": "Mozilla/5.0 (innovation-agents)", **(headers or {})})
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read().decode()


async def _fetch(*args, **kwargs):
    return await asyncio.to_thread(_get, *args, **kwargs)


def _reply(text):
    return {"content": [{"type": "text", "text": text}]}


def _clean(fragment):
    """HTML to plain text on one line."""
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", fragment or ""))).strip()


# ---------- Patents: Google Patents ----------

@tool(
    "google_patent",
    "Read one patent from Google Patents by publication number, e.g. US20200411873A1 or EP3544099A1. "
    "Returns title, owner, inventors, dates, legal status, countries it was filed in, CPC classes, timeline, "
    "abstract, claims, and the patents it cites, that cite it, and that are similar to it. "
    "Find starting patent numbers with web search, then follow the cited, citing and similar lists.",
    {"number": str},
    annotations=READ_ONLY,
)
async def google_patent(args):
    number = re.sub(r"[^A-Za-z0-9]", "", args["number"]).upper()
    url = f"https://patents.google.com/patent/{number}/en"
    page = await _fetch(url)

    def first(pattern):
        match = re.search(pattern, page, re.S)
        return _clean(match.group(1)) if match else "not given"

    def unique(pattern):
        return ", ".join(dict.fromkeys(_clean(m) for m in re.findall(pattern, page, re.S))) or "not given"

    def rows(prop):
        found = re.findall(rf'<tr itemprop="{prop}".*?</tr>', page, re.S)
        return "\n".join("  " + _clean(row) for row in found[:15]) or "  none"

    cpc = re.findall(r'itemprop="Code">([^<]+)</span>&mdash;<span itemprop="Description">([^<]+)</span>\s*<meta itemprop="Leaf"', page)
    events = re.findall(r'<dd itemprop="events".*?datetime="([^"]+)".*?itemprop="title">(.*?)</span>', page, re.S)
    return _reply(f"""{number}: {first(r'<span itemprop="title">(.*?)</span>')}
Link: {url}
Status: {first(r'itemprop="status">(.*?)<')} | priority date {first(r'itemprop="priorityDate" datetime="([^"]+)"')} | filed {first(r'itemprop="filingDate" datetime="([^"]+)"')} | published {first(r'itemprop="publicationDate" datetime="([^"]+)"')}
Owner: {unique(r'itemprop="assigneeCurrent"[^>]*>(.*?)</dd>')} | Inventors: {unique(r'itemprop="inventor"[^>]*>(.*?)</dd>')}
Filed in: {", ".join(dict.fromkeys(re.findall(r'itemprop="countryCode">(\w+)<', page)))}
CPC classes: {"; ".join(f"{code} {_clean(text)}" for code, text in dict.fromkeys(cpc))}
Timeline: {"; ".join(f"{day} {_clean(title)}" for day, title in events)}
Abstract: {first(r'itemprop="abstract".*?itemprop="content"[^>]*>(.*?)</section>')}
Claims: {first(r'itemprop="claims".*?itemprop="content"[^>]*>(.*?)</section>')[:5000]}
Cites:
{rows("backwardReferences")}
Cited by:
{rows("forwardReferences")}
Similar documents:
{rows("similarDocuments")}""")


# ---------- Scientific papers: OpenAlex ----------

@tool(
    "search_papers",
    "Search scientific papers in OpenAlex (over 250 million works). Returns title, year, citations, authors, "
    "institutions, funders, DOI and the start of the abstract for the 10 best matches. Use short keyword queries.",
    {"query": str},
    annotations=READ_ONLY,
)
async def search_papers(args):
    params = {"search": args["query"], "per_page": 10}
    if os.environ.get("OPENALEX_API_KEY"):  # optional free key for a bigger daily allowance
        params["api_key"] = os.environ["OPENALEX_API_KEY"]
    data = json.loads(await _fetch("https://api.openalex.org/works", params))
    lines = [f"{data['meta']['count']} papers found. Best matches:"]
    for work in data["results"]:
        words = {pos: word for word, positions in (work.get("abstract_inverted_index") or {}).items() for pos in positions}
        abstract = " ".join(words[pos] for pos in sorted(words))[:500]
        authors = ", ".join(a["author"]["display_name"] for a in work["authorships"][:4])
        institutions = ", ".join(dict.fromkeys(i["display_name"] for a in work["authorships"] for i in a["institutions"]))
        funders = ", ".join(f["display_name"] for f in work.get("funders") or []) or "not given"
        lines.append(
            f"- {work['display_name']} ({work['publication_year']}, cited {work['cited_by_count']} times) {work['doi'] or work['id']}\n"
            f"  Authors: {authors}. Institutions: {institutions[:300]}. Funders: {funders}.\n  Abstract: {abstract}"
        )
    return _reply("\n".join(lines))


# ---------- EU funding calls: Funding & Tenders Portal ----------

@tool(
    "eu_funding_calls",
    "Search EU funding calls that are open or upcoming (Horizon Europe, EIC, Digital Europe, LIFE and others). "
    "Returns topic ID, title, type of action, opening date and deadline. Read a call in full with eu_call_details.",
    {"query": str},
    annotations=READ_ONLY,
)
async def eu_funding_calls(args):
    # type 1 = call topic, 8 = cascade funding call; status 31094501 = forthcoming, 31094502 = open
    query = {"bool": {"must": [{"terms": {"type": ["1", "8"]}}, {"terms": {"status": ["31094501", "31094502"]}}]}}
    boundary = uuid.uuid4().hex
    body = "".join(
        f'--{boundary}\r\nContent-Disposition: form-data; name="{name}"; filename="blob"\r\n'
        f"Content-Type: application/json\r\n\r\n{json.dumps(value)}\r\n"
        for name, value in {"query": query, "languages": ["en"]}.items()
    ) + f"--{boundary}--\r\n"
    data = json.loads(await _fetch(
        "https://api.tech.ec.europa.eu/search-api/prod/rest/search",
        {"apiKey": "SEDIA", "text": args["query"], "pageSize": 100, "pageNumber": 1},
        data=body.encode(),
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
    ))
    today = date.today().isoformat()
    calls = {}  # best matches first, one line per topic
    for result in data["results"]:
        meta = result["metadata"]
        deadline = max((d[:10] for d in meta.get("deadlineDate") or []), default="not set")
        opens = min((d[:10] for d in meta.get("startDate") or []), default="not set")
        if max(deadline, opens) < today:  # the portal still marks some past calls as open
            continue
        topic = meta.get("identifier", ["?"])[0]
        calls[topic] = f"- {topic}: {meta.get('title', ['?'])[0]} | {', '.join(meta.get('typesOfAction', []))} | opens {opens} | deadline {deadline}"
    return _reply("\n".join(list(calls.values())[:25]) or "No open or upcoming EU calls found for these words.")


@tool(
    "eu_call_details",
    "Read one EU funding call topic in full by its topic ID (from eu_funding_calls): expected outcomes, scope, "
    "budget, deadlines and conditions.",
    {"topic_id": str},
    annotations=READ_ONLY,
)
async def eu_call_details(args):
    topic = args["topic_id"].strip().lower()
    details = json.loads(await _fetch(f"https://ec.europa.eu/info/funding-tenders/opportunities/data/topicDetails/{topic}.json"))["TopicDetails"]

    def day(milliseconds):
        return date.fromtimestamp(int(milliseconds) / 1000).isoformat()

    actions = (details.get("budgetOverviewJSONItem") or {}).get("budgetTopicActionMap", {}).values()
    budget = "\n".join(
        f"- {b['action'].split(' - ', 1)[-1]}: total {sum(int(v) for v in b['budgetYearMap'].values()):,} EUR, "
        f"about {b.get('expectedGrants')} grants of {b.get('minContribution')} to {b.get('maxContribution')} EUR each, "
        f"opens {day(b['plannedOpeningDate'])}, deadline {', '.join(day(d) for d in b['deadlineDates'])}"
        for action in actions for b in action if b["action"].startswith(details["identifier"])  # the call's other topics are listed too
    )
    status = ", ".join(a["status"]["description"] for a in details.get("actions") or [])
    return _reply(f"""{details['identifier']}: {details['title']}
Call: {details.get('callTitle')} | Status: {status}
Link: https://ec.europa.eu/info/funding-tenders/opportunities/portal/screen/opportunities/topic-details/{topic}
Budget:
{budget or "not given"}

{_clean(details.get('description'))[:6000]}

Conditions: {_clean(details.get('conditions'))[:2000]}""")


# ---------- Finnish companies: PRH / YTJ trade register ----------

@tool(
    "finnish_companies",
    "Search the Finnish Trade Register (PRH/YTJ) by company name, main line of business (TOL 2008 code, "
    "e.g. 27200 = manufacture of batteries and accumulators), city, or a mix. Returns business ID, name, company form, "
    "industry, website, registration date, address and register status for up to 20 companies. No financial figures.",
    {
        "type": "object",
        "properties": {"name": {"type": "string"}, "industry_code": {"type": "string"}, "city": {"type": "string"}},
    },
    annotations=READ_ONLY,
)
async def finnish_companies(args):
    params = {"name": args.get("name"), "mainBusinessLine": args.get("industry_code"), "location": args.get("city")}
    data = json.loads(await _fetch(
        "https://avoindata.prh.fi/opendata-ytj-api/v3/companies", {k: v for k, v in params.items() if v}
    ))

    def english(item):
        return next((d["description"] for d in (item or {}).get("descriptions", []) if d["languageCode"] == "3"), "")

    def current(items):
        return [item for item in items or [] if not item.get("endDate")]

    lines = [f"{data['totalResults']} companies found."]
    for company in data["companies"][:20]:
        name = next((n["name"] for n in current(company["names"])), company["names"][0]["name"])
        address = next((a for a in company.get("addresses") or [] if a["type"] == 1), None)
        city = next((p["city"] for p in (address or {}).get("postOffices", []) if p["languageCode"] == "1"), "")
        where = f"{address['street']} {address['buildingNumber']}, {address['postCode']} {city}" if address else "not given"
        status = ", ".join(dict.fromkeys(english(e) for e in current(company.get("registeredEntries")) + company.get("companySituations", [])))
        form = ", ".join(english(f) for f in current(company.get("companyForms"))) or "form not given"
        industry = company.get("mainBusinessLine") or {}
        lines.append(
            f"- {name} ({company['businessId']['value']}), {form}. "
            f"Industry: {industry.get('type', '?')} {english(industry)}. Website: {(company.get('website') or {}).get('url', 'not given')}. "
            f"Registered {company.get('registrationDate')}. Address: {where}. Status: {status}"
        )
    return _reply("\n".join(lines))


# ---------- Statistics: Eurostat ----------

@functools.cache
def _eurostat_catalogue():
    return [line.replace('"', "").split("\t") for line in _get(
        "https://ec.europa.eu/eurostat/api/dissemination/catalogue/toc/txt", {"lang": "en"}
    ).splitlines()[1:]]


@tool(
    "eurostat_search",
    "Find Eurostat datasets whose title contains all the given words, e.g. 'enterprises turnover', "
    "'industrial production' or 'international trade'. Returns dataset code, title and years covered. "
    "Then get the numbers with eurostat_data.",
    {"words": str},
    annotations=READ_ONLY,
)
async def eurostat_search(args):
    words = args["words"].lower().split()
    rows = [r for r in await asyncio.to_thread(_eurostat_catalogue) if r[2] in ("dataset", "table") and all(w in r[0].lower() for w in words)]
    return _reply("\n".join(f"- {r[1]}: {r[0].strip()} ({r[5]} to {r[6]})" for r in rows[:30]) or "No datasets found. Try fewer or other words.")


@tool(
    "eurostat_data",
    "Get numbers from one Eurostat dataset. 'filters' maps dimension codes to values, e.g. "
    '{"geo": ["FI", "SE", "EU27_2020"], "sinceTimePeriod": "2020"}. Start with a narrow request such as '
    '{"geo": "FI", "lastTimePeriod": "1"} to see the dimensions, then ask for what you need. Returns up to 300 values.',
    {
        "type": "object",
        "properties": {"dataset": {"type": "string"}, "filters": {"type": "object"}},
        "required": ["dataset"],
    },
    annotations=READ_ONLY,
)
async def eurostat_data(args):
    data = json.loads(await _fetch(
        f"https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/{args['dataset']}",
        {"lang": "en", **(args.get("filters") or {})},
    ))
    dims = [(d, data["dimension"][d]["category"]) for d in data["id"]]
    codes = [sorted(cat["index"], key=cat["index"].get) for _, cat in dims]
    fixed = [f"{d}={cat['label'][c[0]]}" for (d, cat), c in zip(dims, codes) if len(c) == 1]
    lines = [f"{data['label']}. Same for all values: {', '.join(fixed)}"]
    for flat, value in sorted(data["value"].items(), key=lambda item: int(item[0]))[:300]:
        position, parts = int(flat), []
        for (d, cat), c, size in reversed(list(zip(dims, codes, data["size"]))):
            position, i = divmod(position, size)
            if size > 1:
                parts.append(f"{d}={cat['label'][c[i]]}")
        lines.append(f"{', '.join(reversed(parts))}: {value}")
    return _reply("\n".join(lines))


# ---------- Research projects and funding: OpenAIRE ----------

@tool(
    "research_projects",
    "Search research projects funded by the EU, the Research Council of Finland and many other national funders "
    "(OpenAIRE). Returns title, project code, funder, dates, funded amount and summary. All words must match, so use "
    "1 to 3 broad keywords. Optional funder filter: EC for the EU, AKA for the Research Council of Finland.",
    {
        "type": "object",
        "properties": {"query": {"type": "string"}, "funder": {"type": "string"}},
        "required": ["query"],
    },
    annotations=READ_ONLY,
)
async def research_projects(args):
    params = {"search": args["query"], "pageSize": 15}
    if args.get("funder"):
        params["fundingShortName"] = args["funder"]
    data = json.loads(await _fetch("https://api.openaire.eu/graph/v1/projects", params))
    lines = [f"{data['header']['numFound']} projects found."]
    for project in data["results"]:
        funders = ", ".join(f"{f['name']} ({f.get('jurisdiction') or '?'})" for f in project.get("fundings") or [])
        granted = project.get("granted") or {}
        amount = f"{granted['fundedAmount']:,.0f} {granted.get('currency', '')}" if granted.get("fundedAmount") else "amount not given"
        lines.append(
            f"- {project['title']} ({project.get('acronym') or project['code']}), {funders}, "
            f"{project.get('startDate')} to {project.get('endDate')}, {amount}\n  {_clean(project.get('summary'))[:400]}"
        )
    return _reply("\n".join(lines))


TOOLS = {t.name: t for t in [
    google_patent, search_papers, eu_funding_calls, eu_call_details,
    finnish_companies, eurostat_search, eurostat_data, research_projects,
]}
