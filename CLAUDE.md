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

## Testing

Run tests from a clean environment, because the Claude desktop app's shell carries its own auth variables:

```bash
env -i HOME="$HOME" USER="$USER" PATH="/usr/bin:/bin:/usr/sbin:/sbin" .venv/bin/python run.py disclosures/example.md -a nabc
```

`.claude/launch.json` starts the app the same way for the browser pane. A full run of all agents takes a few minutes and uses subscription usage. Before testing chat edits on a real run folder, back that folder up and restore it afterwards.
