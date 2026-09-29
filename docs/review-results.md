# Phase 1 review results (historical)

Read [verification](verification.md) for current Phase 2 evidence.

Scope reviewed: models, database lifecycle, seeding, API contracts, security,
Compose, tests, documentation consistency, and source-size enforcement.
This was an implementation self-review with executable checks.

Resolved findings:

1. Formatting and long SQL string literals failed lint: formatted and split
   strings without altering behavior.
2. Non-ASCII bearer input raised TypeError: compare encoded bytes; assert 401.
3. NaN was rejected by validation but broke its error response: omit raw input
   from error serialization; assert 422.
4. Boolean confidence could coerce to numeric confidence: strict numeric validation.
5. Transitive dependencies were initially unpinned: added runtime/development
   lockfiles and rebuilt Docker using the runtime lock.

Architecture review: keep the FastAPI monolith, canonical typed edges, explicit
database selection, scenario-scoped evidence, integer money, and labeled synthetic
fixtures. No fake recovery or fusion endpoint was introduced.

PostgreSQL tests exercise the real engine, generated geometry, GiST index,
API persistence, and generated DDL. Missing telemetry stays missing evidence.

Deferred deliberately: production identity, rate limiting, migration framework,
performance benchmarking, browser checks, and cloud deployment. These belong
to later authorized phases and must not be marked complete.
