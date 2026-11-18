# Innovation agents

Specialist Claude agents that analyse invention disclosures. Built on the Claude Agent SDK, which runs Claude Code under the hood, so it runs on your Claude Pro/Max subscription.

## What's in this folder

Everything for the project lives here:

| Path | What it is |
|---|---|
| `app.py`, `ui.html` | The web app: drop a disclosure, read the reports, chat |
| `run.py` | Runs the agents (also from the command line) and checks the subscription login |
| `tools.py` | Free data tools the agents use |
| `agents/` | One file per agent |
| `disclosures/` | Input disclosures |
| `outputs/` | One folder per run with the reports |
| `docs/` | The project brief, plus notes on [data sources](docs/data-sources.md), [confidentiality](docs/confidentiality.md) and [meeting requests](docs/meeting-requests.md) |
| `firewall/` | Prototype: research the field from keywords only, so the disclosure stays in a secure zone ([how it works](firewall/README.md)) |
| `terminal.py`, `terminal.html` | The market terminal (see below) |
| `library.py`, `sectors.json`, `library/` | The sector knowledge library behind the terminal |
| `patents.py`, `epo.py` | The patent database and the European Patent Office client |
| `research.py` | The Research tab: earlier Aalto papers checked for missed commercial opportunities |
| `profiles.py` | Company and person profiles, built on the first click and stored |
| `CLAUDE.md` | Project notes that Claude Code reads when it works in this folder |
| `.claude/launch.json` | Starts the app in Claude's browser pane |
| `.venv/` | The Python environment |

## Market terminal

A dashboard of market knowledge for the sectors behind Aalto's main research areas. Start it with:

```bash
.venv/bin/python terminal.py
```

Then open http://127.0.0.1:8001. It runs next to the disclosure app (port 8000), so both can be open at once.

