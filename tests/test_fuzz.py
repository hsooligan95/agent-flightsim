"""Fuzzing outcomes, as observed in the shipped run -- regression-
pinned so a future change has to argue with these numbers."""
import pytest

from flightsim.fuzz import run_fuzz


@pytest.fixture(scope="module")
def results(engine, tmp_path_factory):
    out = run_fuzz(engine, tmp_path_factory.mktemp("fuzz"))
    return {r["mutation"]: r for r in out}


def test_restamp_defeats_freshness_oracle_but_not_the_stack(results):
    """A re-stamped stale document draws ZERO freshness flags -- the
    oracle reads header dates and the header lies. The wrongness is
    still caught, by the scorer's terms and cross-source consistency:
    the freshness oracle is defeated, the stack is not."""
    r = results["restamp"]
    assert r["freshness_flags"] == []
    assert r["wrong_answers"] != []
    assert r["escapes"] == []


def test_partial_stale_escapes_through_n_compound(results):
    """One stale fact inside a fresh document: doc-level freshness
    cannot see it, and n-compound passes the scorer on its other
    expected term while asserting the stale location."""
    r = results["partial_stale"]
    assert r["freshness_flags"] == []
    escaped = {e["case"] for e in r["escapes"]}
    assert "n-compound" in escaped


def test_value_swap_escapes_every_layer(results):
    """The fuzzing run's hardest finding: a stock count of 7 (truth 2)
    in a fresh, internally consistent document is caught by NOTHING --
    no scorer term pins the count, and no second source states one
    for the consistency oracle to disagree with."""
    r = results["value_swap"]
    assert r["escapes"] != []
    for e in r["escapes"]:
        assert e["wrong"] == {"stock_count": ["7"]}


def test_contradiction_append_caught_by_consistency(results):
    """A contradiction inside a SINGLE document -- a configuration
    the grid cannot express -- is flagged by the consistency oracle."""
    r = results["contradiction_append"]
    assert r["consistency_flags"] != []
    assert r["escapes"] == []
