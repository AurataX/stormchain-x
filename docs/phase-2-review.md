# Phase 2 review and handoff

Implemented and reviewed: decayed source-weighted evidence, explicit uncertainty
flags, independent road passability, typed dependency graph, depot reachability,
backup-aware monotone cascades, seeded sampling, and persistent run snapshots.

53 tests passed, including PostgreSQL upgrade/fresh initialization and snapshot
replay. Review confirmed source-size limits, finite/probability bounds, scenario
isolation, receipt-time cutoffs, same-source deduplication, unknown evidence,
cyclic dependencies, alternate routes, backup exhaustion, and protected writes.

Corrections made during review:

- Direct Pydantic dependencies turned invalid query values into server errors;
  query-model validation now returns 422.
- Physical road damage was an inadequate proxy for closure; access_status now
  carries OPEN/BLOCKED/UNKNOWN independently, with an idempotent legacy migration.
- Unknown depots also make routes uncertain; no unobserved depot is assumed ready.
- Runtime versions are recorded with snapshots; old snapshots are not reinterpreted.

Limits: heuristic probabilities, independent samples, approximate horizon-average
backup service, no flow conservation, static topology/source definitions, local
shared-token authorization, and bounded workload. No production reliability claim.

Next: Phase 3 CP-SAT scheduling with access prerequisites, budgets, crew limits,
information priority and deterministic plan diffs. Phase 4 builds the Next.js
map console. Neither phase is implemented or authorized yet.

Repository destination: private `AurataX/stormchain-x`. Docker artifacts are
disposable and must be removed after testing under the user's storage policy.
