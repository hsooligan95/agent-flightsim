"""AgentFlightSim: enumerate an agent's world, don't just test its code.

A scenario engine that builds simulated service twins, sweeps the
world-state axes an agent will actually meet in production (data
staleness, dependency health, user type, corpus redundancy), runs a
real agent over every cell, and judges the runs with oracles the
per-sentence scorers don't have: a freshness oracle and a cross-source
consistency oracle.
"""
