# Innovation agents: project notes

Aalto course project TU-E700002 (Future Interfaces Project: AI agents and the real world) with Aalto Innovation. Goal: an advisory platform where AI agents analyse invention disclosures (market, technology and IP, funding, NABC) so advisors spend less time on background research. The brief is [docs/Aalto Innovations brief.pdf](docs/Aalto%20Innovations%20brief.pdf).

## Rules from the user

- **Everything for this project lives in this folder.** Put new files, notes, test data and config here, not in other folders.
- **Subscription only, never per-token billing.** `run.py` strips API key, token and base-URL variables and stops unless the CLI's `auth status` says `claude.ai`. Never add an API-key path or instructions for one.
- **Python, and keep the code lean:** no code that isn't needed.
- **Plain language and no em dashes** in replies, docs and reports.
- **Use only fictional or public disclosures.** Aalto's AI rules treat patent-sensitive information as Secret, so it must not go into common AI tools. See [docs/confidentiality.md](docs/confidentiality.md).

## How it fits together

- `run.py`: subscription check, `agent_options()` (the tools allowed for each agent), `start_run()` (runs the agents and keeps `run_info.txt` up to date), and the command line.
- `agents/*.md`: one agent per file. The header holds `tools`, `model`, `effort`, and `after: reports` for agents that run last on the other reports (`overview`).
- `score.py` and `scoring.json`: combine each agent's scorecard (`<agent>.scores.json`) and the scorer's opinion (`scorer.json`) into `score.md`, and compare it with the blind `verifier.json`. Weights live in `scoring.json`.
- `tools.py`: free data tools served to agents through an in-process MCP server: Google Patents pages, OpenAlex, EU Funding & Tenders, PRH, Eurostat and OpenAIRE. Background in [docs/data-sources.md](docs/data-sources.md).
- `app.py` and `ui.html`: the local web app at http://127.0.0.1:8000. Drop a disclosure to start a run, watch progress, read the reports, and chat. The chat may only edit `outputs/<run>/**`, enforced by the rule `Edit(./outputs/<run>/**)`.
- `outputs/<date>_<time>_<disclosure>/`: one folder per run, holding the reports and `run_info.txt`.
- `disclosures/`: input files. Files dropped on the page are saved here.
- **Main focus since 2026-11-05: the market terminal.**
  - `terminal.py` and `terminal.html` (port 8001): a terminal-style dashboard with tabs (Overview, Sector, Companies, Patents), breaking news, sector panels, a sources panel, and a chat that reads only `library/` and can add sectors with its `add_sector` tool.
  - `epo.py`: European Patent Office OPS client (OAuth token, CQL search, 12 s between searches, weekly usage from the reply headers). Keys `EPO_KEY` and `EPO_SECRET` live in `.env` (gitignored). `tools.py` has an `epo_patents` tool. Details in `docs/epo-ops.md`.
  - `patents.py`: the patent database `library/patents.db` (SQLite) with every EP and WO patent in each sector's field. A daemon thread in the terminal pulls new publications every 6 hours and backfills older weeks until 5 years are covered, pausing at 3,000 MB of EPO usage a week. `search()` does the Patents tab's filtering and facet counts in SQL. `build_companies()` rebuilds a companies table (every applicant, merged with the companies in each sector's `data.json`) after each round, and `company_search()` filters it for the Companies tab.
  - `library.py`: a sector analyst agent with structured output keeps `library/<sector>/memory.md`, `data.json` and `history/` up to date, building on the previous memory each time.
  - Sectors are in `sectors.json`, mapped to Aalto's key research areas. Stale sectors (older than 3 days) update in the background while the terminal runs.
- `firewall/`: standalone prototype of the keyword firewall, not yet merged into the app. A secure-zone model turns the disclosure into a public brief plus secret terms; after human review, cloud research agents work only from the brief, with no file access; then the secure zone compares their findings with the disclosure. `secure_model()` in `firewall/pipeline.py` is a Claude stand-in for a future local model. See [firewall/README.md](firewall/README.md).

## Testing

Run tests from a clean environment, because the Claude desktop app's shell carries its own auth variables:

```bash
env -i HOME="$HOME" USER="$USER" PATH="/usr/bin:/bin:/usr/sbin:/sbin" .venv/bin/python run.py disclosures/example.md -a nabc
```

`.claude/launch.json` starts the app the same way for the browser pane. A full run of all agents takes a few minutes and uses subscription usage. Before testing chat edits on a real run folder, back that folder up and restore it afterwards.
