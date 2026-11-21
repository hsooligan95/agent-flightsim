"""Coverage-map and findings reports (Markdown, from run rows)."""
from __future__ import annotations

from .cases import USERS
from .engine import summarize_cells
from .world import DEPENDENCY, REDUNDANCY, STALENESS


def coverage_map(rows: list[dict]) -> str:
    cells = summarize_cells(rows)
    by_key = {(c["staleness"], c["dependency"], c["redundancy"], c["user"]): c
              for c in cells}
    lines = ["# AgentFlightSim — coverage map", ""]
    passed = sum(r["passed"] for r in rows)
    findings = [f for r in rows for f in r["findings"]]
    lines.append(f"{len(rows)} runs · scorer: {passed}/{len(rows)} passed · "
                 f"oracle findings: {len(findings)} "
                 f"({sum(1 for f in findings if f['class'] == 'stale_corpus_answered_as_current')} "
                 f"stale-as-current, "
                 f"{sum(1 for f in findings if f['class'] == 'answer_contradiction')} "
                 f"answer contradictions, "
                 f"{sum(1 for f in findings if f['class'] == 'sources_disagree')} "
                 f"source disagreements)")
    lines.append("")
    for redundancy in REDUNDANCY:
        lines.append(f"## Scorer pass rate — redundancy: {redundancy}")
        lines.append("")
        lines.append("| staleness | dependency | "
                     + " | ".join(USERS) + " |")
        lines.append("|---|---|---|---|---|")
        for staleness in STALENESS:
            for dependency in DEPENDENCY:
                vals = []
                for user in USERS:
                    c = by_key[(staleness, dependency, redundancy, user)]
                    vals.append(f"{c['passed']}/{c['total']}")
                lines.append(f"| {staleness} | {dependency} | "
                             + " | ".join(vals) + " |")
        lines.append("")
        lines.append(f"## Oracle findings — redundancy: {redundancy}")
        lines.append("")
        lines.append("| staleness | dependency | user | findings |")
        lines.append("|---|---|---|---|")
        for c in cells:
            if c["redundancy"] != redundancy or not c["findings"]:
                continue
            lines.append(
                f"| {c['staleness']} | {c['dependency']} | {c['user']} | "
                f"{c['findings']} ({', '.join(c['finding_classes'])}) |")
        lines.append("")
    lines.append("## Finding detail")
    lines.append("")
    for row in rows:
        for f in row["findings"]:
            where = (f"{row['staleness']}/{row['dependency']}/"
                     f"{row['redundancy']}/{row['user']}/{row['case']}")
            lines.append(f"- **{f['class']}** — {where}")
            ev = f["evidence"]
            if f["class"] == "stale_corpus_answered_as_current":
                docs = ", ".join(
                    f"{d['doc']} (snapshot {d['snapshot']})"
                    for d in ev["grounding_docs"])
                lines.append(f"  - grounded entirely in: {docs}")
            elif f["class"] == "answer_contradiction":
                lines.append(f"  - attribute: {ev['attribute']}")
                for value, sents in ev["values"].items():
                    for s in sents:
                        lines.append(f"  - [{value}] \"{s}\"")
            elif f["class"] == "sources_disagree":
                lines.append(f"  - attribute: {ev['attribute']}: "
                             + "; ".join(f"{v} <- {docs}"
                                         for v, docs in ev["values"].items()))
    lines.append("")
    return "\n".join(lines)


def fuzz_report(results: list[dict]) -> str:
    lines = ["# AgentFlightSim — mutation/fuzzing results", "",
             "Each mutation perturbs the base cell (fresh / up / overlap) "
             "off-grid. A wrong answer **escapes** when it asserts a "
             "non-truth value, passes the scorer, and draws no oracle "
             "finding.", ""]
    for r in results:
        lines.append(f"## {r['mutation']}")
        lines.append("")
        lines.append(r["description"])
        lines.append("")
        lines.append(f"- scorer failures: "
                     f"{', '.join(r['scorer_failures']) or 'none'}")
        lines.append(f"- freshness oracle flags: "
                     f"{', '.join(r['freshness_flags']) or 'none'}")
        lines.append(f"- consistency oracle flags: "
                     f"{', '.join(r['consistency_flags']) or 'none'}")
        lines.append(f"- wrong answers (assert a non-truth value): "
                     f"{len(r['wrong_answers'])}")
        for w in r["wrong_answers"]:
            lines.append(f"  - {w['case']}: {w['wrong']}")
        lines.append(f"- **escapes (wrong + passed + unflagged): "
                     f"{len(r['escapes'])}**")
        for e in r["escapes"]:
            lines.append(f"  - ESCAPE {e['case']}: {e['wrong']}")
        lines.append("")
    return "\n".join(lines)
