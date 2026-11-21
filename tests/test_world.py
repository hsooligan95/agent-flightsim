from datetime import date

from flightsim.world import (build_corpus, parse_snapshot_date)


def test_fresh_up_corpus(tmp_path):
    corpus = build_corpus(tmp_path / "c", "fresh", "up")
    assert set(corpus.docs) == {"inventory", "maintenance"}
    assert corpus.docs["inventory"].snapshot_date == date(2026, 11, 21)
    assert not corpus.docs["inventory"].stale
    assert not corpus.docs["maintenance"].stale


def test_degraded_maintenance_is_yesterdays_cache(tmp_path):
    corpus = build_corpus(tmp_path / "c", "fresh", "degraded")
    assert corpus.docs["maintenance"].snapshot_date == date(2026, 11, 20)
    assert corpus.docs["maintenance"].stale
    assert not corpus.docs["inventory"].stale


def test_down_omits_maintenance(tmp_path):
    corpus = build_corpus(tmp_path / "c", "stale", "down")
    assert set(corpus.docs) == {"inventory"}
    assert corpus.docs["inventory"].stale


def test_partitioned_drops_status_sentence_from_inventory(tmp_path):
    overlap = build_corpus(tmp_path / "o", "fresh", "up", "overlap")
    partitioned = build_corpus(tmp_path / "p", "fresh", "up", "partitioned")
    over_text = (overlap.dir / "inventory.md").read_text(encoding="utf-8")
    part_text = (partitioned.dir / "inventory.md").read_text(encoding="utf-8")
    assert "removed yesterday and sent out for repair" in over_text
    assert "removed yesterday" not in part_text
    # stock facts survive partitioning; only the status fact moves out
    assert "Warehouse B, cage 14" in part_text


def test_parse_snapshot_date_variants():
    assert parse_snapshot_date(
        "Snapshot generated 2026-11-21 at 06:00") == date(2026, 11, 21)
    assert parse_snapshot_date(
        "Cached snapshot generated 2026-11-20 at 06:00, served while "
        "degraded") == date(2026, 11, 20)
    assert parse_snapshot_date("no header here") is None
