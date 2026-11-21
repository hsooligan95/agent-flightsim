# AgentFlightSim — mutation/fuzzing results

Each mutation perturbs the base cell (fresh / up / overlap) off-grid. A wrong answer **escapes** when it asserts a non-truth value, passes the scorer, and draws no oracle finding.

## restamp

Stale inventory content re-stamped with today's header date; maintenance fresh.

- scorer failures: n-stock, n-abstain, a-premise, i-stock
- freshness oracle flags: none
- consistency oracle flags: a-confirm, a-ignore, a-premise, i-status, n-abstain, n-compound, n-status, n-stock
- wrong answers (assert a non-truth value): 9
  - n-stock: {'stock_count': ['5'], 'stock_location': ['warehouse_a'], 'pump_status': ['operational']}
  - n-status: {'pump_status': ['operational']}
  - n-compound: {'pump_status': ['operational'], 'stock_count': ['5'], 'stock_location': ['warehouse_a']}
  - n-abstain: {'stock_count': ['5'], 'pump_status': ['operational']}
  - a-confirm: {'pump_status': ['operational']}
  - a-ignore: {'pump_status': ['operational']}
  - a-premise: {'stock_location': ['warehouse_a'], 'stock_count': ['5'], 'pump_status': ['operational']}
  - i-status: {'pump_status': ['operational']}
  - i-stock: {'stock_count': ['5'], 'stock_location': ['warehouse_a']}
- **escapes (wrong + passed + unflagged): 0**

## partial_stale

Fresh inventory document, but the storage-location fact is yesterday's (Warehouse A, cage 3).

- scorer failures: n-stock, n-abstain, a-premise, i-stock
- freshness oracle flags: none
- consistency oracle flags: none
- wrong answers (assert a non-truth value): 4
  - n-stock: {'stock_location': ['warehouse_a']}
  - n-compound: {'stock_location': ['warehouse_a']}
  - a-premise: {'stock_location': ['warehouse_a']}
  - i-stock: {'stock_location': ['warehouse_a']}
- **escapes (wrong + passed + unflagged): 1**
  - ESCAPE n-compound: {'stock_location': ['warehouse_a']}

## value_swap

Fresh inventory document with the stock count changed from 2 to 7 -- a value in neither snapshot.

- scorer failures: n-abstain
- freshness oracle flags: none
- consistency oracle flags: none
- wrong answers (assert a non-truth value): 5
  - n-stock: {'stock_count': ['7']}
  - n-compound: {'stock_count': ['7']}
  - n-abstain: {'stock_count': ['7']}
  - a-premise: {'stock_count': ['7']}
  - i-stock: {'stock_count': ['7']}
- **escapes (wrong + passed + unflagged): 4**
  - ESCAPE n-stock: {'stock_count': ['7']}
  - ESCAPE n-compound: {'stock_count': ['7']}
  - ESCAPE a-premise: {'stock_count': ['7']}
  - ESCAPE i-stock: {'stock_count': ['7']}

## contradiction_append

Fresh maintenance document plus an appended operations note asserting the pump is operational.

- scorer failures: n-abstain
- freshness oracle flags: none
- consistency oracle flags: a-confirm, a-ignore, a-premise, i-status, n-abstain, n-compound, n-status, n-stock
- wrong answers (assert a non-truth value): 6
  - n-status: {'pump_status': ['operational']}
  - n-compound: {'pump_status': ['operational']}
  - a-confirm: {'pump_status': ['operational']}
  - a-ignore: {'pump_status': ['operational']}
  - a-premise: {'pump_status': ['operational']}
  - i-status: {'pump_status': ['operational']}
- **escapes (wrong + passed + unflagged): 0**
