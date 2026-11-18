"""European Patent Office Open Patent Services (OPS 3.2): login and bibliographic search.

Needs EPO_KEY and EPO_SECRET (the consumer key and secret of your app at developers.epo.org) in the
environment or in a .env file in this folder. See docs/epo-ops.md for how OPS works and its limits.
"""

import base64
import json
import os
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

BASE = "https://ops.epo.org/3.2"
ENV_FILE = Path(__file__).parent / ".env"
_token = {"value": None, "expires": 0}


def setting(name):
    """A key from the environment or the .env file in this folder, or None."""
    values = dict(os.environ)
    if ENV_FILE.exists():
        for line in ENV_FILE.read_text().splitlines():
            if "=" in line and not line.lstrip().startswith("#"):
                key, value = line.split("=", 1)
                values.setdefault(key.strip(), value.strip().strip('"'))
    return values.get(name) or None


def credentials():
    """EPO_KEY and EPO_SECRET, or None if they are missing."""
    key, secret = setting("EPO_KEY"), setting("EPO_SECRET")
    return (key, secret) if key and secret else None


def token():
    """An OAuth access token. OPS tokens last about 20 minutes, so a new one is fetched after 19."""
    if _token["value"] and time.time() < _token["expires"]:
        return _token["value"]
    if not credentials():
        raise RuntimeError("EPO_KEY and EPO_SECRET are not set. Add them to the .env file (see docs/epo-ops.md).")
    basic = base64.b64encode(":".join(credentials()).encode()).decode()
    request = urllib.request.Request(f"{BASE}/auth/accesstoken", data=b"grant_type=client_credentials", headers={
        "Authorization": f"Basic {basic}", "Content-Type": "application/x-www-form-urlencoded"})
    with urllib.request.urlopen(request, timeout=30) as response:
        _token.update(value=json.load(response)["access_token"], expires=time.time() + 19 * 60)
    return _token["value"]


def _get(path, params, attempt=0):
    url = f"{BASE}/rest-services/{path}?{urllib.parse.urlencode(params)}"
    request = urllib.request.Request(url, headers={"Authorization": f"Bearer {token()}", "Accept": "application/json"})
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            _token["week_used"] = int(response.headers.get("X-RegisteredQuotaPerWeek-Used") or _token.get("week_used", 0))
            return json.load(response)
    except urllib.error.HTTPError as error:
        if error.code == 404:  # OPS answers "no results" with 404
            return None
        if error.code in (400, 401) and b"token" in error.read().lower():  # expired token: log in again once
            _token["value"] = None
            return _get(path, params, attempt)
        if error.code == 403 and attempt < 3 and "quota" not in (error.headers.get("X-Rejection-Reason") or "").lower():
            time.sleep(20 * (attempt + 1))  # throttled: when OPS is busy it allows only a few searches a minute
            return _get(path, params, attempt + 1)
        raise


def week_used_mb():
    """EPO's own count of this week's usage (from the last reply), in MB. The free allowance is 4,000 MB a week."""
    return _token.get("week_used", 0) / 1_000_000


def _list(value):
    return value if isinstance(value, list) else [value] if value else []


def _text(value):
    return " ".join(v.get("$", "") for v in _list(value) if isinstance(v, dict)).strip()


def _day(yyyymmdd):
    return f"{yyyymmdd[:4]}-{yyyymmdd[4:6]}-{yyyymmdd[6:]}" if len(yyyymmdd) == 8 else yyyymmdd


