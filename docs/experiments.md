# Evaluation contract (Phase 5)

Run every strategy on identical scenario snapshots, budgets, crew inventories,
access constraints, and random seeds. Criticality-first, damage-first,
proximity-first, and random-feasible baselines must obey the same feasibility rules.

Experiment dimensions:

- Missing evidence: 0%, 20%, 50%, 80%.
- Receipt delay: 30 minutes and four hours; retain actual observation time.
- Conflicting sources, stale reports, and communication blackout/restoration.
- Tight versus normal budgets and specialized crew shortages.
- Road disruption after initial planning; alternative route availability.
- Verification enabled versus disabled on the same uncertain assets.

Measure population-weighted service-hours lost, unique services restored,
integer cost, time to critical service, infeasible actions, and verification
decision changes. Report uncertainty intervals across seeded runs, not only
the most favorable trial.

Record scenario/fixture hash, seed, sample count, hardware, dependency versions,
solver deadline/status, runtime distribution, and rejected constraints.
Separate solver runtime from end-to-end request latency.

Do not call synthetic results real-world validation. Any savings shown during
the presentation must be computed from persisted plans with traceable units.
