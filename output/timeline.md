# AgentFlightSim — batches in the AgentTrace store

Trace ID(s): `flightsim-fuzz-20261121`, `flightsim-grid-20261121` · 146 events · sources: agent-flightsim
**Chain OK — 146 events, every hash verified.**

```
flightsim-fuzz-20261121
├── agent-flightsim (36 events)
│   #111 2026-11-21T06:00:00Z  batch_started      
│   #112 2026-11-21T06:01:00Z  mutation_completed 
│   #113 2026-11-21T06:02:00Z  oracle_finding     
│   #114 2026-11-21T06:03:00Z  oracle_finding     
│   #115 2026-11-21T06:04:00Z  oracle_finding     
│   #116 2026-11-21T06:05:00Z  oracle_finding     
│   #117 2026-11-21T06:06:00Z  oracle_finding     
│   #118 2026-11-21T06:07:00Z  oracle_finding     
│   #119 2026-11-21T06:08:00Z  oracle_finding     
│   #120 2026-11-21T06:09:00Z  oracle_finding     
│   #121 2026-11-21T06:10:00Z  oracle_finding     
│   #122 2026-11-21T06:11:00Z  oracle_finding     
│   #123 2026-11-21T06:12:00Z  oracle_finding     
│   #124 2026-11-21T06:13:00Z  oracle_finding     
│   #125 2026-11-21T06:14:00Z  oracle_finding     
│   #126 2026-11-21T06:15:00Z  oracle_finding     
│   #127 2026-11-21T06:16:00Z  oracle_finding     
│   #128 2026-11-21T06:17:00Z  oracle_finding     
│   #129 2026-11-21T06:18:00Z  mutation_completed 
│   #130 2026-11-21T06:19:00Z  mutation_completed 
│   #131 2026-11-21T06:20:00Z  mutation_completed 
│   #132 2026-11-21T06:21:00Z  oracle_finding     
│   #133 2026-11-21T06:22:00Z  oracle_finding     
│   #134 2026-11-21T06:23:00Z  oracle_finding     
│   #135 2026-11-21T06:24:00Z  oracle_finding     
│   #136 2026-11-21T06:25:00Z  oracle_finding     
│   #137 2026-11-21T06:26:00Z  oracle_finding     
│   #138 2026-11-21T06:27:00Z  oracle_finding     
│   #139 2026-11-21T06:28:00Z  oracle_finding     
│   #140 2026-11-21T06:29:00Z  oracle_finding     
│   #141 2026-11-21T06:30:00Z  oracle_finding     
│   #142 2026-11-21T06:31:00Z  oracle_finding     
│   #143 2026-11-21T06:32:00Z  oracle_finding     
│   #144 2026-11-21T06:33:00Z  oracle_finding     
│   #145 2026-11-21T06:34:00Z  oracle_finding     
│   #146 2026-11-21T06:35:00Z  batch_verdict      DECISION flightsim_fuzz_batch_verdict: 4 mutations run; 5 wrong answer(s) escaped every layer (decider=None, computed=None)
flightsim-grid-20261121
├── agent-flightsim (110 events)
│   #  1 2026-11-21T06:00:00Z  batch_started      
│   #  2 2026-11-21T06:01:00Z  cell_completed     
│   #  3 2026-11-21T06:02:00Z  cell_completed     
│   #  4 2026-11-21T06:03:00Z  cell_completed     
│   #  5 2026-11-21T06:04:00Z  cell_completed     
│   #  6 2026-11-21T06:05:00Z  cell_completed     
│   #  7 2026-11-21T06:06:00Z  cell_completed     
│   #  8 2026-11-21T06:07:00Z  cell_completed     
│   #  9 2026-11-21T06:08:00Z  oracle_finding     
│   # 10 2026-11-21T06:09:00Z  oracle_finding     
│   # 11 2026-11-21T06:10:00Z  oracle_finding     
│   # 12 2026-11-21T06:11:00Z  oracle_finding     
│   # 13 2026-11-21T06:12:00Z  oracle_finding     
│   # 14 2026-11-21T06:13:00Z  oracle_finding     
│   # 15 2026-11-21T06:14:00Z  oracle_finding     
│   # 16 2026-11-21T06:15:00Z  cell_completed     
│   # 17 2026-11-21T06:16:00Z  oracle_finding     
│   # 18 2026-11-21T06:17:00Z  oracle_finding     
│   # 19 2026-11-21T06:18:00Z  oracle_finding     
│   # 20 2026-11-21T06:19:00Z  oracle_finding     
│   # 21 2026-11-21T06:20:00Z  oracle_finding     
│   # 22 2026-11-21T06:21:00Z  cell_completed     
│   # 23 2026-11-21T06:22:00Z  oracle_finding     
│   # 24 2026-11-21T06:23:00Z  oracle_finding     
│   # 25 2026-11-21T06:24:00Z  cell_completed     
│   # 26 2026-11-21T06:25:00Z  oracle_finding     
│   # 27 2026-11-21T06:26:00Z  oracle_finding     
│   # 28 2026-11-21T06:27:00Z  cell_completed     
│   # 29 2026-11-21T06:28:00Z  oracle_finding     
│   # 30 2026-11-21T06:29:00Z  oracle_finding     
│   # 31 2026-11-21T06:30:00Z  cell_completed     
│   # 32 2026-11-21T06:31:00Z  oracle_finding     
│   # 33 2026-11-21T06:32:00Z  cell_completed     
│   # 34 2026-11-21T06:33:00Z  cell_completed     
│   # 35 2026-11-21T06:34:00Z  cell_completed     
│   # 36 2026-11-21T06:35:00Z  cell_completed     
│   # 37 2026-11-21T06:36:00Z  cell_completed     
│   # 38 2026-11-21T06:37:00Z  cell_completed     
│   # 39 2026-11-21T06:38:00Z  cell_completed     
│   # 40 2026-11-21T06:39:00Z  oracle_finding     
│   # 41 2026-11-21T06:40:00Z  oracle_finding     
│   # 42 2026-11-21T06:41:00Z  oracle_finding     
│   # 43 2026-11-21T06:42:00Z  oracle_finding     
│   # 44 2026-11-21T06:43:00Z  oracle_finding     
│   # 45 2026-11-21T06:44:00Z  oracle_finding     
│   # 46 2026-11-21T06:45:00Z  oracle_finding     
│   # 47 2026-11-21T06:46:00Z  oracle_finding     
│   # 48 2026-11-21T06:47:00Z  cell_completed     
│   # 49 2026-11-21T06:48:00Z  oracle_finding     
│   # 50 2026-11-21T06:49:00Z  oracle_finding     
│   # 51 2026-11-21T06:50:00Z  oracle_finding     
│   # 52 2026-11-21T06:51:00Z  oracle_finding     
│   # 53 2026-11-21T06:52:00Z  oracle_finding     
│   # 54 2026-11-21T06:53:00Z  oracle_finding     
│   # 55 2026-11-21T06:54:00Z  cell_completed     
│   # 56 2026-11-21T06:55:00Z  oracle_finding     
│   # 57 2026-11-21T06:56:00Z  oracle_finding     
│   # 58 2026-11-21T06:57:00Z  oracle_finding     
│   # 59 2026-11-21T06:58:00Z  cell_completed     
│   # 60 2026-11-21T06:59:00Z  cell_completed     
│   # 61 2026-11-21T07:00:00Z  cell_completed     
│   # 62 2026-11-21T07:01:00Z  oracle_finding     
│   # 63 2026-11-21T07:02:00Z  cell_completed     
│   # 64 2026-11-21T07:03:00Z  oracle_finding     
│   # 65 2026-11-21T07:04:00Z  oracle_finding     
│   # 66 2026-11-21T07:05:00Z  oracle_finding     
│   # 67 2026-11-21T07:06:00Z  oracle_finding     
│   # 68 2026-11-21T07:07:00Z  cell_completed     
│   # 69 2026-11-21T07:08:00Z  oracle_finding     
│   # 70 2026-11-21T07:09:00Z  oracle_finding     
│   # 71 2026-11-21T07:10:00Z  oracle_finding     
│   # 72 2026-11-21T07:11:00Z  cell_completed     
│   # 73 2026-11-21T07:12:00Z  oracle_finding     
│   # 74 2026-11-21T07:13:00Z  oracle_finding     
│   # 75 2026-11-21T07:14:00Z  cell_completed     
│   # 76 2026-11-21T07:15:00Z  oracle_finding     
│   # 77 2026-11-21T07:16:00Z  oracle_finding     
│   # 78 2026-11-21T07:17:00Z  oracle_finding     
│   # 79 2026-11-21T07:18:00Z  oracle_finding     
│   # 80 2026-11-21T07:19:00Z  cell_completed     
│   # 81 2026-11-21T07:20:00Z  oracle_finding     
│   # 82 2026-11-21T07:21:00Z  oracle_finding     
│   # 83 2026-11-21T07:22:00Z  oracle_finding     
│   # 84 2026-11-21T07:23:00Z  cell_completed     
│   # 85 2026-11-21T07:24:00Z  oracle_finding     
│   # 86 2026-11-21T07:25:00Z  oracle_finding     
│   # 87 2026-11-21T07:26:00Z  cell_completed     
│   # 88 2026-11-21T07:27:00Z  oracle_finding     
│   # 89 2026-11-21T07:28:00Z  oracle_finding     
│   # 90 2026-11-21T07:29:00Z  oracle_finding     
│   # 91 2026-11-21T07:30:00Z  oracle_finding     
│   # 92 2026-11-21T07:31:00Z  cell_completed     
│   # 93 2026-11-21T07:32:00Z  oracle_finding     
│   # 94 2026-11-21T07:33:00Z  oracle_finding     
│   # 95 2026-11-21T07:34:00Z  oracle_finding     
│   # 96 2026-11-21T07:35:00Z  cell_completed     
│   # 97 2026-11-21T07:36:00Z  oracle_finding     
│   # 98 2026-11-21T07:37:00Z  oracle_finding     
│   # 99 2026-11-21T07:38:00Z  cell_completed     
│   #100 2026-11-21T07:39:00Z  oracle_finding     
│   #101 2026-11-21T07:40:00Z  oracle_finding     
│   #102 2026-11-21T07:41:00Z  oracle_finding     
│   #103 2026-11-21T07:42:00Z  oracle_finding     
│   #104 2026-11-21T07:43:00Z  cell_completed     
│   #105 2026-11-21T07:44:00Z  oracle_finding     
│   #106 2026-11-21T07:45:00Z  oracle_finding     
│   #107 2026-11-21T07:46:00Z  oracle_finding     
│   #108 2026-11-21T07:47:00Z  cell_completed     
│   #109 2026-11-21T07:48:00Z  oracle_finding     
│   #110 2026-11-21T07:49:00Z  batch_verdict      DECISION flightsim_grid_batch_verdict: 43/108 runs passed the scorer; 72 oracle findings (decider=None, computed=None)
```

