"""Mutation/fuzzing: scenarios perturbed OFF the grid.

The Critic's objection #1: a grid only enumerates intersections of
axes the designer chose, so it covers known unknowns. These mutators
perturb the base cell's documents in ways no axis expresses:

- restamp            stale content wearing a fresh header date. The
                     freshness oracle reads header dates; a re-stamped
                     document is exactly how real caches lie.
- partial_stale      one fact inside an otherwise fresh document is
                     reverted to yesterday's value. Grid staleness is
                     whole-document; real staleness is per-fact.
- value_swap         a fresh document's stock count is changed to a
                     value that appears in NEITHER snapshot -- not
                     stale, not fresh, just wrong.
- contradiction_append  a single fresh document gains a sentence
                     asserting the opposite of its own status. The
                     grid's contradictions are cross-source; this one
                     lives inside one source.

Each mutated corpus is run through the same scorer + oracles, and each
run's answer is checked against world truth directly, so the report
can say plainly which layer -- scorer, freshness oracle, consistency
oracle, or NOTHING -- caught each mutation.
"""
from __future__ import annotations

from pathlib import Path

from .cases import CASES, USERS
from .engine import Engine
from .oracles import asserted_values
from .world import (INVENTORY_FRESH, INVENTORY_STALE, MAINTENANCE_FRESH,
                    write_corpus)

TRUTH_VALUES = {
    "pump_status": "down_for_repair",
    "stock_location": "warehouse_b",
    "stock_count": "2",
}


def _restamp() -> dict[str, str]:
    return {
        "inventory": INVENTORY_STALE.replace("2026-11-20", "2026-11-21"),
        "maintenance": MAINTENANCE_FRESH,
    }


def _partial_stale() -> dict[str, str]:
    return {
        "inventory": INVENTORY_FRESH.replace(
            "Warehouse B, cage 14", "Warehouse A, cage 3"),
        "maintenance": MAINTENANCE_FRESH,
    }


def _value_swap() -> dict[str, str]:
    return {
        "inventory": INVENTORY_FRESH.replace(
            "holds 2 spare", "holds 7 spare"),
        "maintenance": MAINTENANCE_FRESH,
    }


def _contradiction_append() -> dict[str, str]:
    return {
        "inventory": INVENTORY_FRESH,
        "maintenance": MAINTENANCE_FRESH + (
            "\nOperations note: the HP-40 pump on Line 3 is operational "
            "and cleared to run at full capacity.\n"),
    }


MUTATIONS: dict[str, tuple] = {
    "restamp": (_restamp,
                "Stale inventory content re-stamped with today's header "
                "date; maintenance fresh."),
    "partial_stale": (_partial_stale,
                      "Fresh inventory document, but the storage-location "
                      "fact is yesterday's (Warehouse A, cage 3)."),
    "value_swap": (_value_swap,
                   "Fresh inventory document with the stock count changed "
                   "from 2 to 7 -- a value in neither snapshot."),
    "contradiction_append": (_contradiction_append,
                             "Fresh maintenance document plus an appended "
                             "operations note asserting the pump is "
                             "operational."),
}


def wrong_assertions(answer: str) -> dict[str, list[str]]:
    """Attribute -> non-truth values the answer asserts."""
    wrong: dict[str, list[str]] = {}
    for attr, values in asserted_values(answer).items():
        bad = [v for v in values if TRUTH_VALUES.get(attr) not in (None, v)]
        if bad:
            wrong[attr] = bad
    return wrong


def run_fuzz(engine: Engine, workdir: Path) -> list[dict]:
    """Run every mutation over every user type; judge each layer."""
    results: list[dict] = []
    for name, (make, description) in MUTATIONS.items():
        corpus = write_corpus(workdir / "fuzz" / name, make())
        rows: list[dict] = []
        for user in USERS:
            for case in CASES[user]:
                row = engine.run_case(corpus, case)
                row.update({"mutation": name, "user": user})
                row["wrong"] = ({} if row["abstained"]
                                else wrong_assertions(row["answer"]))
                rows.append(row)
        results.append({
            "mutation": name,
            "description": description,
            "rows": rows,
            "scorer_failures": [r["case"] for r in rows if not r["passed"]],
            "freshness_flags": sorted({
                r["case"] for r in rows for f in r["findings"]
                if f["class"] == "stale_corpus_answered_as_current"}),
            "consistency_flags": sorted({
                r["case"] for r in rows for f in r["findings"]
                if f["oracle"] == "consistency"}),
            "wrong_answers": [
                {"case": r["case"], "wrong": r["wrong"]}
                for r in rows if r["wrong"]],
            "escapes": [
                {"case": r["case"], "wrong": r["wrong"]}
                for r in rows
                if r["wrong"] and r["passed"] and not r["findings"]],
        })
    return results
