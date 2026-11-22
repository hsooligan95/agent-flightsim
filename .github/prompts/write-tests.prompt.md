---
mode: agent
description: Write tests for a named module in agent-flightsim
---

Write tests for the module I name, following this repo's existing test
style, layout, and fixtures. Cover the behavior the module documents,
including these invariants where they apply:

- Determinism is a hard contract: the CLI runs the grid twice and refuses to report if the passes differ; fixed seeds only.
- Simulate the world, never patch the agent to pass — the agent is the specimen, the twins and fault axes are the lab.
- Oracle findings and scorer passes are separate verdicts; keep them separate in every report.

Then run the test suite:

    pytest
python run_flightsim.py   # full grid; must be byte-identical across double runs

Show the result. Do not claim done unless the suite is green; if a
test cannot pass, say why instead of weakening the assertion.