## Decision records (computed decision points only)

- #110 **flightsim_grid_batch_verdict** -> **43/108 runs passed the scorer; 72 oracle findings**
  - oracle finding classes: answer_contradiction, sources_disagree, stale_corpus_answered_as_current
  - cells fully clean: 4/36
- #146 **flightsim_fuzz_batch_verdict** -> **4 mutations run; 5 wrong answer(s) escaped every layer**
  - restamp: escapes=0
  - partial_stale: escapes=1
  - value_swap: escapes=4
  - contradiction_append: escapes=0

## Timeline (store order)

- #  1 `2026-11-21T06:00:00Z` **agent-flightsim** — batch_started — 
- #  2 `2026-11-21T06:01:00Z` **agent-flightsim** — cell_completed — 
- #  3 `2026-11-21T06:02:00Z` **agent-flightsim** — cell_completed — 
- #  4 `2026-11-21T06:03:00Z` **agent-flightsim** — cell_completed — 
- #  5 `2026-11-21T06:04:00Z` **agent-flightsim** — cell_completed — 
- #  6 `2026-11-21T06:05:00Z` **agent-flightsim** — cell_completed — 
- #  7 `2026-11-21T06:06:00Z` **agent-flightsim** — cell_completed — 
- #  8 `2026-11-21T06:07:00Z` **agent-flightsim** — cell_completed — 
- #  9 `2026-11-21T06:08:00Z` **agent-flightsim** — oracle_finding — 
- # 10 `2026-11-21T06:09:00Z` **agent-flightsim** — oracle_finding — 
- # 11 `2026-11-21T06:10:00Z` **agent-flightsim** — oracle_finding — 
- # 12 `2026-11-21T06:11:00Z` **agent-flightsim** — oracle_finding — 
- # 13 `2026-11-21T06:12:00Z` **agent-flightsim** — oracle_finding — 
- # 14 `2026-11-21T06:13:00Z` **agent-flightsim** — oracle_finding — 
- # 15 `2026-11-21T06:14:00Z` **agent-flightsim** — oracle_finding — 
- # 16 `2026-11-21T06:15:00Z` **agent-flightsim** — cell_completed — 
- # 17 `2026-11-21T06:16:00Z` **agent-flightsim** — oracle_finding — 
- # 18 `2026-11-21T06:17:00Z` **agent-flightsim** — oracle_finding — 
- # 19 `2026-11-21T06:18:00Z` **agent-flightsim** — oracle_finding — 
- # 20 `2026-11-21T06:19:00Z` **agent-flightsim** — oracle_finding — 
- # 21 `2026-11-21T06:20:00Z` **agent-flightsim** — oracle_finding — 
- # 22 `2026-11-21T06:21:00Z` **agent-flightsim** — cell_completed — 
- # 23 `2026-11-21T06:22:00Z` **agent-flightsim** — oracle_finding — 
- # 24 `2026-11-21T06:23:00Z` **agent-flightsim** — oracle_finding — 
- # 25 `2026-11-21T06:24:00Z` **agent-flightsim** — cell_completed — 
- # 26 `2026-11-21T06:25:00Z` **agent-flightsim** — oracle_finding — 
- # 27 `2026-11-21T06:26:00Z` **agent-flightsim** — oracle_finding — 
- # 28 `2026-11-21T06:27:00Z` **agent-flightsim** — cell_completed — 
- # 29 `2026-11-21T06:28:00Z` **agent-flightsim** — oracle_finding — 
- # 30 `2026-11-21T06:29:00Z` **agent-flightsim** — oracle_finding — 
- # 31 `2026-11-21T06:30:00Z` **agent-flightsim** — cell_completed — 
- # 32 `2026-11-21T06:31:00Z` **agent-flightsim** — oracle_finding — 
- # 33 `2026-11-21T06:32:00Z` **agent-flightsim** — cell_completed — 
- # 34 `2026-11-21T06:33:00Z` **agent-flightsim** — cell_completed — 
- # 35 `2026-11-21T06:34:00Z` **agent-flightsim** — cell_completed — 
- # 36 `2026-11-21T06:35:00Z` **agent-flightsim** — cell_completed — 
- # 37 `2026-11-21T06:36:00Z` **agent-flightsim** — cell_completed — 
- # 38 `2026-11-21T06:37:00Z` **agent-flightsim** — cell_completed — 
- # 39 `2026-11-21T06:38:00Z` **agent-flightsim** — cell_completed — 
- # 40 `2026-11-21T06:39:00Z` **agent-flightsim** — oracle_finding — 
- # 41 `2026-11-21T06:40:00Z` **agent-flightsim** — oracle_finding — 
- # 42 `2026-11-21T06:41:00Z` **agent-flightsim** — oracle_finding — 
- # 43 `2026-11-21T06:42:00Z` **agent-flightsim** — oracle_finding — 
- # 44 `2026-11-21T06:43:00Z` **agent-flightsim** — oracle_finding — 
- # 45 `2026-11-21T06:44:00Z` **agent-flightsim** — oracle_finding — 
- # 46 `2026-11-21T06:45:00Z` **agent-flightsim** — oracle_finding — 
- # 47 `2026-11-21T06:46:00Z` **agent-flightsim** — oracle_finding — 
- # 48 `2026-11-21T06:47:00Z` **agent-flightsim** — cell_completed — 
- # 49 `2026-11-21T06:48:00Z` **agent-flightsim** — oracle_finding — 
- # 50 `2026-11-21T06:49:00Z` **agent-flightsim** — oracle_finding — 
- # 51 `2026-11-21T06:50:00Z` **agent-flightsim** — oracle_finding — 
- # 52 `2026-11-21T06:51:00Z` **agent-flightsim** — oracle_finding — 
- # 53 `2026-11-21T06:52:00Z` **agent-flightsim** — oracle_finding — 
- # 54 `2026-11-21T06:53:00Z` **agent-flightsim** — oracle_finding — 
- # 55 `2026-11-21T06:54:00Z` **agent-flightsim** — cell_completed — 
- # 56 `2026-11-21T06:55:00Z` **agent-flightsim** — oracle_finding — 
- # 57 `2026-11-21T06:56:00Z` **agent-flightsim** — oracle_finding — 
- # 58 `2026-11-21T06:57:00Z` **agent-flightsim** — oracle_finding — 
- # 59 `2026-11-21T06:58:00Z` **agent-flightsim** — cell_completed — 
- # 60 `2026-11-21T06:59:00Z` **agent-flightsim** — cell_completed — 
- # 61 `2026-11-21T07:00:00Z` **agent-flightsim** — cell_completed — 
- # 62 `2026-11-21T07:01:00Z` **agent-flightsim** — oracle_finding — 
- # 63 `2026-11-21T07:02:00Z` **agent-flightsim** — cell_completed — 
- # 64 `2026-11-21T07:03:00Z` **agent-flightsim** — oracle_finding — 
- # 65 `2026-11-21T07:04:00Z` **agent-flightsim** — oracle_finding — 
- # 66 `2026-11-21T07:05:00Z` **agent-flightsim** — oracle_finding — 
- # 67 `2026-11-21T07:06:00Z` **agent-flightsim** — oracle_finding — 
- # 68 `2026-11-21T07:07:00Z` **agent-flightsim** — cell_completed — 
- # 69 `2026-11-21T07:08:00Z` **agent-flightsim** — oracle_finding — 
- # 70 `2026-11-21T07:09:00Z` **agent-flightsim** — oracle_finding — 
- # 71 `2026-11-21T07:10:00Z` **agent-flightsim** — oracle_finding — 
- # 72 `2026-11-21T07:11:00Z` **agent-flightsim** — cell_completed — 
- # 73 `2026-11-21T07:12:00Z` **agent-flightsim** — oracle_finding — 
- # 74 `2026-11-21T07:13:00Z` **agent-flightsim** — oracle_finding — 
- # 75 `2026-11-21T07:14:00Z` **agent-flightsim** — cell_completed — 
- # 76 `2026-11-21T07:15:00Z` **agent-flightsim** — oracle_finding — 
- # 77 `2026-11-21T07:16:00Z` **agent-flightsim** — oracle_finding — 
- # 78 `2026-11-21T07:17:00Z` **agent-flightsim** — oracle_finding — 
- # 79 `2026-11-21T07:18:00Z` **agent-flightsim** — oracle_finding — 
- # 80 `2026-11-21T07:19:00Z` **agent-flightsim** — cell_completed — 
- # 81 `2026-11-21T07:20:00Z` **agent-flightsim** — oracle_finding — 
- # 82 `2026-11-21T07:21:00Z` **agent-flightsim** — oracle_finding — 
- # 83 `2026-11-21T07:22:00Z` **agent-flightsim** — oracle_finding — 
- # 84 `2026-11-21T07:23:00Z` **agent-flightsim** — cell_completed — 
- # 85 `2026-11-21T07:24:00Z` **agent-flightsim** — oracle_finding — 
- # 86 `2026-11-21T07:25:00Z` **agent-flightsim** — oracle_finding — 
- # 87 `2026-11-21T07:26:00Z` **agent-flightsim** — cell_completed — 
- # 88 `2026-11-21T07:27:00Z` **agent-flightsim** — oracle_finding — 
- # 89 `2026-11-21T07:28:00Z` **agent-flightsim** — oracle_finding — 
- # 90 `2026-11-21T07:29:00Z` **agent-flightsim** — oracle_finding — 
- # 91 `2026-11-21T07:30:00Z` **agent-flightsim** — oracle_finding — 
- # 92 `2026-11-21T07:31:00Z` **agent-flightsim** — cell_completed — 
- # 93 `2026-11-21T07:32:00Z` **agent-flightsim** — oracle_finding — 
- # 94 `2026-11-21T07:33:00Z` **agent-flightsim** — oracle_finding — 
- # 95 `2026-11-21T07:34:00Z` **agent-flightsim** — oracle_finding — 
- # 96 `2026-11-21T07:35:00Z` **agent-flightsim** — cell_completed — 
- # 97 `2026-11-21T07:36:00Z` **agent-flightsim** — oracle_finding — 
- # 98 `2026-11-21T07:37:00Z` **agent-flightsim** — oracle_finding — 
- # 99 `2026-11-21T07:38:00Z` **agent-flightsim** — cell_completed — 
- #100 `2026-11-21T07:39:00Z` **agent-flightsim** — oracle_finding — 
- #101 `2026-11-21T07:40:00Z` **agent-flightsim** — oracle_finding — 
- #102 `2026-11-21T07:41:00Z` **agent-flightsim** — oracle_finding — 
- #103 `2026-11-21T07:42:00Z` **agent-flightsim** — oracle_finding — 
- #104 `2026-11-21T07:43:00Z` **agent-flightsim** — cell_completed — 
- #105 `2026-11-21T07:44:00Z` **agent-flightsim** — oracle_finding — 
- #106 `2026-11-21T07:45:00Z` **agent-flightsim** — oracle_finding — 
- #107 `2026-11-21T07:46:00Z` **agent-flightsim** — oracle_finding — 
- #108 `2026-11-21T07:47:00Z` **agent-flightsim** — cell_completed — 
- #109 `2026-11-21T07:48:00Z` **agent-flightsim** — oracle_finding — 
- #110 `2026-11-21T07:49:00Z` **agent-flightsim** — batch_verdict — DECISION flightsim_grid_batch_verdict: 43/108 runs passed the scorer; 72 oracle findings (decider=None, computed=None)
- #111 `2026-11-21T06:00:00Z` **agent-flightsim** — batch_started — 
- #112 `2026-11-21T06:01:00Z` **agent-flightsim** — mutation_completed — 
- #113 `2026-11-21T06:02:00Z` **agent-flightsim** — oracle_finding — 
- #114 `2026-11-21T06:03:00Z` **agent-flightsim** — oracle_finding — 
- #115 `2026-11-21T06:04:00Z` **agent-flightsim** — oracle_finding — 
- #116 `2026-11-21T06:05:00Z` **agent-flightsim** — oracle_finding — 
- #117 `2026-11-21T06:06:00Z` **agent-flightsim** — oracle_finding — 
- #118 `2026-11-21T06:07:00Z` **agent-flightsim** — oracle_finding — 
- #119 `2026-11-21T06:08:00Z` **agent-flightsim** — oracle_finding — 
- #120 `2026-11-21T06:09:00Z` **agent-flightsim** — oracle_finding — 
- #121 `2026-11-21T06:10:00Z` **agent-flightsim** — oracle_finding — 
- #122 `2026-11-21T06:11:00Z` **agent-flightsim** — oracle_finding — 
- #123 `2026-11-21T06:12:00Z` **agent-flightsim** — oracle_finding — 
- #124 `2026-11-21T06:13:00Z` **agent-flightsim** — oracle_finding — 
- #125 `2026-11-21T06:14:00Z` **agent-flightsim** — oracle_finding — 
- #126 `2026-11-21T06:15:00Z` **agent-flightsim** — oracle_finding — 
- #127 `2026-11-21T06:16:00Z` **agent-flightsim** — oracle_finding — 
- #128 `2026-11-21T06:17:00Z` **agent-flightsim** — oracle_finding — 
- #129 `2026-11-21T06:18:00Z` **agent-flightsim** — mutation_completed — 
- #130 `2026-11-21T06:19:00Z` **agent-flightsim** — mutation_completed — 
- #131 `2026-11-21T06:20:00Z` **agent-flightsim** — mutation_completed — 
- #132 `2026-11-21T06:21:00Z` **agent-flightsim** — oracle_finding — 
- #133 `2026-11-21T06:22:00Z` **agent-flightsim** — oracle_finding — 
- #134 `2026-11-21T06:23:00Z` **agent-flightsim** — oracle_finding — 
- #135 `2026-11-21T06:24:00Z` **agent-flightsim** — oracle_finding — 
- #136 `2026-11-21T06:25:00Z` **agent-flightsim** — oracle_finding — 
- #137 `2026-11-21T06:26:00Z` **agent-flightsim** — oracle_finding — 
- #138 `2026-11-21T06:27:00Z` **agent-flightsim** — oracle_finding — 
- #139 `2026-11-21T06:28:00Z` **agent-flightsim** — oracle_finding — 
- #140 `2026-11-21T06:29:00Z` **agent-flightsim** — oracle_finding — 
- #141 `2026-11-21T06:30:00Z` **agent-flightsim** — oracle_finding — 
- #142 `2026-11-21T06:31:00Z` **agent-flightsim** — oracle_finding — 
- #143 `2026-11-21T06:32:00Z` **agent-flightsim** — oracle_finding — 
- #144 `2026-11-21T06:33:00Z` **agent-flightsim** — oracle_finding — 
- #145 `2026-11-21T06:34:00Z` **agent-flightsim** — oracle_finding — 
- #146 `2026-11-21T06:35:00Z` **agent-flightsim** — batch_verdict — DECISION flightsim_fuzz_batch_verdict: 4 mutations run; 5 wrong answer(s) escaped every layer (decider=None, computed=None)
