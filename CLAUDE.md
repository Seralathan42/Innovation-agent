# Innovation agents: project notes

Aalto course project TU-E700002 (Future Interfaces Project: AI agents and the real world) with Aalto Innovation. Goal: an advisory platform where AI agents analyse invention disclosures (market, technology and IP, funding, NABC) so advisors spend less time on background research. The brief is [docs/Aalto Innovations brief.pdf](docs/Aalto%20Innovations%20brief.pdf).

## Rules from the user

- **Everything for this project lives in this folder.** Put new files, notes, test data and config here, not in other folders.
- **Subscription only, never per-token billing.** `run.py` strips API key, token and base-URL variables and stops unless the CLI's `auth status` says `claude.ai`. Never add an API-key path or instructions for one.
- **Python, and keep the code lean:** no code that isn't needed.
- **Plain language and no em dashes** in replies, docs and reports.
- **Use only fictional or public disclosures.** Aalto's AI rules treat patent-sensitive information as Secret, so it must not go into common AI tools. See [docs/confidentiality.md](docs/confidentiality.md).

## How it fits together

- `run.py`: subscription check, `MODEL` (Sonnet 5.5, used by every agent unless its file names another), `agent_options()` (the tools allowed for each agent), `start_run()` (runs the agents and keeps `run_info.txt` up to date), and the command line.
- `agents/*.md`: one agent per file. The header holds `tools`, `model`, `effort`, `after: reports` for agents that run last on the other reports, and `output: check` for the checker (`check`). Report agents return Markdown plus a 1 to 5 score (saved in `scores.json`); the checker saves `check.json`.
- `tools.py`: free data tools served to agents through an in-process MCP server: EPO patent search and single-patent lookup (family, grant, legal events, claims), Google Patents pages, OpenAlex (papers and research trend), EU Funding & Tenders, PRH, Eurostat (with PRODCOM and trade per product), OpenAIRE (Graph API v3), and `stored_patents` / `stored_companies`, which search our own databases on this computer. Background in [docs/data-sources.md](docs/data-sources.md).
- `app.py` and `ui.html`: the local web app at http://127.0.0.1:8000. Drop a disclosure to start a run, watch progress, read the reports, and chat. The chat may only edit `outputs/<run>/**`, enforced by the rule `Edit(./outputs/<run>/**)`.
- `outputs/<date>_<time>_<disclosure>/`: one folder per run, holding the reports and `run_info.txt`.
- `disclosures/`: input files. Files dropped on the page are saved here.
- **Main focus since 2026-11-05: the market terminal.**
  - `terminal.py` and `terminal.html` (port 8001): a terminal-style dashboard with tabs (Brief, Sectors, Sector, Companies, Patents, Similar patents, Past research), breaking news, sector panels, a sources panel, and a chat that reads only `library/` (plus the open brief and its disclosure) and can add sectors with its `add_sector` tool. Brief drops a disclosure into `start_run()` with the four report agents and the checker; the runs are the `outputs/` folders.
  - `epo.py`: European Patent Office OPS client (OAuth token, CQL search, 12 s between searches, weekly usage from the reply headers). Keys `EPO_KEY` and `EPO_SECRET` live in `.env` (gitignored). `tools.py` has an `epo_patents` tool. Details in `docs/epo-ops.md`.
  - `patents.py`: the patent database `library/patents.db` (SQLite) with every EP and WO patent in each sector's field. A daemon thread in the terminal pulls new publications every 6 hours and backfills older weeks until 5 years are covered, pausing at 3,000 MB of EPO usage a week. Each patent keeps its family, priority date, all CPC classes and full abstract; one family (EP plus WO) counts once. A sector whose `patent_query` changes is pulled again. `build_search()` rebuilds `library/patent_search.db` every hour (one row per family plus indexed side tables `f_sector`, `f_applicant`, `f_inventor`, `f_class` and the full-text table `fam_text`, swapped in with `os.replace`), and `search()` filters it for the Patents tab, with `part` letting the page load the list before the counts; and `similar()` ranks stored patents against a description with SQLite full-text search (the Similar tab; nothing leaves the computer). `build_companies()` rebuilds a companies table (every applicant, merged with the companies in each sector's `data.json`) after each round, and `company_search()` filters it for the Companies tab.
  - `research.py`: the Research tab. Fetches Aalto papers (2012 to 2021) from ACRIS through Aalto's API gateway, `research.api.aalto.fi/api/acris/v1` ("Research API Public"; key `ACRIS_API_KEY` in `.env`, sent as the `USER-KEY` header), into `library/research.db`; screens each against `patents.db` in code (distinctive-word overlap, company owners, authors as inventors); and `analyse()`, only when the user asks, runs a Sonnet agent with structured output for a verdict on whether Aalto missed a commercial opportunity. Papers come only from ACRIS, by the user's choice.
  - `profiles.py`: company and person profiles. The chat writes names as `#company/Name` or `#person/Name` links; clicking one opens a profile in the middle. A Sonnet agent builds it on the first click from public web sources (structured output with key people, photos as image links, past work) and it is stored in `library/profiles.db`.
  - `library.py`: a sector analyst agent with structured output keeps `library/<sector>/memory.md`, `data.json` and `history/` up to date, building on the previous memory each time. News from earlier updates is kept for 90 days, and figures should come mainly from official sources.
  - Sectors are in `sectors.json`, mapped to Aalto's key research areas. Stale sectors (older than 3 days) update in the background while the terminal runs.
- `demo/`: the presentation video [demo/knowledge-hub-demo.mp4](demo/knowledge-hub-demo.mp4). `record.py` films each scene in headless Chrome against the running terminal (clips in `demo/clips/`, gitignored), and `sound.py` adds our own music and interface sounds timed to the on-screen events. Script and timings in [docs/demo-script.md](docs/demo-script.md).
- `firewall/`: standalone prototype of the keyword firewall, not yet merged into the app. A secure-zone model turns the disclosure into a public brief plus secret terms; after human review, cloud research agents work only from the brief, with no file access; then the secure zone compares their findings with the disclosure. `secure_model()` in `firewall/pipeline.py` is a Claude stand-in for a future local model. See [firewall/README.md](firewall/README.md).

## Testing

Run tests from a clean environment, because the Claude desktop app's shell carries its own auth variables:

```bash
env -i HOME="$HOME" USER="$USER" PATH="/usr/bin:/bin:/usr/sbin:/sbin" .venv/bin/python run.py disclosures/example.md -a nabc
```

`.claude/launch.json` starts the app the same way for the browser pane. A full run of all agents takes a few minutes and uses subscription usage. Before testing chat edits on a real run folder, back that folder up and restore it afterwards.
