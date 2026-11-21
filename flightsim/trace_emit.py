"""AgentTrace integration: every sim batch lands in the audit store.

Each batch (grid, fuzz) is emitted into an AgentTrace store
(~/workspace/github-portfolio/agent-trace, schema_version 1) under one
trace ID: batch start, one event per cell/mutation, one event per
oracle finding, and a closing decision_record carrying the batch
verdict. The store then renders the batch as a tree/timeline via
AgentTrace's own renderer -- the sim's runs become auditable artifacts
in the same record as the rest of the portfolio's agents.

Timestamps are the sim's deterministic clock (world date + event
index), so re-running a batch reproduces the same store byte-for-byte
up to the hash chain.
"""
from __future__ import annotations

import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

from .engine import PORTFOLIO, summarize_cells

sys.path.insert(0, str(PORTFOLIO / "agent-trace"))

from agenttrace.render import render_timeline  # noqa: E402
from agenttrace.schema import new_event  # noqa: E402
from agenttrace.store import append_events, load_events, verify  # noqa: E402

SOURCE = "agent-flightsim"
AGENT = "flightsim"
_BASE_TS = datetime(2026, 11, 21, 6, 0, tzinfo=timezone.utc)


class _Clock:
    def __init__(self) -> None:
        self._n = 0

    def next(self) -> str:
        ts = _BASE_TS + timedelta(minutes=self._n)
        self._n += 1
        return ts.strftime("%Y-%m-%dT%H:%M:%SZ")


def _finding_events(clock: _Clock, trace_id: str, rows: list[dict],
                    coords: dict) -> list[dict]:
    events = []
    for row in rows:
        for finding in row["findings"]:
            events.append(new_event(
                trace_id=trace_id, ts=clock.next(), source=SOURCE,
                agent=AGENT, type="oracle_finding",
                payload={"class": finding["class"],
                         "oracle": finding["oracle"],
                         **coords, "case": row["case"],
                         "evidence": finding["evidence"]}))
    return events


def emit_grid_batch(store_path: Path, rows: list[dict], *, seed: int,
                    trace_id: str) -> dict:
    clock = _Clock()
    cells = summarize_cells(rows)
    events = [new_event(
        trace_id=trace_id, ts=clock.next(), source=SOURCE, agent=AGENT,
        type="batch_started",
        payload={"batch": "grid", "seed": seed, "cells": len(cells),
                 "runs": len(rows)})]
    by_cell: dict[tuple, list[dict]] = {}
    for row in rows:
        by_cell.setdefault((row["staleness"], row["dependency"],
                            row["redundancy"], row["user"]), []).append(row)
    for cell in cells:
        coords = {k: cell[k] for k in
                  ("staleness", "dependency", "redundancy", "user")}
        events.append(new_event(
            trace_id=trace_id, ts=clock.next(), source=SOURCE, agent=AGENT,
            type="cell_completed",
            payload={**coords, "passed": cell["passed"],
                     "total": cell["total"],
                     "failed_cases": cell["failed_cases"],
                     "finding_classes": cell["finding_classes"]}))
        events.extend(_finding_events(
            clock, trace_id,
            by_cell[(cell["staleness"], cell["dependency"],
                     cell["redundancy"], cell["user"])], coords))
    passed = sum(r["passed"] for r in rows)
    findings = [f for r in rows for f in r["findings"]]
    classes = sorted({f["class"] for f in findings})
    events.append(new_event(
        trace_id=trace_id, ts=clock.next(), source=SOURCE, agent=AGENT,
        type="batch_verdict", kind="decision_record",
        payload={
            "decision_point": "flightsim_grid_batch_verdict",
            "choice": (f"{passed}/{len(rows)} runs passed the scorer; "
                       f"{len(findings)} oracle findings"),
            "evidence": {"reasons": [
                f"oracle finding classes: {', '.join(classes) or 'none'}",
                f"cells fully clean: "
                f"{sum(1 for c in cells if not c['findings'] and c['passed'] == c['total'])}/{len(cells)}",
            ]}}))
    append_events(store_path, events)
    return {"trace_id": trace_id, "events": len(events)}


def emit_fuzz_batch(store_path: Path, fuzz_results: list[dict], *,
                    seed: int, trace_id: str) -> dict:
    clock = _Clock()
    events = [new_event(
        trace_id=trace_id, ts=clock.next(), source=SOURCE, agent=AGENT,
        type="batch_started",
        payload={"batch": "fuzz", "seed": seed,
                 "mutations": [r["mutation"] for r in fuzz_results]})]
    for result in fuzz_results:
        coords = {"mutation": result["mutation"]}
        events.append(new_event(
            trace_id=trace_id, ts=clock.next(), source=SOURCE, agent=AGENT,
            type="mutation_completed",
            payload={**coords,
                     "scorer_failures": result["scorer_failures"],
                     "freshness_flags": result["freshness_flags"],
                     "consistency_flags": result["consistency_flags"],
                     "escapes": len(result["escapes"])}))
        events.extend(_finding_events(
            clock, trace_id, result["rows"], coords))
    escapes = sum(len(r["escapes"]) for r in fuzz_results)
    events.append(new_event(
        trace_id=trace_id, ts=clock.next(), source=SOURCE, agent=AGENT,
        type="batch_verdict", kind="decision_record",
        payload={
            "decision_point": "flightsim_fuzz_batch_verdict",
            "choice": (f"{len(fuzz_results)} mutations run; "
                       f"{escapes} wrong answer(s) escaped every layer"),
            "evidence": {"reasons": [
                f"{r['mutation']}: escapes={len(r['escapes'])}"
                for r in fuzz_results]}}))
    append_events(store_path, events)
    return {"trace_id": trace_id, "events": len(events)}


def render_store_timeline(store_path: Path) -> str:
    events = load_events(store_path)
    result = verify(store_path)
    return render_timeline(
        events, verify_result=result,
        title="AgentFlightSim — batches in the AgentTrace store")
