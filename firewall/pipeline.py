"""Keyword firewall: research an invention without sending the invention to outside services.

1. Secure zone: a model you control reads the disclosure and writes a public brief (field, problem,
   search keywords, patent classes) and a private list of secret terms.
2. Review: you check the brief, and can edit it, before anything leaves.
3. Research zone: cloud agents with web search and the data tools research the field using only the brief.
   They never see the disclosure. Every outside request they make is logged and checked for secret terms.
4. Secure zone: the model compares their findings with the disclosure and writes the assessment.

For now the secure-zone model is a stand-in: Claude on your subscription, with no tools. So the
disclosure still goes to Anthropic in steps 1 and 4: use fictional or public disclosures only.

Usage:  .venv/bin/python firewall/pipeline.py disclosures/test-leak-detector.pdf
"""

import argparse
import asyncio
import json
import re
import sys
import unicodedata
from datetime import datetime
from pathlib import Path

from claude_agent_sdk import AssistantMessage, ResultMessage, ToolUseBlock, query
from pypdf import PdfReader

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))  # use run.py and tools.py from the project folder
from run import agent_options, check_subscription  # noqa: E402  (importing run also enforces subscription-only)

RUNS_DIR = HERE / "runs"
RESEARCH_AGENTS = ["patents", "market", "funding"]  # files in firewall/agents/

BRIEF_FIELDS = ["field", "problem", "product_type", "applications", "customer_types", "search_keywords", "patent_classes"]
BRIEF_SCHEMA = {
    "type": "object",
    "properties": {
        "field": {"type": "string"},
        "problem": {"type": "string"},
        "product_type": {"type": "string"},
        **{name: {"type": "array", "items": {"type": "string"}} for name in BRIEF_FIELDS[3:] + ["secret_terms"]},
    },
    "required": BRIEF_FIELDS + ["secret_terms"],
    "additionalProperties": False,
}

EXTRACT_PROMPT = """You work in the secure zone of an innovation office. You read a confidential invention \
disclosure and decide what may leave the secure zone.

Outside research agents will search the web, patent databases and funding portals using only your public brief. \
Treat everything in the public brief as public: search engines and other companies may see it.

Rules for the public brief (field, problem, product_type, applications, customer_types, search_keywords, patent_classes):
- Describe the field, the problem and the kind of product only as far as an outsider could guess from a one-line \
description of the research area.
- Never describe how the invention works or what is new about it. Never include results, numbers, names of people, \
the organisation, partners, places or dates.
- search_keywords: 6 to 12 short search phrases about the field, the problem, existing solutions, competing product \
types and customer types. Choose phrases that also fit many existing products. Never use the inventive step, or a \
mix of features that points to it.
- patent_classes: 2 to 5 CPC classes for the field, not for the inventive step.
- When in doubt, be broader. The outside agents only map the field; the exact comparison with the invention happens \
later, inside the secure zone.

secret_terms: every word or phrase that must never leave: the inventive step and its key features, distinctive \
technical terms, numbers and results, names of people, the organisation and partners, and plans and dates. \
Add the short variants that a search might contain."""

RESEARCH_TASK = """Below is the public brief of an invention. The invention itself is confidential and you will \
not see it; you only know the field it belongs to.

{brief}

Map the landscape around this field. Reply with your finished report in Markdown as your final message."""

ASSESS_PROMPT = """You work in the secure zone of Aalto Innovation, the unit that helps commercialise Aalto \
University research. You get a confidential invention disclosure and reports on patents, the market and funding \
that outside agents wrote. The outside agents never saw the invention. They only knew its field, so their reports \
map the field. Your job is to compare the invention with what they found.

Write an assessment in Markdown with these sections:
1. Verdict: two or three sentences.
2. Novelty: the closest patents and papers in the reports, which features of the invention they already show, and \
which features look new. Say that the outside search covered the field, not the invention's own features, so a \
confidential professional patent search is still needed.
3. Market fit: how the invention fits the customers, competitors and market figures in the market report.
4. Funding fit: the best options from the funding report, with deadlines.
5. Risks and next steps.
6. Questions for the researchers.

Use only the disclosure and the reports, and keep the links from the reports where they matter."""


def read_disclosure(path):
    """Read the disclosure as text, on this computer."""
    text = "\n".join(page.extract_text() or "" for page in PdfReader(path).pages) if path.suffix.lower() == ".pdf" else path.read_text()
    return unicodedata.normalize("NFKC", text)  # turns PDF ligatures such as "ﬁ" back into normal letters


async def secure_model(instructions, text, schema=None):
    """The secure zone. Stand-in for now: Claude on your subscription with no tools, so it only sees the text
    it is given. Replace this with a model on hardware you control (for example in Aalto's SECDATA environment);
    nothing else in the pipeline has to change."""
    output_format = {"type": "json_schema", "schema": schema} if schema else None
    options = agent_options(instructions, [], disallowed_tools=["Read"], output_format=output_format)
    result = None
    async for message in query(prompt=text, options=options):
        if isinstance(message, ResultMessage):
            result = message
    if result is None or result.is_error:
        raise RuntimeError(result.errors or result.result if result else "no result")
    return result.structured_output if schema else result.result


