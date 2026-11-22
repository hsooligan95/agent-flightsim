---
mode: agent
description: Review the current diff against agent-flightsim's invariants
---

Review my current diff against this repo's invariants:

- Determinism is a hard contract: the CLI runs the grid twice and refuses to report if the passes differ; fixed seeds only.
- Simulate the world, never patch the agent to pass — the agent is the specimen, the twins and fault axes are the lab.
- Oracle findings and scorer passes are separate verdicts; keep them separate in every report.
- NOT_SIMULATED.md is the honesty register: tests fail if it loses an entry; a fixed blind spot moves to the regression tests.

Flag every violation with file and line. Also flag any change that
alters a documented behavior contract (output shapes, exit codes,
event schemas, recorded artifacts) without updating the docs and
tests that describe it. No style nitpicks — correctness and contract
violations only.
