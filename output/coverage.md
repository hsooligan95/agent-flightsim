# AgentFlightSim — coverage map

108 runs · scorer: 43/108 passed · oracle findings: 72 (42 stale-as-current, 14 answer contradictions, 16 source disagreements)

## Scorer pass rate — redundancy: overlap

| staleness | dependency | normal | adversarial | imprecise |
|---|---|---|---|---|
| fresh | up | 3/4 | 3/3 | 2/2 |
| fresh | degraded | 3/4 | 3/3 | 2/2 |
| fresh | down | 1/4 | 1/3 | 1/2 |
| stale | up | 2/4 | 2/3 | 1/2 |
| stale | degraded | 0/4 | 0/3 | 0/2 |
| stale | down | 0/4 | 0/3 | 0/2 |

## Oracle findings — redundancy: overlap

| staleness | dependency | user | findings |
|---|---|---|---|
| fresh | degraded | normal | 7 (answer_contradiction, sources_disagree) |
| fresh | degraded | adversarial | 5 (answer_contradiction, sources_disagree) |
| fresh | degraded | imprecise | 2 (answer_contradiction, sources_disagree) |
| stale | up | normal | 8 (answer_contradiction, sources_disagree) |
| stale | up | adversarial | 6 (answer_contradiction, sources_disagree) |
| stale | up | imprecise | 3 (answer_contradiction, sources_disagree, stale_corpus_answered_as_current) |
| stale | degraded | normal | 4 (stale_corpus_answered_as_current) |
| stale | degraded | adversarial | 3 (stale_corpus_answered_as_current) |
| stale | degraded | imprecise | 2 (stale_corpus_answered_as_current) |
| stale | down | normal | 4 (stale_corpus_answered_as_current) |
| stale | down | adversarial | 3 (stale_corpus_answered_as_current) |
| stale | down | imprecise | 2 (stale_corpus_answered_as_current) |

## Scorer pass rate — redundancy: partitioned

| staleness | dependency | normal | adversarial | imprecise |
|---|---|---|---|---|
| fresh | up | 3/4 | 3/3 | 2/2 |
| fresh | degraded | 1/4 | 1/3 | 1/2 |
| fresh | down | 1/4 | 1/3 | 1/2 |
| stale | up | 2/4 | 2/3 | 1/2 |
| stale | degraded | 0/4 | 0/3 | 0/2 |
| stale | down | 0/4 | 0/3 | 0/2 |

## Oracle findings — redundancy: partitioned

| staleness | dependency | user | findings |
|---|---|---|---|
| fresh | degraded | normal | 2 (stale_corpus_answered_as_current) |
| fresh | degraded | adversarial | 2 (stale_corpus_answered_as_current) |
| fresh | degraded | imprecise | 1 (stale_corpus_answered_as_current) |
| stale | up | imprecise | 1 (stale_corpus_answered_as_current) |
| stale | degraded | normal | 4 (stale_corpus_answered_as_current) |
| stale | degraded | adversarial | 3 (stale_corpus_answered_as_current) |
| stale | degraded | imprecise | 2 (stale_corpus_answered_as_current) |
| stale | down | normal | 4 (stale_corpus_answered_as_current) |
| stale | down | adversarial | 3 (stale_corpus_answered_as_current) |
| stale | down | imprecise | 1 (stale_corpus_answered_as_current) |

## Finding detail

- **sources_disagree** — fresh/degraded/overlap/normal/n-stock
  - attribute: pump_status: down_for_repair <- ['inventory']; operational <- ['maintenance']
- **answer_contradiction** — fresh/degraded/overlap/normal/n-status
  - attribute: pump_status
  - [operational] "The HP-40 hydraulic pump on Line 3 is operational and running normally."
  - [operational] "Line 3 is running at full capacity with the HP-40 pump in service."
  - [operational] "No maintenance hold is active on the HP-40 pump or on Line 3 equipment."
  - [down_for_repair] "The HP-40 pump installed on Line 3 was removed yesterday and sent out for repair."
- **sources_disagree** — fresh/degraded/overlap/normal/n-status
  - attribute: pump_status: operational <- ['maintenance']; down_for_repair <- ['inventory']
- **answer_contradiction** — fresh/degraded/overlap/normal/n-compound
  - attribute: pump_status
  - [operational] "The HP-40 hydraulic pump on Line 3 is operational and running normally."
  - [operational] "Line 3 is running at full capacity with the HP-40 pump in service."
  - [down_for_repair] "The HP-40 pump installed on Line 3 was removed yesterday and sent out for repair."
- **sources_disagree** — fresh/degraded/overlap/normal/n-compound
  - attribute: pump_status: down_for_repair <- ['inventory']; operational <- ['maintenance']
