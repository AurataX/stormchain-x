# Phase 1 handoff (historical)

Phase 2 has since been authorized; read [tasks](tasks.md) for current status.

Completed: planning documentation, agent contracts, backend repository structure,
Docker setup, relational/PostGIS schema, seven domain table groups, synthetic
fixtures, initial routes, and automated checks. See [evidence](verification.md).

Architecture: thin FastAPI routes call focused services using async SQLAlchemy
sessions. PostgreSQL/PostGIS is the Docker path; SQLite is explicit local
development. Source models generate reviewable SQL. Bootstrap is a separate
idempotent initialization operation.

Dataset: ten fictional assets, sixteen directed dependencies, two observation
sources, one scenario, and six initial observations. Conflicting reports remain
separate, and assets without reports remain unassessed.

Run: `docker compose up --build -d`; open `http://127.0.0.1:8000/docs`.
Tests: `.venv/Scripts/python.exe scripts/verify.py`; see
[PostgreSQL setup](postgres-testing.md) to include all integration checks.

Files: see [manifest](file-manifest.md) and [structure](structure.md).
Limitations: no operations UI or decision engine yet; no GCP deployment;
shared-token local demo access; no versioned schema migrations.

Exact next phase: evidence snapshots and decay/conflict handling, typed dependency
graph, depot reachability/backup rules, and seeded Monte Carlo cascade with
bounded convergence and reproducibility tests.

This handoff originally stopped before Phase 2. The user's later approval
supersedes that boundary; Phase 3 still requires confirmation.
