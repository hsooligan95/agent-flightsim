"""The simulated world: two service twins and the axes they vary on.

World truth (2026-11-21, "now"): the HP-40 pump on Line 3 is DOWN and
removed for repair; 2 spares sit in Warehouse B, cage 14; a
replenishment order is on order; Line 3 runs on backup pump BP-9 at
reduced capacity.

Yesterday's snapshot (stale): pump operational, 5 spares in Warehouse A
cage 3, Line 3 at full capacity, no maintenance hold.

Axes
----
staleness   fresh | stale          -- age of the inventory twin's snapshot
dependency  up | degraded | down   -- maintenance twin serves its live
                                      doc, yesterday's cached doc, or
                                      nothing at all
user        normal | adversarial | imprecise   (question sets, cases.py)
redundancy  overlap | partitioned  -- whether the inventory twin also
                                      states the pump-status fact.
                                      Justification: the cheap test
                                      (flightsim-test) showed answers
                                      surviving a dependency outage only
                                      when the surviving twin redundantly
                                      covered the fact. Redundancy is an
                                      architectural property of the real
                                      corpus, so it is an axis, not an
                                      accident of the fixtures.

Every document carries its snapshot date in its header -- the only
freshness signal that exists in the corpus. The oracles parse it from
the text, exactly as a real freshness check would have to.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

WORLD_NOW = date(2026, 11, 21)
FRESH_DATE = date(2026, 11, 21)
STALE_DATE = date(2026, 11, 20)

STALENESS = ["fresh", "stale"]
DEPENDENCY = ["up", "degraded", "down"]
REDUNDANCY = ["overlap", "partitioned"]

# ------------------------------------------------------------------ docs

_INV_STATUS_FRESH = (
    "The HP-40 pump installed on Line 3 was removed yesterday and sent "
    "out for repair.\n")
_INV_STATUS_STALE = (
    "The HP-40 pump installed on Line 3 is operational and in daily "
    "service.\n")

INVENTORY_FRESH = """# Inventory Status
Source: Inventory Service

Snapshot generated 2026-11-21 at 06:00 from the live inventory system.

The warehouse currently holds 2 spare HP-40 hydraulic pumps in stock.
The spare HP-40 pumps are stored in Warehouse B, cage 14, on the ground floor rack.
A replenishment order for additional HP-40 pumps is already on order with the supplier.
""" + _INV_STATUS_FRESH

INVENTORY_STALE = """# Inventory Status
Source: Inventory Service

Snapshot generated 2026-11-20 at 06:00 from the live inventory system.

The warehouse currently holds 5 spare HP-40 hydraulic pumps in stock.
The spare HP-40 pumps are stored in Warehouse A, cage 3, on the ground floor rack.
No replenishment order is needed because stock levels are healthy this week.
""" + _INV_STATUS_STALE

MAINTENANCE_FRESH = """# Maintenance Status
Source: Maintenance Service

Snapshot generated 2026-11-21 at 06:00 from the live maintenance system.

The HP-40 hydraulic pump on Line 3 is down and has been removed for repair.
Line 3 is currently running on the backup pump BP-9 at reduced capacity.
The repaired HP-40 pump is expected back from the workshop on Friday.
A maintenance hold is in place on the HP-40 pump until the repair is complete.
"""

# Degraded dependency: the maintenance backend is degraded, so the twin
# serves its cached copy from yesterday. Real degraded caches present
# their data as normal assertions; the only freshness signal is the
# header line, which nothing in the agent reads.
MAINTENANCE_DEGRADED = """# Maintenance Status
Source: Maintenance Service

Cached snapshot generated 2026-11-20 at 06:00, served while the maintenance backend is degraded.