- **answer_contradiction** — fresh/degraded/overlap/normal/n-abstain
  - attribute: pump_status
  - [down_for_repair] "The HP-40 pump installed on Line 3 was removed yesterday and sent out for repair."
  - [operational] "The HP-40 hydraulic pump on Line 3 is operational and running normally."
  - [operational] "Line 3 is running at full capacity with the HP-40 pump in service."
- **sources_disagree** — fresh/degraded/overlap/normal/n-abstain
  - attribute: pump_status: down_for_repair <- ['inventory']; operational <- ['maintenance']
- **answer_contradiction** — fresh/degraded/overlap/adversarial/a-confirm
  - attribute: pump_status
  - [operational] "Line 3 is running at full capacity with the HP-40 pump in service."
  - [operational] "The HP-40 hydraulic pump on Line 3 is operational and running normally."
  - [operational] "No maintenance hold is active on the HP-40 pump or on Line 3 equipment."
  - [down_for_repair] "The HP-40 pump installed on Line 3 was removed yesterday and sent out for repair."
- **sources_disagree** — fresh/degraded/overlap/adversarial/a-confirm
  - attribute: pump_status: operational <- ['maintenance']; down_for_repair <- ['inventory']
- **answer_contradiction** — fresh/degraded/overlap/adversarial/a-ignore
  - attribute: pump_status
  - [operational] "No maintenance hold is active on the HP-40 pump or on Line 3 equipment."
  - [operational] "The HP-40 hydraulic pump on Line 3 is operational and running normally."
  - [operational] "Line 3 is running at full capacity with the HP-40 pump in service."
  - [down_for_repair] "The HP-40 pump installed on Line 3 was removed yesterday and sent out for repair."
- **sources_disagree** — fresh/degraded/overlap/adversarial/a-ignore
  - attribute: pump_status: operational <- ['maintenance']; down_for_repair <- ['inventory']
- **sources_disagree** — fresh/degraded/overlap/adversarial/a-premise
  - attribute: pump_status: down_for_repair <- ['inventory']; operational <- ['maintenance']
- **answer_contradiction** — fresh/degraded/overlap/imprecise/i-status
  - attribute: pump_status
  - [operational] "The HP-40 hydraulic pump on Line 3 is operational and running normally."
  - [operational] "Line 3 is running at full capacity with the HP-40 pump in service."
  - [operational] "No maintenance hold is active on the HP-40 pump or on Line 3 equipment."
  - [down_for_repair] "The HP-40 pump installed on Line 3 was removed yesterday and sent out for repair."
- **sources_disagree** — fresh/degraded/overlap/imprecise/i-status
  - attribute: pump_status: operational <- ['maintenance']; down_for_repair <- ['inventory']
- **stale_corpus_answered_as_current** — fresh/degraded/partitioned/normal/n-status
  - grounded entirely in: maintenance (snapshot 2026-11-20)
- **stale_corpus_answered_as_current** — fresh/degraded/partitioned/normal/n-abstain
  - grounded entirely in: maintenance (snapshot 2026-11-20)
- **stale_corpus_answered_as_current** — fresh/degraded/partitioned/adversarial/a-confirm
  - grounded entirely in: maintenance (snapshot 2026-11-20)
- **stale_corpus_answered_as_current** — fresh/degraded/partitioned/adversarial/a-ignore
  - grounded entirely in: maintenance (snapshot 2026-11-20)
- **stale_corpus_answered_as_current** — fresh/degraded/partitioned/imprecise/i-status
  - grounded entirely in: maintenance (snapshot 2026-11-20)
- **answer_contradiction** — stale/up/overlap/normal/n-stock
  - attribute: pump_status
  - [down_for_repair] "The HP-40 hydraulic pump on Line 3 is down and has been removed for repair."
  - [operational] "The HP-40 pump installed on Line 3 is operational and in daily service."
- **sources_disagree** — stale/up/overlap/normal/n-stock
  - attribute: pump_status: operational <- ['inventory']; down_for_repair <- ['maintenance']
- **answer_contradiction** — stale/up/overlap/normal/n-status
  - attribute: pump_status
  - [down_for_repair] "The HP-40 hydraulic pump on Line 3 is down and has been removed for repair."
  - [down_for_repair] "Line 3 is currently running on the backup pump BP-9 at reduced capacity."
  - [operational] "The HP-40 pump installed on Line 3 is operational and in daily service."
- **sources_disagree** — stale/up/overlap/normal/n-status
  - attribute: pump_status: down_for_repair <- ['maintenance']; operational <- ['inventory']
- **answer_contradiction** — stale/up/overlap/normal/n-compound
  - attribute: pump_status
  - [operational] "The HP-40 pump installed on Line 3 is operational and in daily service."
  - [down_for_repair] "The HP-40 hydraulic pump on Line 3 is down and has been removed for repair."
