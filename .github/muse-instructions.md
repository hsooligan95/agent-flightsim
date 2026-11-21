# Copilot instructions — agent-flightsim

You are working in **AgentFlightSim**, a scenario engine for agents: it
builds simulated service twins, sweeps world-state axes (staleness,
dependency health, user type, redundancy), runs a real agent over every
grid cell, and judges runs with a freshness oracle and a cross-source
consistency oracle that per-sentence groundedness cannot replace.

## Stack

- Python 3; package `flightsim/`; grid runner `run_flightsim.py`.
- The agent under test is factory-floor-agent, run unmodified on its
  stub model; the scorer is imported from the evaluation harness.

## Tests

```bash
pytest              # 26 tests
python run_flightsim.py   # full grid + fuzz passes, byte-identical across double runs
```

## Architecture notes

- Determinism is a hard contract: the CLI runs the grid twice and
  refuses to report if the passes differ. Fixed seeds only; no
  wall-clock dependence in scoring.
- Simulate the world, never patch the agent to pass. The agent is the
  specimen; twins, corpora snapshots, and fault axes are the lab.
- The freshness oracle parses document header snapshot dates; the
  consistency oracle checks declared fact groups (e.g. pump_status,
  stock_count). Oracle findings and scorer passes are separate
  verdicts — keep them separate in every report.
- `NOT_SIMULATED.md` is the honesty register of known blind spots
  (e.g. value-swap mutations currently escape every oracle). Tests
  fail if it loses an entry; if a change fixes a blind spot, move the
  entry to the regression tests and say so.

## Shared rules

- Use Unix LF line endings in every file; never CRLF.
- Never commit secrets, tokens, or credentials — real or synthetic-looking.
- Tests must pass before you describe a change as complete; run the test
  command above and report honestly if you cannot.
- Prefer the smallest complete implementation: reuse what already exists in
  this repo before adding new code, files, or dependencies.
