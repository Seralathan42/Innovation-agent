# Free data sources

Research from 24 October 2026 into free substitutes for the paid tools Aalto Innovation uses: Patsnap, market data, company and ESG data, grant data and internal systems. "Tested" means a live request returned data without a key on that day.

## Connected to the agents (in tools.py)

| Tool | Source | What it gives | Access |
|---|---|---|---|
| `google_patent` | Google Patents patent pages | One patent: owner, inventors, dates, legal status, countries, CPC classes, timeline, abstract, claims, cited, citing and similar patents | No key. Google's rules allow `/patent/` pages but forbid automated search, so agents find patent numbers with web search |
| `search_papers` | OpenAlex | Papers: title, year, citations, authors, institutions, funders, abstract | No key: about 100 searches a day, shared per IP address. Free key (`OPENALEX_API_KEY`): about 1,000 |
| `eu_funding_calls`, `eu_call_details` | EU Funding & Tenders Portal | Open and upcoming EU calls; full call text, budget and deadlines | No key (public key "SEDIA"), tested. The portal's open/closed labels are unreliable, so the tool filters by deadline |
| `finnish_companies` | PRH / YTJ trade register | Finnish companies by name, industry code (TOL 2008) or city. No financial figures | No key, tested |
| `eurostat_search`, `eurostat_data` | Eurostat | Official EU statistics, such as the number of enterprises and turnover per industry. The detailed product-sales data (PRODCOM) is not in this API | No key, tested |
| `research_projects` | OpenAIRE | Funded projects from the EU, the Research Council of Finland (funder code AKA) and other funders, with amounts | No key: 60 requests an hour. Free token: 7,200. Tested |

## Free, not connected yet

| Source | What it gives | Access |
|---|---|---|
| EPO Open Patent Services | Worldwide patent data, legal status and families | Free key, 4 GB a week. The user chose not to use it |
| Google Patents on BigQuery | Patent full text with SQL | Free sandbox, 1 TB of queries a month. Full-text searches use that up quickly |
| USPTO Open Data Portal | US patents and applications | Free key, needs a USPTO.gov account (since June 2026) |
| Semantic Scholar | Papers and citations | Free key on request, 1 request a second |
| CORDIS | All EU-funded projects with partners and budgets | Free, needs an EU Login account. Bulk downloads need no account |
| UN Comtrade | Trade by country and product | Free key, 500 calls a day |
| Statistics Finland, OECD, World Bank | Official statistics | No key |
| SEC EDGAR | Financials of US-listed companies | No key |
| GLEIF | Legal entity IDs and ownership | No key, tested |
| Climate TRACE | Emissions per facility, with owner | Free, API in beta |
| Grants.gov | US federal grants | No key, tested |
| GDELT | Worldwide news events | No key |

## Gone, unclear or not free

- **PatentsView:** API paused on 20 March 2026. The data is now only available as bulk downloads on the USPTO Open Data Portal.
- **Lens.org:** API access needs an application, and free use could not be confirmed.
- **Crunchbase:** no real free API in 2026.
- **Google Trends:** the API is still in alpha, and you have to apply.
- **OpenCorporates:** free only on request, for academics, NGOs and journalists.
- **OpenSanctions:** free for non-commercial use only.
- **Business Finland funding data:** Excel export only, no API.
- **research.fi:** no documented public API found. OpenAIRE covers Research Council of Finland projects instead.
- **ESG ratings and startup deal data:** no free equivalent.

## Through Aalto's library

Aalto students can use **Statista**, **Orbis** (company financials and ownership) and **Zephyr** (deals and venture capital). These have no API, so export the data as CSV and pass it to `run.py` as an extra input file. The agents cannot read Excel files. The licences are for academic, non-commercial use.

## Internal systems (SSO, CRM, finance, documents)

The project cannot use Aalto's internal data, so these are mocked as local files, such as a CSV of past projects passed as an input file. Free stand-ins with APIs, if needed later:
- **SSO:** Keycloak
- **CRM:** HubSpot free CRM or Twenty
- **Finance:** Odoo Community or ERPNext
- **Documents:** Paperless-ngx or Nextcloud