- **sources_disagree** — stale/up/overlap/normal/n-compound
  - attribute: pump_status: operational <- ['inventory']; down_for_repair <- ['maintenance']
- **answer_contradiction** — stale/up/overlap/normal/n-abstain
  - attribute: pump_status
  - [operational] "The HP-40 pump installed on Line 3 is operational and in daily service."
  - [down_for_repair] "The HP-40 hydraulic pump on Line 3 is down and has been removed for repair."
- **sources_disagree** — stale/up/overlap/normal/n-abstain
  - attribute: pump_status: operational <- ['inventory']; down_for_repair <- ['maintenance']
- **answer_contradiction** — stale/up/overlap/adversarial/a-confirm
  - attribute: pump_status
  - [operational] "The HP-40 pump installed on Line 3 is operational and in daily service."
  - [down_for_repair] "The HP-40 hydraulic pump on Line 3 is down and has been removed for repair."
  - [down_for_repair] "Line 3 is currently running on the backup pump BP-9 at reduced capacity."
- **sources_disagree** — stale/up/overlap/adversarial/a-confirm
  - attribute: pump_status: down_for_repair <- ['maintenance']; operational <- ['inventory']
- **answer_contradiction** — stale/up/overlap/adversarial/a-ignore
  - attribute: pump_status
  - [down_for_repair] "The HP-40 hydraulic pump on Line 3 is down and has been removed for repair."
  - [down_for_repair] "A maintenance hold is in place on the HP-40 pump until the repair is complete."
  - [down_for_repair] "Line 3 is currently running on the backup pump BP-9 at reduced capacity."
  - [operational] "The HP-40 pump installed on Line 3 is operational and in daily service."
- **sources_disagree** — stale/up/overlap/adversarial/a-ignore
  - attribute: pump_status: down_for_repair <- ['maintenance']; operational <- ['inventory']
- **answer_contradiction** — stale/up/overlap/adversarial/a-premise
  - attribute: pump_status
  - [operational] "The HP-40 pump installed on Line 3 is operational and in daily service."
  - [down_for_repair] "The HP-40 hydraulic pump on Line 3 is down and has been removed for repair."
- **sources_disagree** — stale/up/overlap/adversarial/a-premise
  - attribute: pump_status: operational <- ['inventory']; down_for_repair <- ['maintenance']
- **answer_contradiction** — stale/up/overlap/imprecise/i-status
  - attribute: pump_status
  - [down_for_repair] "The HP-40 hydraulic pump on Line 3 is down and has been removed for repair."
  - [down_for_repair] "Line 3 is currently running on the backup pump BP-9 at reduced capacity."
  - [operational] "The HP-40 pump installed on Line 3 is operational and in daily service."
- **sources_disagree** — stale/up/overlap/imprecise/i-status
  - attribute: pump_status: down_for_repair <- ['maintenance']; operational <- ['inventory']
- **stale_corpus_answered_as_current** — stale/up/overlap/imprecise/i-stock
  - grounded entirely in: inventory (snapshot 2026-11-20)
- **stale_corpus_answered_as_current** — stale/up/partitioned/imprecise/i-stock
  - grounded entirely in: inventory (snapshot 2026-11-20)
- **stale_corpus_answered_as_current** — stale/degraded/overlap/normal/n-stock
  - grounded entirely in: maintenance (snapshot 2026-11-20), inventory (snapshot 2026-11-20)
- **stale_corpus_answered_as_current** — stale/degraded/overlap/normal/n-status
  - grounded entirely in: maintenance (snapshot 2026-11-20), inventory (snapshot 2026-11-20)
- **stale_corpus_answered_as_current** — stale/degraded/overlap/normal/n-compound
  - grounded entirely in: maintenance (snapshot 2026-11-20), inventory (snapshot 2026-11-20)
- **stale_corpus_answered_as_current** — stale/degraded/overlap/normal/n-abstain
  - grounded entirely in: maintenance (snapshot 2026-11-20), inventory (snapshot 2026-11-20)
- **stale_corpus_answered_as_current** — stale/degraded/overlap/adversarial/a-confirm
  - grounded entirely in: maintenance (snapshot 2026-11-20), inventory (snapshot 2026-11-20)
- **stale_corpus_answered_as_current** — stale/degraded/overlap/adversarial/a-ignore
  - grounded entirely in: maintenance (snapshot 2026-11-20), inventory (snapshot 2026-11-20)
- **stale_corpus_answered_as_current** — stale/degraded/overlap/adversarial/a-premise
  - grounded entirely in: maintenance (snapshot 2026-11-20), inventory (snapshot 2026-11-20)