def search(cql, count=25, start=1):
    """Search published patents with a CQL query. Returns (total hits, list of patents).

    Each patent: number, kind, family (the same for every publication of one invention), title, applicants,
    inventors, date (published), priority (first filing), cpc, abstract and an Espacenet link.
    OPS returns at most 100 results per request and 2,000 per query; use start to page (1, 101, 201 ...).
    """
    time.sleep(max(0, _token.get("last_search", 0) + 12 - time.time()))  # at most 5 searches a minute, OPS's busiest limit
    _token["last_search"] = time.time()
    data = _get("published-data/search/biblio", {"q": cql, "Range": f"{start}-{start + min(count, 100) - 1}"})
    if not data:
        return 0, []
    found = data["ops:world-patent-data"]["ops:biblio-search"]
    patents = []
    for document in _list(found["ops:search-result"].get("exchange-documents")):
        doc = document["exchange-document"]
        if not all(k in doc for k in ("@country", "@doc-number", "@kind")):  # OPS sometimes lists an entry it has no data for
            continue
        biblio = doc.get("bibliographic-data", {})
        number = f"{doc['@country']}{doc['@doc-number']}{doc['@kind']}"
        ids = _list(biblio.get("publication-reference", {}).get("document-id"))
        date = next((i["date"]["$"] for i in ids if "date" in i), "")
        titles = _list(biblio.get("invention-title"))
        title = next((t["$"] for t in titles if t.get("@lang") == "en"), titles[0]["$"] if titles else "")
        parties = biblio.get("parties", {}).get("applicants", {}).get("applicant")
        applicants = [_text(a["applicant-name"]["name"]) for a in _list(parties) if a.get("@data-format") == "epodoc"]
        found_inventors = biblio.get("parties", {}).get("inventors", {}).get("inventor")
        inventors = [_text(i["inventor-name"]["name"]) for i in _list(found_inventors) if i.get("@data-format") == "epodoc"]
        cpc = []
        for c in _list(biblio.get("patent-classifications", {}).get("patent-classification")):
            parts = [c.get(k, {}).get("$", "") for k in ("section", "class", "subclass", "main-group")]
            cpc.append(f"{''.join(parts[:3])}{parts[3]}/{c.get('subgroup', {}).get('$', '')}")
        abstracts = _list(doc.get("abstract"))  # English if there is one, otherwise whatever language it has
        abstract = next((_text(a.get("p")) for a in abstracts if a.get("@lang") == "en"), _text(abstracts[0].get("p")) if abstracts else "")
        filed = [i["date"]["$"] for claim in _list(biblio.get("priority-claims", {}).get("priority-claim"))
                 for i in _list(claim.get("document-id")) if "date" in i]
        filed += [i["date"]["$"] for i in _list(biblio.get("application-reference", {}).get("document-id")) if "date" in i]
        patents.append({
            "number": number, "kind": doc["@kind"], "family": doc.get("@family-id") or number, "title": title,
            "applicants": applicants, "inventors": inventors, "cpc": sorted(set(cpc)),
            "date": _day(date), "priority": _day(min(filed, default="")), "abstract": abstract,
            "link": f"https://worldwide.espacenet.com/patent/search?q=pn%3D{number}",
        })
    return int(found.get("@total-result-count", 0)), patents


def details(number):
    """One patent in depth, by publication number (EP3544099A1 or EP3544099): every publication in its family with
    that publication's legal events, and the claims. A family member with kind B is a granted patent."""
    epodoc = re.sub(r"[A-Z]\d?$", "", re.sub(r"[^A-Z0-9]", "", number.upper()))
    family = _get(f"family/publication/epodoc/{epodoc}/legal", {}) or {}
    members = []
    for member in _list(family.get("ops:world-patent-data", {}).get("ops:patent-family", {}).get("ops:family-member")):
        doc = next(i for i in _list(member["publication-reference"]["document-id"]) if i["@document-id-type"] == "docdb")
        events = [(e.get("ops:L007EP", {}).get("$", ""), e["@code"].strip(), e["@desc"]) for e in _list(member.get("ops:legal"))]
        members.append({"number": f"{doc['country']['$']}{doc['doc-number']['$']}{doc['kind']['$']}", "kind": doc["kind"]["$"],
                        "date": _day(doc["date"]["$"]), "events": sorted(events)})
    text = _get(f"published-data/publication/epodoc/{epodoc}/claims", {}) or {}
    claims = text.get("ops:world-patent-data", {}).get("ftxt:fulltext-documents", {}).get("ftxt:fulltext-document", {}).get("claims")
    return {"number": epodoc, "members": sorted(members, key=lambda m: m["date"]),
            "claims": "\n".join(c["$"] for claim in _list(claims)[:1] for c in _list(claim["claim"]["claim-text"]))}
