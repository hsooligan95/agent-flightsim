#!/usr/bin/env python3
"""Run the full AgentFlightSim batch: grid + fuzz + AgentTrace emit.

    python run_flightsim.py [--seed N] [--out DIR] [--no-fuzz] [--no-trace]

Outputs (in --out, default ./output):
    results.json   every run: scorer verdict, answer, oracle findings
    coverage.md    the coverage map + finding detail
    fuzz.md        mutation results, layer by layer, escapes named
    agenttrace.jsonl  the batches in an AgentTrace store (if trace on)
    timeline.md    the store rendered as a tree/timeline (if trace on)

The grid is run TWICE and the passes must be identical, or nothing is
reported -- a coverage map that changes between runs is a sample, not
a map, and this tool does not ship samples dressed as maps.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from flightsim import trace_emit  # noqa: E402
from flightsim.engine import Engine, assert_deterministic  # noqa: E402
from flightsim.fuzz import run_fuzz  # noqa: E402
from flightsim.report import coverage_map, fuzz_report  # noqa: E402


def _jsonable(rows: list[dict]) -> list[dict]:
    return [{k: v for k, v in r.items()} for r in rows]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, default=20261121)
    parser.add_argument("--out", type=Path,
                        default=Path(__file__).resolve().parent / "output")
    parser.add_argument("--no-fuzz", action="store_true")
    parser.add_argument("--no-trace", action="store_true")
    args = parser.parse_args()

    out = args.out
    out.mkdir(parents=True, exist_ok=True)
    engine = Engine(workdir=out)

    print("grid pass 1/2 ...")
    rows = engine.run_grid()
    print("grid pass 2/2 (determinism check) ...")
    assert_deterministic(rows, engine.run_grid())
    print(f"determinism: two full grid passes identical ({len(rows)} runs)")

    fuzz_results = []
    if not args.no_fuzz:
        print("fuzz mutations ...")
        fuzz_results = run_fuzz(engine, out)

    (out / "results.json").write_text(json.dumps({
        "seed": args.seed,
        "grid": _jsonable(rows),
        "fuzz": [{k: v for k, v in r.items() if k != "rows"}
                 | {"rows": _jsonable(r["rows"])} for r in fuzz_results],
    }, indent=2), encoding="utf-8")
    (out / "coverage.md").write_text(coverage_map(rows), encoding="utf-8")
    if fuzz_results:
        (out / "fuzz.md").write_text(fuzz_report(fuzz_results),
                                     encoding="utf-8")

    passed = sum(r["passed"] for r in rows)
    findings = [f for r in rows for f in r["findings"]]
    print(f"grid: {passed}/{len(rows)} scorer passes; "
          f"{len(findings)} oracle findings")
    for cls in sorted({f["class"] for f in findings}):
        n = sum(1 for f in findings if f["class"] == cls)
        print(f"  {cls}: {n}")
    for r in fuzz_results:
        print(f"fuzz {r['mutation']}: wrong={len(r['wrong_answers'])} "
              f"escapes={len(r['escapes'])}")

    if not args.no_trace:
        store = out / "agenttrace.jsonl"
        if store.exists():
            store.unlink()  # fresh store per batch run; chain stays valid
        g = trace_emit.emit_grid_batch(
            store, rows, seed=args.seed,
            trace_id=f"flightsim-grid-{args.seed}")
        print(f"trace: grid batch -> {g['events']} events "
              f"(trace {g['trace_id']})")
        if fuzz_results:
            fz = trace_emit.emit_fuzz_batch(
                store, fuzz_results, seed=args.seed,
                trace_id=f"flightsim-fuzz-{args.seed}")
            print(f"trace: fuzz batch -> {fz['events']} events "
                  f"(trace {fz['trace_id']})")
        (out / "timeline.md").write_text(
            trace_emit.render_store_timeline(store), encoding="utf-8")
        print("trace: timeline rendered from the store alone")
    print(f"outputs in {out}")


if __name__ == "__main__":
    main()