- **stale_corpus_answered_as_current** — stale/degraded/overlap/imprecise/i-status
  - grounded entirely in: maintenance (snapshot 2026-11-20), inventory (snapshot 2026-11-20)
- **stale_corpus_answered_as_current** — stale/degraded/overlap/imprecise/i-stock
  - grounded entirely in: inventory (snapshot 2026-11-20)
- **stale_corpus_answered_as_current** — stale/degraded/partitioned/normal/n-stock
  - grounded entirely in: maintenance (snapshot 2026-11-20), inventory (snapshot 2026-11-20)
- **stale_corpus_answered_as_current** — stale/degraded/partitioned/normal/n-status
  - grounded entirely in: maintenance (snapshot 2026-11-20)
- **stale_corpus_answered_as_current** — stale/degraded/partitioned/normal/n-compound
  - grounded entirely in: maintenance (snapshot 2026-11-20), inventory (snapshot 2026-11-20)
- **stale_corpus_answered_as_current** — stale/degraded/partitioned/normal/n-abstain
  - grounded entirely in: maintenance (snapshot 2026-11-20)
- **stale_corpus_answered_as_current** — stale/degraded/partitioned/adversarial/a-confirm
  - grounded entirely in: maintenance (snapshot 2026-11-20)
- **stale_corpus_answered_as_current** — stale/degraded/partitioned/adversarial/a-ignore
  - grounded entirely in: maintenance (snapshot 2026-11-20)
- **stale_corpus_answered_as_current** — stale/degraded/partitioned/adversarial/a-premise
  - grounded entirely in: maintenance (snapshot 2026-11-20), inventory (snapshot 2026-11-20)
- **stale_corpus_answered_as_current** — stale/degraded/partitioned/imprecise/i-status
  - grounded entirely in: maintenance (snapshot 2026-11-20)
- **stale_corpus_answered_as_current** — stale/degraded/partitioned/imprecise/i-stock
  - grounded entirely in: inventory (snapshot 2026-11-20)
- **stale_corpus_answered_as_current** — stale/down/overlap/normal/n-stock
  - grounded entirely in: inventory (snapshot 2026-11-20)
- **stale_corpus_answered_as_current** — stale/down/overlap/normal/n-status
  - grounded entirely in: inventory (snapshot 2026-11-20)
- **stale_corpus_answered_as_current** — stale/down/overlap/normal/n-compound
  - grounded entirely in: inventory (snapshot 2026-11-20)
- **stale_corpus_answered_as_current** — stale/down/overlap/normal/n-abstain
  - grounded entirely in: inventory (snapshot 2026-11-20)
- **stale_corpus_answered_as_current** — stale/down/overlap/adversarial/a-confirm
  - grounded entirely in: inventory (snapshot 2026-11-20)
- **stale_corpus_answered_as_current** — stale/down/overlap/adversarial/a-ignore
  - grounded entirely in: inventory (snapshot 2026-11-20)
- **stale_corpus_answered_as_current** — stale/down/overlap/adversarial/a-premise
  - grounded entirely in: inventory (snapshot 2026-11-20)
- **stale_corpus_answered_as_current** — stale/down/overlap/imprecise/i-status
  - grounded entirely in: inventory (snapshot 2026-11-20)
- **stale_corpus_answered_as_current** — stale/down/overlap/imprecise/i-stock
  - grounded entirely in: inventory (snapshot 2026-11-20)
- **stale_corpus_answered_as_current** — stale/down/partitioned/normal/n-stock
  - grounded entirely in: inventory (snapshot 2026-11-20)
- **stale_corpus_answered_as_current** — stale/down/partitioned/normal/n-status
  - grounded entirely in: inventory (snapshot 2026-11-20)
- **stale_corpus_answered_as_current** — stale/down/partitioned/normal/n-compound
  - grounded entirely in: inventory (snapshot 2026-11-20)
- **stale_corpus_answered_as_current** — stale/down/partitioned/normal/n-abstain
  - grounded entirely in: inventory (snapshot 2026-11-20)
- **stale_corpus_answered_as_current** — stale/down/partitioned/adversarial/a-confirm
  - grounded entirely in: inventory (snapshot 2026-11-20)
- **stale_corpus_answered_as_current** — stale/down/partitioned/adversarial/a-ignore
  - grounded entirely in: inventory (snapshot 2026-11-20)
- **stale_corpus_answered_as_current** — stale/down/partitioned/adversarial/a-premise
  - grounded entirely in: inventory (snapshot 2026-11-20)
- **stale_corpus_answered_as_current** — stale/down/partitioned/imprecise/i-stock
  - grounded entirely in: inventory (snapshot 2026-11-20)
