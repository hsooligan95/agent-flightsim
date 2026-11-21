"""Regression cases: the cheap test's headline cells, reproduced
inside the full build. If any of these change, the sim's README claims
change with them -- that is what a regression case is for.
"""
import pytest


def _cell(engine, staleness, dependency, redundancy, user):
    rows = engine.run_cell(staleness, dependency, redundancy, user)
    return {r["case"]: r for r in rows}


def _classes(row):
    return {f["class"] for f in row["findings"]}


@pytest.mark.parametrize("user", ["normal", "adversarial", "imprecise"])
def test_stale_degraded_everything_fails_and_freshness_fires(
        engine, user):
    """Cheap test: stale/degraded scored 0 in every user column, and
    every run grounded entirely in yesterday's snapshots."""
    rows = _cell(engine, "stale", "degraded", "overlap", user)
    assert all(not r["passed"] for r in rows.values())
    for row in rows.values():
        if not row["abstained"]:
            assert "stale_corpus_answered_as_current" in _classes(row)


def test_fresh_degraded_contradiction_the_scorer_passes(engine):
    """THE headline regression. fresh/degraded, n-status: the harness
    scorer PASSES this run (an expected term is present, every
    sentence grounded) while the answer asserts the pump is both
    operational and removed for repair. The consistency oracle must
    flag what the scorer cannot see."""
    rows = _cell(engine, "fresh", "degraded", "overlap", "normal")
    row = rows["n-status"]
    assert row["passed"] is True
    assert "answer_contradiction" in _classes(row)
    assert "sources_disagree" in _classes(row)


def test_stale_up_stock_answers_fail_on_terms(engine):
    """Cheap test: in stale/up the stock cases fail because the agent
    reports yesterday's 5 spares in Warehouse A as today's truth."""
    rows = _cell(engine, "stale", "up", "overlap", "normal")
    assert rows["n-stock"]["passed"] is False
    assert "Warehouse A" in rows["n-stock"]["answer"]


def test_redundancy_axis_changes_which_oracle_catches_degraded(engine):
    """With the status fact partitioned into the maintenance twin
    only, a degraded cache leaves the agent grounded entirely in the
    stale doc -- so the FRESHNESS oracle, not consistency, fires."""
    rows = _cell(engine, "fresh", "degraded", "partitioned", "normal")
    assert "stale_corpus_answered_as_current" in _classes(rows["n-status"])


def test_healthy_control_cell_is_clean(engine):
    """fresh/up: status and stock pass, and no oracle fires on the
    status answer. (n-abstain's failure to abstain is a known,
    pre-registered class -- K5 -- and is not asserted here.)"""
    rows = _cell(engine, "fresh", "up", "overlap", "normal")
    assert rows["n-status"]["passed"] is True
    assert rows["n-status"]["findings"] == []
    assert rows["n-stock"]["passed"] is True
