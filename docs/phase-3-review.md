# Phase 3 review and handoff

Implemented: static SYNTHETIC repair catalog (`services/actions.py`), candidate
selection and access prerequisites (`planning.py`), CP-SAT model (`scheduler.py`,
`gating.py`), plan builder and version/diff persistence (`plan_builder.py`,
`recovery.py`), and `/api/v1/recovery/plans` endpoints. No new table: plans use
the existing `recovery_plans` table, with the input snapshot stored in the rationale.

## Model

- Candidates: non-road assets whose most likely fused physical state is not
  OPERATIONAL (never when evidence is UNKNOWN); roads whose own passability is
  most likely BLOCKED.
- Variables per candidate: selected, start, end. `end` is 0 when unselected and
  start + duration when selected, so only selected actions pay completion time.
- Constraints: total cost <= scenario budget; per-crew `AddCumulative` over optional
  intervals with capacity `available_crews[crew]` (missing crew type = 0);
  access gating: a selected action needs an already-open 1-hop ROAD_ACCESS
  predecessor, or a selected predecessor that finishes by its start.
- Objective: maximize criticality weight (x100, integer) x selected, dominating
  the sum of completion times. Single worker, fixed seed, 10 s limit.
- Solver status is reported verbatim with objective, best bound and relative gap.
- Verification priority = criticality x entropy for uncertain, unselected assets.
  It is a heuristic, not formal VoI.

## Deliberate deviations and limits

- UNKNOWN-access roads are **not** repair candidates. `access_assessment` marks nearly
  every node UNKNOWN when the depot has no evidence (as in the fixture), which
  would spend budget on roads no one reported blocked. They appear in
  verification priority instead. Change only with owner approval.
- Non-candidate roads count as open, including roads with no evidence.
- Benefit is each action's own criticality weight; it does not credit downstream
  services a repair enables (a zero-weight road would never be chosen).
- Catalog costs/durations are illustrative. Whole-hour granularity.
- 10 s limit: `FEASIBLE` (gap > 0) is possible on larger inputs and is reported as such.

## Evidence (Windows, Python 3.12.10, ortools 9.15.6755)

- Baseline before changes: `scripts/verify.py` = 49 passed, 4 skipped.
- After: size gate, docs check, schema check, ruff check/format all pass;
  pytest **55 passed, 4 skipped** (6 new + scheduler unit tests, scheduler tests
  checked by mutation: removing the gating or budget constraint fails them).
- Fixture plan at 2026-09-28T13:00Z: hospital-central, road-coastal,
  substation-east selected, status OPTIMAL, gap 0.0; budget 10,000,000 cents drops
  the substation.
- **Unverified:** the 4 PostgreSQL tests are skipped (Docker daemon offline) and
  no PostgreSQL run of the recovery endpoints exists. Docker cleanup was not needed
  (no containers were built). The local venv needed the blocked SQLAlchemy `.pyd`
  files deleted (Windows Application Control); pure-Python fallback is used.

Next: Phase 4 console against these endpoints. Phase 5 covers baselines and benchmarks.
