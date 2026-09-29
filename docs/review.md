# Change review checklist

Review the final implementation, not the intended plan.

- Scope: only authorized features; pending phases remain explicitly pending.
- Correctness: real persistence, valid references, no invented service metrics.
- Security: protected writes, bounded inputs, parameterized queries, no secret leakage.
- Isolation: observations always belong to a scenario; no accidental cross-scenario history.
- Data: synthetic provenance, UTC timestamps, stable ordering, duplicate behavior.
- Database: foreign keys and checks enforced; schema generation matches models.
- Failure behavior: dependency outages produce useful errors; never silent database fallback.
- Simplicity: no unused libraries, empty future services, or one-use abstraction layers.
- Maintainability: source gate passes; names and formatting remain readable.
- UI (Phase 4): keyboard use, responsive layout, semantic colors, real API connections.
- Evidence: exact test counts, commands, and unverified paths recorded.

Run `python scripts/verify.py` from the repository using the project environment.
PostgreSQL integration requires an isolated test database and `TEST_DATABASE_URL`.
Never point destructive integration fixtures at an existing application database.

This checklist and executable gates reduce differences between models. They do
not guarantee identical code or substitute for a human review.
