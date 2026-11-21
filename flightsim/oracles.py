"""The oracles: checks the per-sentence scorers structurally miss.

The existing portfolio scorers (rag-evaluation-harness) check each
answer sentence against single retrieved passages: retrieval, expected
terms, per-sentence groundedness. The FlightSim cheap test proved two
failure classes walk straight through all three:

1. **Uniformly stale corpus answered as current.** Every sentence is
   grounded -- against yesterday's snapshot. Nothing in the pipeline
   reads the snapshot timestamps the documents carry, so the agent
   certifies yesterday's world as today's with groundedness 1.0.

2. **Cross-source contradictory answers.** Two retrieved sources
   disagree (one fresh, one serving a cached older snapshot); the
   composed answer asserts BOTH sides, each sentence grounded against
   its own passage. Per-sentence groundedness cannot see it, because
   consistency is a property of the answer as a whole, not of any
   sentence.

The freshness oracle and the consistency oracle below are those two
checks, written as first-class, separately testable components.
"""
from __future__ import annotations

import re

from .world import FACT_GROUPS, Corpus

_SENTENCE_RE = re.compile(r"(?<=[.!?])\s+")


def split_sentences(text: str) -> list[str]:
    return [s.strip() for s in _SENTENCE_RE.split(text.strip())
            if s.strip()]


# ------------------------------------------------------------- freshness

def freshness_findings(run: dict, corpus: Corpus) -> list[dict]:
    """Flag a confident answer grounded entirely in stale sources.

    A finding fires when the agent answered (did not abstain) and every
    document that grounded its claims carries a snapshot date older
    than the world's "now". The oracle's view of freshness is the
    parsed header date -- the only signal the corpus actually offers.
    """
    if run.get("abstained"):
        return []
    claims = run.get("claims", [])
    services = {c.get("source") for c in claims if c.get("grounded")}
    grounding = [corpus.doc_for_service(s) for s in services if s]
    grounding = [m for m in grounding if m is not None]
    if not grounding:
        # Fall back to whatever was retrieved at all.
        grounding = [corpus.docs[d] for d in run.get("hit_docs", [])
                     if d in corpus.docs]
    if not grounding:
        return []
    if all(m.stale for m in grounding):
        return [{
            "oracle": "freshness",
            "class": "stale_corpus_answered_as_current",
            "evidence": {
                "grounding_docs": [
                    {"doc": m.doc_id,
                     "snapshot": (m.snapshot_date.isoformat()
                                  if m.snapshot_date else None)}
                    for m in grounding],
                "answer": run.get("answer", ""),
            },
        }]
    return []


# ----------------------------------------------------------- consistency

def asserted_values(text: str,
                    fact_groups: list[dict] = FACT_GROUPS
                    ) -> dict[str, dict[str, list[str]]]:
    """Map attribute -> value -> sentences asserting that value."""
    out: dict[str, dict[str, list[str]]] = {}
    for sent in split_sentences(text):
        low = sent.lower()
        for group in fact_groups:
            attr = group["attribute"]
            if group["kind"] == "numeric":
                for num in re.findall(group["pattern"], low):
                    out.setdefault(attr, {}).setdefault(num, []).append(sent)
            else:
                for value, patterns in group["values"].items():
                    if any(re.search(p, low) for p in patterns):
                        out.setdefault(attr, {}).setdefault(
                            value, []).append(sent)
    return out


def consistency_findings(run: dict) -> list[dict]:
    """Flag answers that assert both sides of a monitored attribute,
    and retrieved source sets that disagree with each other.

    - answer_contradiction: the answer itself asserts >= 2 mutually
      exclusive values for one attribute. The headline failure class:
      every sentence can be individually grounded while the answer as
      a whole is incoherent.
    - sources_disagree: the retrieved passages assert conflicting
      values. A world-level signal -- the agent was handed a
      contradiction whether or not its answer shows it.
    """
    findings: list[dict] = []
    if not run.get("abstained"):
        for attr, values in asserted_values(run.get("answer", "")).items():
            if len(values) >= 2:
                findings.append({
                    "oracle": "consistency",
                    "class": "answer_contradiction",
                    "evidence": {"attribute": attr, "values": values},
                })
    per_doc: dict[str, dict[str, dict[str, list[str]]]] = {}
    for doc_id, text in run.get("passages", {}).items():
        per_doc[doc_id] = asserted_values(text)
    attrs = {a for pv in per_doc.values() for a in pv}
    for attr in sorted(attrs):
        seen: dict[str, list[str]] = {}
        for doc_id, pv in per_doc.items():
            for value in pv.get(attr, {}):
                seen.setdefault(value, []).append(doc_id)
        if len(seen) >= 2:
            findings.append({
                "oracle": "consistency",
                "class": "sources_disagree",
                "evidence": {"attribute": attr, "values": seen},
            })
    return findings


def run_oracles(run: dict, corpus: Corpus) -> list[dict]:
    """All oracle findings for one run, each tagged with the run's
    coordinates by the caller."""
    return freshness_findings(run, corpus) + consistency_findings(run)