The HP-40 hydraulic pump on Line 3 is operational and running normally.
Line 3 is running at full capacity with the HP-40 pump in service.
The next scheduled service for the HP-40 pump is due in three weeks.
No maintenance hold is active on the HP-40 pump or on Line 3 equipment.
"""


def _partitioned(text: str, status_sentence: str) -> str:
    """Drop the pump-status sentence: the fact lives in one twin only."""
    return text.replace(status_sentence, "")


# ------------------------------------------------------- fact assertions
# The consistency oracle's vocabulary, declared per world: for each
# monitored attribute, the mutually exclusive values and the sentence
# patterns that assert each one. Patterns are assertion-shaped (they
# include their negations, e.g. "no maintenance hold" asserts
# *operational*) so a match means the sentence takes that side.

FACT_GROUPS: list[dict] = [
    {
        "attribute": "pump_status",
        "kind": "patterns",
        "values": {
            "operational": [
                r"operational",
                r"running normally",
                r"full capacity",
                r"no maintenance hold",
                r"in daily service",
            ],
            "down_for_repair": [
                r"removed yesterday and sent out for repair",
                r"removed for repair",
                r"is down\b",
                r"maintenance hold is in place",
                r"reduced capacity",
                r"backup pump",
            ],
        },
    },
    {
        "attribute": "stock_location",
        "kind": "patterns",
        "values": {
            "warehouse_a": [r"warehouse a\b"],
            "warehouse_b": [r"warehouse b\b"],
        },
    },
    {
        "attribute": "stock_count",
        "kind": "numeric",
        # The asserted value is the captured numeral itself.
        "pattern": r"(\d+)\s+spare",
    },
]

_SNAPSHOT_RE = re.compile(
    r"(?:Cached snapshot|Snapshot) generated (\d{4}-\d{2}-\d{2})")


def parse_snapshot_date(text: str) -> date | None:
    """The freshness signal a real system would have: the header date."""
    m = _SNAPSHOT_RE.search(text)
    return date.fromisoformat(m.group(1)) if m else None


# ---------------------------------------------------------------- corpus

@dataclass
class DocMeta:
    doc_id: str
    service: str
    snapshot_date: date | None

    @property
    def stale(self) -> bool:
        return self.snapshot_date is not None and self.snapshot_date < WORLD_NOW


@dataclass
class Corpus:
    dir: Path
    docs: dict[str, DocMeta] = field(default_factory=dict)

    def doc_for_service(self, service: str) -> DocMeta | None:
        for meta in self.docs.values():
            if meta.service == service:
                return meta
        return None


def _service_of(text: str) -> str:
    m = re.search(r"Source:\s*(.+)", text)
    return m.group(1).strip() if m else "unknown"


def build_corpus(out_dir: Path, staleness: str, dependency: str,
                 redundancy: str = "overlap") -> Corpus:
    """Write the corpus for one grid cell and describe it.

    Snapshot dates in the returned metadata are PARSED from the written
    documents, not asserted by the builder -- the metadata is the
    oracle's view of the world, and fuzzing (which re-stamps documents)
    depends on that honesty.
    """
    if staleness not in STALENESS:
        raise ValueError(staleness)
    if dependency not in DEPENDENCY:
        raise ValueError(dependency)
    if redundancy not in REDUNDANCY:
        raise ValueError(redundancy)
    out_dir.mkdir(parents=True, exist_ok=True)
    for old in out_dir.glob("*.md"):
        old.unlink()

    inv = INVENTORY_FRESH if staleness == "fresh" else INVENTORY_STALE
    status_sentence = (_INV_STATUS_FRESH if staleness == "fresh"
                       else _INV_STATUS_STALE)
    if redundancy == "partitioned":
        inv = _partitioned(inv, status_sentence)
    texts: dict[str, str] = {"inventory": inv}
    if dependency == "up":
        texts["maintenance"] = MAINTENANCE_FRESH
    elif dependency == "degraded":
        texts["maintenance"] = MAINTENANCE_DEGRADED
    # dependency == "down": the maintenance twin serves nothing.

    corpus = Corpus(dir=out_dir)
    for doc_id, text in texts.items():
        (out_dir / f"{doc_id}.md").write_text(text, encoding="utf-8")
        corpus.docs[doc_id] = DocMeta(
            doc_id=doc_id, service=_service_of(text),
            snapshot_date=parse_snapshot_date(text))
    return corpus


def write_corpus(out_dir: Path, texts: dict[str, str]) -> Corpus:
    """Write arbitrary document texts (the fuzzing entry point) and
    describe them by parsing, never by assumption."""
    out_dir.mkdir(parents=True, exist_ok=True)
    for old in out_dir.glob("*.md"):
        old.unlink()
    corpus = Corpus(dir=out_dir)
    for doc_id, text in texts.items():
        (out_dir / f"{doc_id}.md").write_text(text, encoding="utf-8")
        corpus.docs[doc_id] = DocMeta(
            doc_id=doc_id, service=_service_of(text),
            snapshot_date=parse_snapshot_date(text))
    return corpus
