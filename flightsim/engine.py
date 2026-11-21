"""The scenario engine: enumerate the grid, run the agent, judge runs.

Agent under test: factory-floor-agent's `run_agent`, unmodified, on its
offline stub composer (no API key). Scorer: rag-evaluation-harness's
`evaluate_case`, imported verbatim -- its `run_agent` symbol is rebound
to the agent under test pointed at the current cell's corpus, exactly
as in the cheap test. The oracles (oracles.py) judge the same runs a
second time, with checks the scorer doesn't have.

Determinism: the stub agent is deterministic, the grid order is fixed,
and the CLI runs the whole grid twice and refuses to report results if
the two passes differ.
"""
from __future__ import annotations

import importlib.util
import os
import sys
from pathlib import Path

from .cases import CASES, USERS
from .oracles import run_oracles
from .world import DEPENDENCY, REDUNDANCY, STALENESS, Corpus, build_corpus

REPO = Path(__file__).resolve().parent.parent
PORTFOLIO = Path(os.environ.get("FLIGHTSIM_PORTFOLIO", REPO.parent))


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def _load_portfolio():
    if os.environ.get("OPENAI_API_KEY"):
        raise RuntimeError(
            "FlightSim runs the agent on its offline stub composer; "
            "OPENAI_API_KEY is set in the environment. Unset it.")
    sys.path.insert(0, str(PORTFOLIO / "factory-floor-agent" / "src"))
    ff_agent = _load_module(
        "ff_agent", PORTFOLIO / "factory-floor-agent" / "src" / "agent.py")
    rag_eval = _load_module(
        "rag_eval",
        PORTFOLIO / "rag-evaluation-harness" / "evals" / "run_eval.py")
    return ff_agent, rag_eval


class Engine:
    def __init__(self, workdir: Path):
        self.workdir = Path(workdir)
        self.ff_agent, self.rag_eval = _load_portfolio()
        self._corpus_dir: Path | None = None
        engine = self

        def _run_agent(question: str, threshold: float | None = None):
            return engine.ff_agent.run_agent(
                question, docs_dir=engine._corpus_dir)

        self.rag_eval.run_agent = _run_agent

    # ------------------------------------------------------------- runs

    def run_case(self, corpus: Corpus, case: dict) -> dict:
        """One run: scorer verdict + full trace + oracle findings."""
        self._corpus_dir = corpus.dir
        verdict = self.rag_eval.evaluate_case(case)
        trace = self.ff_agent.run_agent(case["question"],
                                        docs_dir=corpus.dir)
        passages: dict[str, str] = {}
        for hit in trace.get("hits", []):
            passages.setdefault(hit.chunk.doc_id, "")
            passages[hit.chunk.doc_id] += hit.chunk.text + "\n"
        run = {
            "answer": trace.get("answer", ""),
            "claims": trace.get("claims", []),
            "grounded": bool(trace.get("grounded")),
            "abstained": bool(trace.get("abstained")
                              or not trace.get("grounded")),
            "hit_docs": [h.chunk.doc_id for h in trace.get("hits", [])],
            "passages": passages,
        }
        return {
            "case": case["id"],
            "kind": case["kind"],
            "passed": verdict["passed"],
            "diagnosis": verdict["diagnosis"],
            "answer": run["answer"],
            "grounded": run["grounded"],
            "abstained": run["abstained"],
            "hit_docs": run["hit_docs"],
            "findings": run_oracles(run, corpus),
        }

    def run_cell(self, staleness: str, dependency: str, redundancy: str,
                 user: str, corpus: Corpus | None = None) -> list[dict]:
        if corpus is None:
            corpus = build_corpus(
                self.workdir / "corpora"
                / f"{staleness}-{dependency}-{redundancy}",
                staleness, dependency, redundancy)
        rows = []
        for case in CASES[user]:
            row = self.run_case(corpus, case)
            row.update({"staleness": staleness, "dependency": dependency,
                        "redundancy": redundancy, "user": user})
            rows.append(row)
        return rows

    def run_grid(self) -> list[dict]:
        rows: list[dict] = []
        for staleness in STALENESS:
            for dependency in DEPENDENCY:
                for redundancy in REDUNDANCY:
                    for user in USERS:
                        rows.extend(self.run_cell(
                            staleness, dependency, redundancy, user))
        return rows


def row_key(row: dict) -> tuple:
    return (row["staleness"], row["dependency"], row["redundancy"],
            row["user"], row["case"], row["passed"], row["answer"],
            tuple(sorted(f["class"] for f in row["findings"])))


def assert_deterministic(rows_a: list[dict], rows_b: list[dict]) -> None:
    if [row_key(r) for r in rows_a] != [row_key(r) for r in rows_b]:
        raise AssertionError(
            "NON-DETERMINISM: two full passes over the same grid differ")


def summarize_cells(rows: list[dict]) -> list[dict]:
    """One summary dict per grid cell, in grid order."""
    cells = []
    for staleness in STALENESS:
        for dependency in DEPENDENCY:
            for redundancy in REDUNDANCY:
                for user in USERS:
                    cell = [r for r in rows
                            if r["staleness"] == staleness
                            and r["dependency"] == dependency
                            and r["redundancy"] == redundancy
                            and r["user"] == user]
                    if not cell:
                        continue
                    findings = [f for r in cell for f in r["findings"]]
                    cells.append({
                        "staleness": staleness, "dependency": dependency,
                        "redundancy": redundancy, "user": user,
                        "passed": sum(r["passed"] for r in cell),
                        "total": len(cell),
                        "failed_cases": [r["case"] for r in cell
                                         if not r["passed"]],
                        "finding_classes": sorted(
                            {f["class"] for f in findings}),
                        "findings": len(findings),
                    })
    return cells
