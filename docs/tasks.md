# Phase ledger

## Phase 1 — documentation and backend foundation (authorized)

- [x] Inspect original requirements and Atelier/Ponytail guidance.
- [x] Record architecture corrections, design, structure, and hosting plan.
- [x] Implement package, schema, models, and Compose.
- [x] Add synthetic seed and initial endpoints.
- [x] Run database/API tests, schema checks, and source-size gate.
- [x] Record exact evidence and local commands.
- [x] Review hostile inputs; fix reproduced failures and retain regression tests.
- [x] Inspect relevant public repositories and GCP metadata read-only.

Evidence: [verification](verification.md), [review](review-results.md),
[handoff](phase-1-handoff.md). Phase 1 is complete; Phase 2 is now authorized.

## Phase 2 — evidence, graph, and cascade (authorized)

- [x] Snapshot evidence by scenario; implement confidence decay and conflict flags.
- [x] Build typed dependency graph, backup rules, and depot reachability.
- [x] Implement seeded Monte Carlo and bounded cascade convergence.
- [x] Test missing/stale/conflicting observations and cyclic dependencies.
- [ ] Persist reproducible runs; review and publish to the authorized AurataX repository.
- [ ] Remove project Docker containers/images/volumes after verification.

## Phase 3 — feasible adaptive recovery (authorized, implemented)

- [x] Integer CP-SAT scheduling, access prerequisites, crews, and budgets.
- [x] Sensitivity-based verification priority; no unsupported formal VoI claim.
- [x] Persist plan snapshots, solver status, and deterministic diffs.

Evidence: [Phase 3 review](phase-3-review.md). PostgreSQL path for plans is unverified
(Docker daemon was offline); Phase 3 is authorized, Phase 4 is next.

## Phase 4 — connected operations console

- [x] Map, inspector, constraints, evidence form, comparison (no timeline: no timeline API).
- [x] Apply design tokens, icons, motion, keyboard and responsive behavior (code only).
- [ ] Browser-test every workflow against the API; no dummy controls.

Evidence: [Phase 4 status](phase-4-status.md). Implemented and API-verified through
the proxy; visual, keyboard and 360/768/1280px checks are NOT yet done.

## Phase 5 — evaluation, release, and demonstration

- [ ] Fair feasible baselines and reproducible experiment matrix.
- [ ] Integration, accessibility, performance, deployment and restore checks.
- [ ] Rehearse V1 → road report → V2 → rationale with measured outcomes.