def leak_check(brief, secret_terms, disclosure):
    """Local checks on the public brief before it leaves. Returns a list of problems for the reviewer."""
    text = json.dumps({k: v for k, v in brief.items() if k != "patent_classes"}, ensure_ascii=False).lower()

    def phrases(s):  # every run of 6 words
        words = re.findall(r"\w+", s.lower())
        return {" ".join(words[i:i + 6]) for i in range(len(words) - 5)}

    problems = [f"contains the secret term '{t}'" for t in secret_terms if t.lower() in text]
    problems += [f"contains the number '{n}'" for n in sorted(set(re.findall(r"\d+(?:[.,]\d+)?", text)))]
    problems += [f"copies the disclosure word for word: '{p}'" for p in sorted(phrases(disclosure) & phrases(text))]
    return problems


async def research(name, brief):
    """Run one research-zone agent on the public brief. Returns its report and every outside request it made."""
    _, header, instructions = (HERE / "agents" / f"{name}.md").read_text().split("---", 2)
    tools = [t.strip() for t in header.split("tools:", 1)[1].splitlines()[0].split(",")]
    options = agent_options(instructions.strip(), tools, disallowed_tools=["Read"])  # no file access at all
    prompt = RESEARCH_TASK.format(brief=json.dumps(brief, indent=2, ensure_ascii=False))
    report, requests = None, []
    async for message in query(prompt=prompt, options=options):
        if isinstance(message, AssistantMessage):
            requests += [f"{b.name.replace('mcp__data__', '')}: {json.dumps(b.input, ensure_ascii=False)}"
                         for b in message.content if isinstance(b, ToolUseBlock)]
        elif isinstance(message, ResultMessage) and not message.is_error:
            report = message.result
    if report is None:
        raise RuntimeError("no report")
    return report, requests


async def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("disclosure", type=Path)
    args = parser.parse_args()
    try:
        check_subscription()
    except RuntimeError as error:
        sys.exit(f"Stopped: {error}")
    disclosure = read_disclosure(args.disclosure)
    out = RUNS_DIR / f"{datetime.now():%Y-%m-%d_%H-%M-%S}_{args.disclosure.stem}"
    out.mkdir(parents=True)
    print(f"Saving to {out.relative_to(HERE.parent)}/")

    print("\n1/4 Secure zone: reading the disclosure and writing the public brief")
    result = await secure_model(EXTRACT_PROMPT, disclosure, BRIEF_SCHEMA)
    secret_terms = result.pop("secret_terms")
    (out / "secret_terms.json").write_text(json.dumps(secret_terms, indent=2, ensure_ascii=False))
    (out / "public_brief.json").write_text(json.dumps(result, indent=2, ensure_ascii=False))
    problems = leak_check(result, secret_terms, disclosure)
    (out / "leak_check.txt").write_text("\n".join(problems) or "No problems found.")

    print("\n2/4 Review. This public brief is all that will leave the secure zone:\n")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    print("\nLeak check: " + ("no problems found." if not problems else "\n  - " + "\n  - ".join(problems)))
    answer = input(f"\nYou can edit {(out / 'public_brief.json').relative_to(HERE.parent)} now. "
                   "Press Enter to send it to the research agents, or type n to stop: ")
    if answer.strip().lower().startswith("n"):
        sys.exit("Stopped. Nothing was sent outside the secure zone.")
    brief = json.loads((out / "public_brief.json").read_text())  # includes any edits

    print("\n3/4 Research zone: agents research the field using only the public brief")
    results = await asyncio.gather(*(research(name, brief) for name in RESEARCH_AGENTS), return_exceptions=True)
    reports, sent = {}, []
    for name, outcome in zip(RESEARCH_AGENTS, results):
        if isinstance(outcome, Exception):
            print(f"  [{name}] failed: {outcome}")
            continue
        reports[name], requests = outcome
        (out / f"{name}.md").write_text(reports[name])
        sent += [f"- {name} | {request}" for request in requests]
        print(f"  [{name}] done, {len(requests)} outside requests")
    leaks = [line for line in sent if any(term.lower() in line.lower() for term in secret_terms)]
    (out / "outbound_log.md").write_text(
        f"# Requests sent outside the secure zone\n\n{len(sent)} requests, {len(leaks)} containing a secret term.\n"
        + ("\n## Containing a secret term\n\n" + "\n".join(leaks) + "\n" if leaks else "")
        + "\n## All requests\n\n" + "\n".join(sent) + "\n"
    )
    print(f"  Outside requests: {len(sent)}, containing a secret term: {len(leaks)} (see outbound_log.md)")
    if not reports:
        sys.exit("No research reports, so there is nothing to assess.")

    print("\n4/4 Secure zone: comparing the findings with the disclosure")
    material = f"# Confidential invention disclosure\n\n{disclosure}\n\n" + "\n\n".join(
        f"# Research report: {name}\n\n{report}" for name, report in reports.items())
    (out / "assessment.md").write_text(await secure_model(ASSESS_PROMPT, material))
    print(f"\nDone. Read {(out / 'assessment.md').relative_to(HERE.parent)}")


if __name__ == "__main__":
    asyncio.run(main())
