"""Combine the agents' sub-scores into one weighted score and compare it with the independent verifier.

Weights, bands and the tolerance are in scoring.json, so advisors can change them without touching code.
"""

import json
from pathlib import Path

CONFIG = json.loads((Path(__file__).parent / "scoring.json").read_text())
MARGIN = {"low": 1.0, "medium": 0.5, "high": 0.0}  # how many points off a sub-score may be, by confidence


def load(out_dir, name):
    path = Path(out_dir) / f"{name}.json"
    return json.loads(path.read_text()) if path.exists() else []


def to_percent(mean):  # a 1 to 5 average as 0 to 100
    return (mean - 1) / 4 * 100


def build(out_dir):
    """Return the Markdown for score.md. Raises ValueError when no agent gave a scorecard."""
    out_dir = Path(out_dir)
    rows = []  # agent, criterion, score, confidence, evidence, weight
    for path in sorted(out_dir.glob("*.scores.json")):
        for criterion, card in json.loads(path.read_text()).items():
            try:
                score = min(5.0, max(1.0, float(card["score"])))
                confidence = card.get("confidence", "medium").lower()
                rows.append((path.name.split(".")[0], criterion, score, confidence if confidence in MARGIN else "medium",
                             card.get("evidence", ""), CONFIG["weights"][criterion]))
            except (KeyError, TypeError, ValueError, AttributeError):
                continue  # malformed or unknown criterion
    if not rows:
        raise ValueError("no scorecards")

    total = sum(r[5] for r in rows)

    def structured(shift):  # weighted average, with every score moved by its margin (shift is -1, 0 or +1)
        return to_percent(sum(w * min(5, max(1, s + shift * MARGIN[c])) for _, _, s, c, _, w in rows) / total)

    opinions = [min(100.0, max(0.0, float(o["score"]))) for o in load(out_dir, "scorer") if "score" in o]
    w = CONFIG["opinion_weight"] if opinions else 0

    def blend(sub, opinion):
        return (1 - w) * sub + w * opinion

    final = blend(structured(0), sum(opinions) / len(opinions) if opinions else 0)
    low = blend(structured(-1), min(opinions) if opinions else 0)
    high = blend(structured(1), max(opinions) if opinions else 0)
    band = "Pursue" if final >= CONFIG["bands"]["pursue"] else "Pass" if final < CONFIG["bands"]["pass"] else "Needs more information"

    lines = [f"# Score: {final:.0f} / 100", "",
             f"**{band}.** Likely range {low:.0f} to {high:.0f}, based on how confident the agents were.", "",
             "## Sub-scores", "", "| Criterion | Agent | Score (1 to 5) | Confidence | Weight | Evidence |", "|---|---|---|---|---|---|"]
    for agent, criterion, s, c, evidence, weight in sorted(rows, key=lambda r: -r[5]):
        lines.append(f"| {criterion.replace('_', ' ')} | {agent} | {s:g} | {c} | {weight / total:.0%} | {evidence.replace('|', '/')} |")
    missing = [c for c in CONFIG["weights"] if c not in {r[1] for r in rows}]
    if missing:
        lines += ["", f"No score for: {', '.join(m.replace('_', ' ') for m in missing)}. The weights of the others were scaled up."]

    lines += ["", "## Scorer's overall opinion", ""]
    if opinions:
        lines.append(f"Independent holistic scores from {len(opinions)} runs: {', '.join(f'{o:.0f}' for o in opinions)}. "
                     f"It counts for {w:.0%} of the final score.")
        for o in load(out_dir, "scorer")[:1]:
            lines += ["", *[f"- {reason}" for reason in o.get("reasons", [])]]
    else:
        lines.append("Not available.")

    lines += ["", "## Verification", ""]
    verifier = (load(out_dir, "verifier") or [None])[0]
    if verifier and "score" in verifier:
        gap = abs(float(verifier["score"]) - final)
        if gap <= CONFIG["verifier_tolerance"]:
            lines.append(f"**Verified.** The verifier scored the invention {float(verifier['score']):.0f} on its own, "
                         f"{gap:.0f} points from the final score.")
        else:
            lines.append(f"**Disputed.** The verifier scored the invention {float(verifier['score']):.0f} on its own, "
                         f"{gap:.0f} points from the final score. Treat the score as uncertain and read the issues below.")
        lines += ["", verifier.get("summary", "")]
        for issue in verifier.get("issues", []):
            lines.append(f"- **{issue.get('criterion', '?')}**: {issue.get('problem', '')} (suggested score: {issue.get('suggested_score', '?')})")
    else:
        lines.append("Not verified: the verifier did not finish.")

    lines += ["", "## How this is calculated", "",
              "Each agent scores its own criteria from 1 to 5. The score is the weighted average of those, turned into 0 to 100, "
              f"then blended with the scorer's overall opinion ({w:.0%}). The verifier scores the same reports without seeing the "
              "final score. Weights and bands are in `scoring.json`. This is a structured opinion, not a validated prediction."]
    return "\n".join(lines) + "\n"
