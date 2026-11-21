# AgentFlightSim

**Enumerate the world your agent will meet — don't just test the code it runs.**

AgentFlightSim is a scenario engine for agents: it builds simulated
service twins, sweeps the world-state axes production actually varies
on, runs a real agent over every cell of the grid, and judges the runs
with two oracles the standard scorers don't have — a **freshness
oracle** and a **cross-source consistency oracle**. It exists because
its own cheap test found failures that per-sentence groundedness
structurally cannot see.

## The incident that justifies the oracles

World truth, 2026-11-21: the HP-40 pump on Line 3 is **down, removed
for repair**; Line 3 runs on a backup pump at reduced capacity.

Put the agent in a world where its only corpus is yesterday's snapshot
and ask about the pump. It answers, fluently and with every sentence
grounded at overlap 1.0:

> "The HP-40 hydraulic pump on Line 3 is operational and running
> normally. Line 3 is running at full capacity with the HP-40 pump in
> service. No maintenance hold is active on the HP-40 pump or on
> Line 3 equipment. The HP-40 pump installed on Line 3 is operational
> and in daily service."

Nothing failed. No tool timed out, no fallback was chosen. The
documents carry snapshot timestamps — *nothing in the pipeline reads
them* — so the agent certifies yesterday's world as today's, and the
groundedness scorer has nothing to object to: every claim is grounded,
in a world that no longer exists.

The second incident is worse. With one twin fresh and the other
serving a cached older snapshot, the agent composes an answer that
asserts **both** worlds — "operational and running normally… No
maintenance hold is active" *and* "removed yesterday and sent out for
repair" — and the existing evaluation harness **passes the run**: an
expected term is present, and each sentence is grounded against its
own passage. Consistency is a property of the answer as a whole;
per-sentence checks cannot see it, ever.

Those two blind spots are this repo's headline components.

## The oracles

- **Freshness oracle** (`flightsim/oracles.py`) — parses the snapshot
  date each document declares in its header (the only freshness signal
  the corpus offers) and flags any confident answer grounded
  *entirely* in stale sources: `stale_corpus_answered_as_current`.
- **Consistency oracle** — extracts asserted values for monitored
  attributes (pump status, stock location, stock count — declared per
  world in `flightsim/world.py`) and flags `answer_contradiction`
  (one answer asserting mutually exclusive values) and
  `sources_disagree` (the retrieved sources themselves conflict).

## The engine

Two service twins (inventory, maintenance) generate the corpus; the
grid sweeps four axes — the fourth is there because the cheap test
earned it:

| axis | values | why |
|---|---|---|
| staleness | fresh, stale | age of the inventory snapshot |
| dependency | up, degraded, down | maintenance twin serves live data, yesterday's cache, or nothing |
| user | normal, adversarial, imprecise | question style, incl. leading premises and "ignore the hold" |
| redundancy | overlap, partitioned | whether a fact lives in both twins or one — the cheap test showed answers surviving an outage only when the surviving twin redundantly covered the fact |

108 runs over 36 cells, scored by rag-evaluation-harness's scorer
verbatim (expected terms encode world truth) and then by the oracles.
The grid runs **twice** and the passes must be byte-identical, or the
tool refuses to report: a coverage map that changes between runs is a
sample, not a map.

## Results (seed 20261121, reproduced by `python run_flightsim.py`)

Scorer: **43/108 passed**. Oracles: **72 findings** the scorer's
verdicts alone don't express — 42 stale-as-current, 14 answer
contradictions, 16 source disagreements. Only **4 of 36 cells** are
fully clean. Full map and finding detail: `output/coverage.md`.

Three readings worth a reviewer's time:

- **fresh/degraded passes the scorer while contradicting itself.**
  Every status answer in those cells is a two-snapshot composite; the
  consistency oracle flags all of them (14 findings across the
  degraded/overlap cells), the scorer flags none of the status runs.
- **The redundancy axis changes which oracle saves you.** With the
  status fact in both twins (overlap), a degraded cache produces
  contradictions. Partition the fact into the maintenance twin alone
  and the same degraded cell produces answers grounded entirely in
  the cached doc — the freshness oracle's catch instead — and the
  scorer pass rate in fresh/degraded falls from 3/4·3/3·2/2 to
  1/4·1/3·1/2. Redundancy is measurable resilience, not a style choice.
