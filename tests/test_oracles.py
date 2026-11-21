"""Oracle unit tests on synthetic runs (no agent needed)."""
from flightsim.oracles import (asserted_values, consistency_findings,
                               freshness_findings)
from flightsim.world import build_corpus

CONTRADICTORY_ANSWER = (
    "The HP-40 hydraulic pump on Line 3 is operational and running "
    "normally. Line 3 is running at full capacity with the HP-40 pump "
    "in service. No maintenance hold is active on the HP-40 pump or on "
    "Line 3 equipment. The HP-40 pump installed on Line 3 was removed "
    "yesterday and sent out for repair.")

COHERENT_ANSWER = (
    "The HP-40 hydraulic pump on Line 3 is down and has been removed "
    "for repair. Line 3 is currently running on the backup pump BP-9 "
    "at reduced capacity.")


def _run(answer, claims_services, hit_docs=(), passages=None,
         abstained=False):
    return {
        "answer": answer,
        "claims": [{"sentence": s, "grounded": True, "overlap": 1.0,
                    "source": svc}
                   for s, svc in claims_services],
        "hit_docs": list(hit_docs),
        "passages": passages or {},
        "abstained": abstained,
    }


# -------------------------------------------------------------- freshness

def test_freshness_flags_answer_grounded_entirely_in_stale(tmp_path):
    corpus = build_corpus(tmp_path / "c", "stale", "degraded")
    run = _run("The warehouse currently holds 5 spare HP-40 hydraulic "
               "pumps in stock.",
               [("s", "Inventory Service"), ("s", "Maintenance Service")])
    findings = freshness_findings(run, corpus)
    assert [f["class"] for f in findings] == [
        "stale_corpus_answered_as_current"]
    docs = {d["doc"] for d in findings[0]["evidence"]["grounding_docs"]}
    assert docs == {"inventory", "maintenance"}


def test_freshness_silent_when_any_grounding_doc_is_fresh(tmp_path):
    corpus = build_corpus(tmp_path / "c", "stale", "up")
    run = _run("answer", [("s", "Inventory Service"),
                          ("s", "Maintenance Service")])
    assert freshness_findings(run, corpus) == []


def test_freshness_silent_on_abstention_and_on_fresh(tmp_path):
    stale = build_corpus(tmp_path / "s", "stale", "degraded")
    run = _run("", [("s", "Inventory Service")], abstained=True)
    assert freshness_findings(run, stale) == []
    fresh = build_corpus(tmp_path / "f", "fresh", "up")
    run = _run("answer", [("s", "Inventory Service")])
    assert freshness_findings(run, fresh) == []


# ------------------------------------------------------------ consistency

def test_consistency_flags_the_cheap_tests_contradictory_answer():
    run = _run(CONTRADICTORY_ANSWER, [])
    classes = [f["class"] for f in consistency_findings(run)]
    assert "answer_contradiction" in classes
    finding = next(f for f in consistency_findings(run)
                   if f["class"] == "answer_contradiction")
    assert finding["evidence"]["attribute"] == "pump_status"
    assert set(finding["evidence"]["values"]) == {
        "operational", "down_for_repair"}


def test_consistency_silent_on_coherent_answer():
    run = _run(COHERENT_ANSWER, [])
    assert consistency_findings(run) == []


def test_consistency_flags_disagreeing_sources():
    run = _run(COHERENT_ANSWER, [], passages={
        "inventory": "The HP-40 pump installed on Line 3 was removed "
                     "yesterday and sent out for repair.",
        "maintenance": "The HP-40 hydraulic pump on Line 3 is "
                       "operational and running normally.",
    })
    classes = [f["class"] for f in consistency_findings(run)]
    assert classes == ["sources_disagree"]


def test_asserted_values_numeric_counts():
    values = asserted_values(
        "The warehouse currently holds 2 spare HP-40 pumps in stock.")
    assert set(values["stock_count"]) == {"2"}
    values = asserted_values(
        "One doc holds 2 spare pumps. Another holds 5 spare pumps.")
    assert set(values["stock_count"]) == {"2", "5"}
