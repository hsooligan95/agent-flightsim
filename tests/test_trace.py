"""AgentTrace integration: a sim batch lands in the store as
schema_version 1 events under one trace ID, the chain verifies, and
the store alone renders the batch timeline."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from flightsim import trace_emit  # noqa: E402
from flightsim.engine import PORTFOLIO  # noqa: E402

sys.path.insert(0, str(PORTFOLIO / "agent-trace"))
from agenttrace.store import load_events, verify  # noqa: E402


def test_grid_batch_lands_in_store(engine, tmp_path):
    rows = engine.run_cell("stale", "degraded", "overlap", "normal")
    store = tmp_path / "store.jsonl"
    out = trace_emit.emit_grid_batch(
        store, rows, seed=1, trace_id="flightsim-grid-test")
    assert out["events"] > len(rows)
    result = verify(store)
    assert result.ok and result.count == out["events"]
    events = load_events(store)
    assert all(e["schema_version"] == "1" for e in events)
    assert {e["trace_id"] for e in events} == {"flightsim-grid-test"}
    assert {e["source"] for e in events} == {"agent-flightsim"}
    verdicts = [e for e in events if e["kind"] == "decision_record"]
    assert len(verdicts) == 1
    assert verdicts[0]["payload"]["decision_point"] == \
        "flightsim_grid_batch_verdict"
    findings = [e for e in events if e["type"] == "oracle_finding"]
    assert findings, "stale/degraded must emit oracle findings"
    assert all(f["payload"]["class"] ==
               "stale_corpus_answered_as_current" for f in findings)
    timeline = trace_emit.render_store_timeline(store)
    assert "Chain OK" in timeline
    assert "flightsim-grid-test" in timeline
