# Corrections to Gemini's proposal

The modular monolith and transparent recovery reasoning are sound. These
changes are necessary before implementing the algorithms:

- UNKNOWN is an epistemic label, not a physical failure state. Maintain a
  distribution over four physical states plus separate freshness/conflict flags.
- Decayed weighted Dirichlet counts are a documented evidence heuristic unless
  supported by a source likelihood model. Include raw confidence, reliability,
  half-life, and correlated-report deduplication; avoid claiming calibration.
- Road blockage is a separate access property. Floodwater recession cannot be
  modeled as debris clearance. Use canonical ROAD_ACCESS edges consistently.
- Reachability requires an actual depot-to-target route. An unselected road
  repair cannot make a blocked route feasible. Gate selected actions on
  selected prerequisites or an already-open alternative route.
- CP-SAT uses integer time/cost units and optional intervals. Penalize completion
  times only for selected actions. Record FEASIBLE versus OPTIMAL and the gap.
- Sum service benefits at service nodes, avoiding overlap between upstream repairs.
- Independent Monte Carlo draws omit common hazard correlations. State that
  assumption; use seeded samples and bounded fixed-point cascade propagation.
- Verification value starts as sensitivity-based information priority. Formal
  expected VoI requires conditional re-solves and observation outcomes.
- Never promise the scripted $40,000 savings or subsecond solver time. Benchmark.
- Compare baselines under the same access, budget, and crew constraints.