- **stale/degraded is a total loss**: 0/9 runs pass, every answer a
  coherent yesterday. No fault event, no warning anywhere in the
  agent — the sim is the only place this world was ever enumerated.

## Fuzzing: beyond the grid

A grid only covers intersections of axes its designer chose (the
Critic's objection, and a fair one). Four mutators perturb documents
off-grid; each run's answer is also checked directly against world
truth, so the report can name which layer — scorer, freshness oracle,
consistency oracle, or **nothing** — caught each mutation
(`output/fuzz.md`):

| mutation | wrong answers | escapes | caught by |
|---|---|---|---|
| restamp (stale content, fresh header) | 9 | 0 | scorer terms + consistency — **the freshness oracle itself is fooled**: it reads header dates and the header lies |
| partial_stale (one stale fact in a fresh doc) | 4 | **1** | scorer, mostly; n-compound escapes — it passes on its other expected term while asserting the stale location |
| value_swap (stock count 2 → 7, in neither snapshot) | 5 | **4** | **nothing** — no scorer term pins the count, and with only one source stating a count, the consistency oracle has nothing to disagree with |
| contradiction_append (one doc contradicts itself) | 6 | 0 | consistency oracle — a configuration the grid cannot express, caught by an oracle that generalizes past it |

Honest summary: fuzzing found two things the grid didn't — a
wrong-but-plausible fact that escapes *every* layer (value_swap), and
proof that the freshness oracle's trust in timestamps is a real,
demonstrable weakness (restamp). Both are now register entries and
regression tests, not footnotes.

## AgentTrace integration

Every batch is emitted into an [AgentTrace](../agent-trace) store
(schema_version 1) under one trace ID per batch — batch start, one
event per cell, one per oracle finding, and a closing
`decision_record` with the batch verdict. The shipped run produced
**146 events; the hash chain verifies end-to-end**, and
`output/timeline.md` is rendered from the store alone: the sim's
batches sit in the same tamper-evident record as the rest of the
fleet's agents.

## What is NOT simulated

The map's polish is a liability if it implies completeness, so the
repo ships [NOT_SIMULATED.md](NOT_SIMULATED.md): no real LLM (the
agent runs the portfolio's deterministic stub — findings characterize
the pipeline, not a production model), no tool use, no multi-turn
memory, no multi-agent interaction, static dependency states,
whole-document grid staleness, trusted timestamps, declared-not-learned
contradictions, three scripted user styles, no cost/latency model.
Tests fail if the register loses an entry.

## Layout

```
flightsim/
  world.py       twins, axes, fact groups, corpus builder
  cases.py       question sets per user type (harness case format)
  oracles.py     freshness + consistency oracles
  engine.py      grid enumeration, seeded deterministic runs
  fuzz.py        off-grid document mutations, layer-by-layer judging
  trace_emit.py  AgentTrace store emission + timeline rendering
  report.py      coverage map / fuzz report rendering
run_flightsim.py the batch: grid x2, fuzz, trace, reports
NOT_SIMULATED.md the register of what the sim does not model
output/          captured results of the shipped run
tests/           engine, oracle, fuzz, trace, and register tests
```

## Run it

FlightSim drives its sibling repos (the portfolio is one ecosystem):
it needs `factory-floor-agent`, `rag-evaluation-harness`, and
`agent-trace` checked out beside it, and `OPENAI_API_KEY` **unset** —
the agent under test runs on its offline stub composer, no keys, no
network.

```bash
pip install -r requirements.txt
python run_flightsim.py            # grid + fuzz + AgentTrace emit
python -m pytest tests/            # full suite
```

## Provenance

Productized from a one-day pre-registered cheap test
(`flightsim-test/`, with its `KNOWN_FAILURES.md` bar written before
anything was built): enumeration had to find a failing cell whose
class was not already covered by the existing eval set or chaos
scenarios, deterministically, or the standalone build died. It passed
on the stale-corpus class, and its by-product — the contradictory
composite the scorers passed — became this build's first requirement:
the oracles above.