- **Tabs:**
  - Overview: all sectors with their headline.
  - Sector: one sector in detail, with key metrics, signals, open funding calls, companies, Aalto links, patents, the full memory file and a list of every source.
  - Companies and Patents across all sectors.
  - Research: earlier Aalto papers checked for missed opportunities, meaning research that someone else has since turned into patents or a business while Aalto did not. How it works:
    - **Papers** come from ACRIS, Aalto's research portal, through Aalto's API gateway (the "Research API Public" product at https://3scale.apps.ocp4.aalto.fi). Put the application's user key in `.env` as `ACRIS_API_KEY=...` and restart the terminal. It keeps English journal and conference papers from 2012 to 2021 (the patents are in English, so other languages would match falsely) with at most 25 authors (`YEARS` and `MAX_AUTHORS` in `research.py`), with their department and Scopus citation count. The list loads in about 15 minutes; each abstract is a separate request, so all of them take a few hours, and papers appear in the tab as their abstracts arrive. Papers without an abstract are left out.
    - **Screening** (code only, on this computer, no Claude usage): each paper is compared with the stored patents. It counts how much of the paper's distinctive wording the closest patents share (a patent sharing 30% or more counts as close, `CLOSE` in `research.py`), how many companies own close patents, and whether one of the paper's authors is an inventor on a close patent or the patent is Aalto's. Papers are re-screened weekly as the patent store grows. Word overlap misses the same idea written in different words, so the screening only ranks papers for a closer look.
    - **In-depth analysis** (Sonnet), only when you ask: open a paper and press Analyse. It is shown at the top of the paper, above the abstract and the screening. The agent does not rely on the local store: it searches online, in several wordings, for patents worldwide (EPO and Google Patents), later research on the same idea, and companies anywhere selling the same thing with evidence of their success. It checks whether the closest patents were granted, and checks whether Aalto or the authors patented, licensed or spun it out. It gives a verdict (Missed opportunity, Partly missed, Followed up by Aalto or the authors, or No commercial use found), the evidence with links, and what Aalto could still do now.
    - Filters: Verdict, Closest patent overlap, Patented by the authors, Companies on close patents, Department and Year.
  - **Profiles:** click a company or person named in the chat (and companies listed on a research paper) to open a profile in the middle. A company profile shows what they do and are building, founding year, location, size and funding, and the key people with their photos and most impressive past work. A person profile shows their photo, current roles and earlier work. A profile is built by a Sonnet agent from public sources the first time someone opens it (about a minute) and stored in `library/profiles.db`, so it opens at once after that; Update builds it again. Photos come from public pages and fall back to initials.
  - Similar: describe a piece of research or paste an abstract, and see the closest stored patents (best match first), who files most in that area, in which years, and in which CPC classes. It searches the patent database on this computer, so nothing you type is sent anywhere. It ranks by shared words, with rare words counting most, and covers only the stored EP and WO patents, so it is a first look, not a full prior art search. **Summarise** asks Sonnet for a short summary of the topic: what it covers, who patents it and how activity has changed, based on the closest stored patents. This sends the text to Claude, so use it only for public topics. For a worldwide search, ask the chat, which uses the EPO directly.
  - The Companies tab lists every applicant in the patent database, together with the 6 to 12 companies the sector agent profiles for each sector, so it grows as the patent backfill runs. A profiled company is matched to its applicant name (for example Oura and OURA HEALTH OY) and keeps its description and link. Other applicants link to their patents on Espacenet.
    - Filters: Sector, Source (profiled or patent applicant only), Organisation type (company, university or research, person or other), Country, Finnish, Aalto connection (co-applicant on Aalto patents, or Aalto mentioned), Patents stored and Latest patent year. Plus search within results and four sort orders, with Most patents first by default. Private persons who file patents are hidden to start with; remove the "NOT Organisation type: Person or other" chip to see them.
    - Click a patent count to open the Patents tab filtered to that applicant.
    - Organisation type is guessed from the applicant name, and applicant names are kept as the EPO writes them, so one company can appear under a few spellings (NOKIA TECHNOLOGIES OY and NOKIA TECH OY).
  - The Patents tab filters every stored patent the way Patsnap does:
    - a facet sidebar: Sector, Aalto, Authority, Patent type, Publication year, Applicant, Applicant country, Inventor, CPC classification (choose the level: section, class, subclass or group) and Added to store;
    - each facet shows its values with counts and a More link, and long facets have their own search box;
    - tick values and press Refine to keep only those, or Exclude to remove them. Values in one facet combine with "or", and different facets combine with "and";
    - active filters show as chips above the results (red for exclusions) with Clear all, plus search within results and five sort orders, including first filing date.

    Each sector's patents panel links to the tab with that sector already selected. Legal status, citation counts and patent value are not in the filters, because they need extra EPO calls per patent.
- **Breaking news** below the tabs rotates through the newest signals from all sectors.
- **Funding calls are checked:** after each sector update, every EU call is looked up on the EU portal, which gives the real deadline and budget. Calls that have closed are dropped, and a call disappears from the page once its deadline passes.
- **News** from earlier updates stays in each sector's list for 90 days (`KEEP_NEWS_DAYS` in `library.py`).
- **Sources:** every figure, news item, call and company links to its source, and the memory files cite their sources inline. The Sources panel lists every link behind a sector.
- **Chat** (right side, toggle with the Chat button):
  - Ask about any sector; it reads the library, can check facts with web search and the data tools, and always gives source links. Follow-up questions keep the context. New chat starts over.
  - Ask for a new sector dataset (for example "Add a sector on space technology"). The chat agrees the scope with you, adds it to `sectors.json` and starts building it.
  - It can only read `library/`. It cannot change other files.
- **Patents** come from the European Patent Office (OPS). Put your EPO keys in a `.env` file in this folder:
  ```
  EPO_KEY=your consumer key
  EPO_SECRET=your consumer secret
  ```
  The terminal then builds a patent database, `library/patents.db` (SQLite), with every EP and WO patent in each sector's field, not just a sample:
  - **New patents:** every 6 hours it pulls everything published since the last pull, with a week of overlap for late indexing.
  - **Older patents:** it keeps filling in the past, one week at a time, until 5 years are covered (`BACKFILL_MONTHS` in `patents.py`). Rounds run a minute apart while older weeks are missing, then once an hour. Each sector's panel shows how far back its patents go.
  - **Aalto's patents** in each field are pulled in full every time.
  - **EPO allowance:** the backfill pauses when this week's EPO usage reaches 3,000 MB of the free 4,000 MB (`WEEKLY_BUDGET_MB`) and carries on after the weekly reset, so new patents and chat searches always have room. Searches are spaced 12 seconds apart to stay under EPO's busy-time limit.
  - **What is stored for each patent:** number, patent family, publication date, first filing (priority) date, applicants, inventors, every CPC class and the full abstract (in the original language when there is no English one). An invention published as both EP and WO shows and counts once.
  - **Sector classes:** each sector's `patent_query` in `sectors.json` lists the CPC classes that match its scope (for example energy: batteries, grids, electrolysis, wind, solar, district heating and heat storage). When you change a query, that sector is pulled again from today backwards.
  - **Size:** the eight sectors publish about 150,000 EP and WO patents a year, so 5 years is about 750,000 patents. That is roughly 25 hours of pulling spread over 2 to 3 weeks, because of the weekly EPO budget, and 2 to 3 GB on disk.
  - **Granted or not:** the EPO search returns applications only, so the store does not show whether a patent was granted. The `epo_patent` tool (used by the chat and the IP agent) looks that up for one patent: its family, grant, legal events and claims.
  - The Patents tab searches a copy built for speed (`library/patent_search.db`): one row per invention plus small indexed tables for applicants, inventors, classes and sectors. It is rebuilt every hour from the patent store, so new patents show up within the hour. The list appears at once and the filter counts follow within a second or two. Patent pulls use no Claude allowance. To run one round from the command line: `.venv/bin/python patents.py`.

  How fresh the data is: the EPO database had last week's publications on 10 November 2026 (EP applications are published on Wednesdays, WO applications on Thursdays). Patent applications are usually published about 18 months after they are filed, so the newest patents show inventions from about a year and a half ago. The chat and the sector agent can search EPO too. How OPS works, its query language and its limits are in [docs/epo-ops.md](docs/epo-ops.md).

**The library** is one folder per sector in `library/<sector>/`, plus the shared patent database `library/patents.db`:
- `memory.md`: the knowledge file.
- `data.json`: the figures shown in the terminal.
- `history/`: a dated copy of every update.

Each update starts from the previous memory, so knowledge builds up instead of being rewritten. While the terminal runs, it updates every sector older than 3 days, one at a time, checking once an hour. **Refresh** on a sector updates it now.

You can also update from the command line:

```bash
.venv/bin/python library.py              # all sectors older than 3 days
.venv/bin/python library.py energy       # one sector now
```

**Sectors** are in [sectors.json](sectors.json): eight sectors mapped to Aalto's key research areas (digitalisation and AI, energy, materials, health, living environments, art and design). Add, remove or edit entries there; the terminal picks them up on restart.

**Model:** every agent in the project (the sector updates, the research checks, the chats and the disclosure agents) runs on Claude Sonnet 5.5, which uses less of your allowance than Opus. It is set once as `MODEL` in `run.py`, and an agent file can name another model in its header.

**Usage:** one sector update took about 2 minutes of research and uses a fair share of your Claude Pro allowance. Eight sectors every 3 days adds up, so lower the number of sectors or raise `MAX_AGE_DAYS` in `library.py` if you hit your limits. The library uses only public information, so the confidentiality rules for disclosures don't apply to it.

## Subscription only

The script cannot be billed per token. Before any agent runs it asks Claude Code how it is signed in, and it stops unless the answer is your claude.ai subscription. An API key, a token, a cloud account (Bedrock, Vertex, Foundry) or a Console login all stop the run before anything is sent.

One setting is outside the script's control: **extra usage** on your Claude plan, which bills you for use beyond your plan's limits. Keep it turned off in your claude.ai settings. With it off, an agent that hits the limit stops with a usage-limit error (shown in `run_info.txt`) and you can run it again once your usage resets.

## Setup (once)

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
claude auth login        # sign in with your Claude subscription account
```

If the `claude` command is missing, install Claude Code first (https://code.claude.com).

## Use the app

From inside this folder (`cd ~/Desktop/"AI Project"`):

```bash
.venv/bin/python app.py
```

Then open http://127.0.0.1:8000 in your browser. Stop it with Ctrl+C.

1. **Drop an invention disclosure** anywhere on the page, or click **New analysis**. PDF, text, Markdown and images work; save Word files as PDF first. The file is saved in `disclosures/` and all agents start on it.
2. **Watch the progress.** The Progress tab shows each agent working. Each report gets its own tab as soon as it is ready, so you can start reading while the rest run.
3. **Read the results.** When everything is done the page opens the **Overview**: a one-page verdict, key findings, risks, next steps and questions for the researchers, written from all the other reports. The full reports are in the other tabs.
4. **Ask the assistant** on the right. It knows the selected run, can answer questions, check facts with web search and the data tools, and edit the reports. When it edits a report, that report opens so you can see the change.

The left column lists every run, newest first, including runs started from the command line. The assistant can only change files in the selected run's folder. Claude Code blocks anything else, not just the instructions. Each run keeps its own conversation until you click New chat or stop the app. The page is only reachable from your own computer, and like `run.py` it only runs on your subscription login. If you close the app during a run, that run stops and is shown as stopped.

The server is in [app.py](app.py) and the page in [ui.html](ui.html).

## Run from the command line

```bash
.venv/bin/python run.py disclosures/example.md                  # all agents
.venv/bin/python run.py disclosures/example.md -a market nabc   # chosen agents
.venv/bin/python run.py disclosure.pdf competitor_data.csv      # extra input files
```

Each run gets its own folder in `outputs/`, named by start time and disclosure, for example `outputs/2026-10-24_10-37-12_example/`. It holds one report per agent (`overview.md`, `market.md`, `ip.md`, ...) and a `run_info.txt` with the input files and each agent's status: waiting, running, saved (with how long it took) or failed (with the reason).

## Add an agent

Create a new file in `agents/`, for example `agents/planning.md`. The file name is the agent name and the text is its instructions. An optional header sets tools, model and effort:

```
---
tools: WebSearch, WebFetch
model: sonnet
effort: high
---
You are a planning advisor at Aalto Innovation...
```

Every agent can read the input files. Leave out `tools` for an agent that only works from the inputs. Without `model` the agent uses your account's default model.

Agents run at the same time. An agent with `after: reports` in its header waits until the others are done and also gets their reports as input. [agents/overview.md](agents/overview.md) works this way.

## Data tools

[tools.py](tools.py) connects free data sources. Only the two EPO tools need a key (free, in `.env`). To give an agent a tool, add the tool's name to the agent's `tools:` line.

| Tool | Source | What it returns |
|---|---|---|
| `google_patent` | Google Patents | One patent in full: owner, dates, legal status, countries, CPC classes, claims, and cited, citing and similar patents |
| `epo_patents` | European Patent Office | Worldwide patent search with CQL: number, dates, applicants, classes, abstract |
| `epo_patent` | European Patent Office | One patent: its family, whether it was granted, the latest legal events and the claims |
| `search_papers` | OpenAlex | The 10 best-matching papers: title, year, citations, authors, institutions, funders, abstract |
| `research_trend` | OpenAlex | How active a topic is: papers per year, the most active institutions, and Aalto's own papers |
| `eu_funding_calls` | EU Funding & Tenders Portal | Open and upcoming EU calls with opening dates and deadlines |
| `eu_call_details` | EU Funding & Tenders Portal | One call in full: expected outcomes, scope, budget, conditions |
| `finnish_companies` | PRH / YTJ trade register | Finnish companies by name, industry code or city |
| `eurostat_search` | Eurostat | Dataset codes matching some words |
| `eurostat_data` | Eurostat | The numbers from one dataset, including production per product (PRODCOM) and EU trade per product |
| `page_images` | Any web page | The pictures on a page with their alt text, used by the profiles to find photos and logos |
| `research_projects` | OpenAIRE | Funded research projects (EU, Research Council of Finland and others): funder, dates, amount, summary |

Which agent has what:
- `ip`: EPO patent search and lookup, Google Patents pages, papers, research trend, research projects
- `market`: Eurostat (with production and trade per product), Finnish companies
- `funding`: EU calls, research projects
- `nabc`: works from the disclosure only
- `overview`: works from the disclosure and the other reports

All agents except `nabc` and `overview` also have web search.

Agents search patents at the European Patent Office with `epo_patents` and check a patent's status with `epo_patent`. `google_patent` adds what the EPO service lacks: the patents that cite a patent and similar ones. Google Patents has no free search API and its rules forbid automated searching, so it is only used to read single patent pages. OpenAlex works without a key on a small shared daily allowance. For more, get a free key at openalex.org and set it as `OPENALEX_API_KEY`.

To add a data source, write a function in `tools.py` like the others and add it to `TOOLS` at the bottom.

## Use from other code

```python
import asyncio
from run import run_agent

report = asyncio.run(run_agent("nabc", ["disclosures/example.md"]))
```

`run_agent` returns the report text, so the output of one agent can be saved and passed as an input file to another.

## Notes

- Subscription login is for your own use on your own machine, not for a tool that other people use.
- Invention disclosures are confidential. On personal Claude plans, check the "Help improve Claude" privacy setting at claude.ai, and test with fictional disclosures such as `disclosures/example.md`.
