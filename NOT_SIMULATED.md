# What AgentFlightSim does NOT simulate

The coverage map only shows the dimensions the sim models. Unmodeled
dimensions don't appear as gaps in the map — they don't appear at all —
so they are listed here, in the repo, next to the map. Read the map
with this register in hand.

## The agent

- **No real LLM.** The agent under test runs factory-floor-agent's
  deterministic extractive composer (the portfolio's offline stub).
  Findings characterize the *pipeline* — retrieval, grounding,
  freshness handling, source selection — not a production LLM's
  behavior. A stochastic model would make the map a sample, not a map;
  the sim takes the deterministic horn of that dilemma deliberately
  (see the Critic memo) and says so.
- **No tool use or side effects.** The agent retrieves from documents
  and answers. It does not call tools, write state, or actuate
  anything, so tool-error handling, partial writes, and irreversible
  actions are out of scope. (agent-chaos covers tool faults; this sim
  covers world state.)
- **No multi-turn conversation.** Every run is one question. Memory
  across turns, clarification dialogues, and context corruption over
  time are not modeled.
- **No multi-agent interaction.** One agent, one corpus. Handoffs,
  delegation, and agent-to-agent disagreement are not simulated.

## The world

- **One domain, two twins, one asset.** A factory floor, an inventory
  service, a maintenance service, one pump. The axes generalize; the
  fixtures don't pretend to.
- **Static dependency states.** "Degraded" and "down" are fixed corpus
  states for the whole run — not timed faults, retries, flapping,
  partial latency, or recovery mid-question.
- **Whole-document grid staleness.** On the grid, a document is fresh
  or stale as a unit. Per-fact staleness exists only in the fuzzing
  mutations (partial_stale), not as a grid axis.
- **Timestamps are trusted.** The freshness oracle reads header dates.
  The fuzzing results show a re-stamped stale document defeats it —
  content-level freshness (checksums against a source of truth) is
  not modeled.
- **Declared, not learned, contradictions.** The consistency oracle
  checks the attributes listed in the world's fact groups
  (pump_status, stock_location, stock_count). Two sources can disagree
  about anything else — return dates, order states, capacities — and
  no oracle will see it.

## The users

- **Three scripted question styles**, not calibrated user
  distributions. "Adversarial" means leading premises and an
  instruction to ignore a safety hold — not jailbreak research,
  not real attacker tradecraft, and not a sample of how actual users
  phrase anything.

## The measurements

- **Deterministic seeds.** Every number in the README reproduces
  exactly, because the stub agent is deterministic. That is the
  portfolio contract (clone, run, verify) — and it means the map is
  exact for this agent and says nothing probabilistic about any other.
- **No cost or latency model.** Runs are not timed or priced; a cell
  that passes slowly and expensively looks identical to a fast one.
- **Scorer terms encode one truth, partially.** The harness scorer
  checks expected terms drawn from world truth, and a case passes if
  ANY expected term appears. Facts no term pins down can be wrong
  invisibly: the fuzzing run proves it — a mutated stock count of 7
  (truth: 2) escaped every layer, because the scorer's terms for the
  stock cases name the location, not the count, and the consistency
  oracle's stock_count group detects *disagreement between sources*,
  not wrongness in a single source. The register entry above about
  declared contradictions applies to the scorer too.
