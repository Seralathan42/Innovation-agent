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
| `docs/` | The project brief, plus notes on [data sources](docs/data-sources.md) and [confidentiality](docs/confidentiality.md) |
| `CLAUDE.md` | Project notes that Claude Code reads when it works in this folder |
| `.claude/launch.json` | Starts the app in Claude's browser pane |
| `.venv/` | The Python environment |

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

## Scoring

Every run ends with a **Score** tab: one number from 0 to 100, a likely range, and a band (Pursue, Needs more information, Pass).

1. The `nabc`, `ip`, `market` and `funding` agents each end their report with a scorecard: 1 to 5 per criterion, with a confidence and one sentence of evidence. It is saved as `<agent>.scores.json`.
2. The `scorer` agent reads the reports and gives its own overall score from 0 to 100. It runs 3 times and the answers are averaged.
3. [score.py](score.py) takes the weighted average of the sub-scores and blends in the scorer's opinion. The weights, the blend (25%), the band limits and the verifier tolerance are in [scoring.json](scoring.json). Edit that file to change them.
4. The `verifier` agent (a different model, `opus`) scores the invention on its own from the reports and scorecards, without seeing the final score, and checks the evidence behind each sub-score with web search. If its score is more than 10 points from the final score, the Score tab says **Disputed**.

The result is a structured opinion, not a validated prediction. There are no past outcomes to learn weights from, so the weights are set by hand. If the `opus` model is not on your plan, change `model: opus` in `agents/verifier.md`.

## Add an agent

Create a new file in `agents/`, for example `agents/planning.md`. The file name is the agent name and the text is its instructions. An optional header sets tools, model and effort. `output: json`, `runs: 3` and `scorecards: yes` are used by the scoring agents:

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

[tools.py](tools.py) connects free data sources, and none of them needs an API key. To give an agent a tool, add the tool's name to the agent's `tools:` line.

| Tool | Source | What it returns |
|---|---|---|
| `google_patent` | Google Patents | One patent in full: owner, dates, legal status, countries, CPC classes, claims, and cited, citing and similar patents |
| `search_papers` | OpenAlex | The 10 best-matching papers: title, year, citations, authors, institutions, funders, abstract |
| `eu_funding_calls` | EU Funding & Tenders Portal | Open and upcoming EU calls with opening dates and deadlines |
| `eu_call_details` | EU Funding & Tenders Portal | One call in full: expected outcomes, scope, budget, conditions |
| `finnish_companies` | PRH / YTJ trade register | Finnish companies by name, industry code or city |
| `eurostat_search` | Eurostat | Dataset codes matching some words |
| `eurostat_data` | Eurostat | The numbers from one dataset |
| `research_projects` | OpenAIRE | Funded research projects (EU, Research Council of Finland and others): funder, dates, amount, summary |

Which agent has what:
- `ip`: patents, papers, research projects
- `market`: Eurostat, Finnish companies
- `funding`: EU calls, research projects
- `nabc`: works from the disclosure only
- `overview`: works from the disclosure and the other reports

All agents except `nabc` and `overview` also have web search.

Google Patents has no free search API, and its rules forbid automated searching, so agents find patents with web search and then read them with `google_patent`. OpenAlex works without a key on a small shared daily allowance. For more, get a free key at openalex.org and set it as `OPENALEX_API_KEY`.

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
