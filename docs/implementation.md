# Implementation plan and acceptance

Documentation first; backend foundation second; tests and evidence last.

Phase 1 must deliver:

- Runnable FastAPI package and Docker Compose configuration.
- Foreign-key constrained asset types, assets, dependencies, observation sources,
  observations, scenarios, and recovery-plan storage.
- Explicit idempotent bootstrap with a labeled synthetic coastal district.
- GeoJSON assets, asset details/history, dependency listing, scenario retrieval,
  validated and authorized observation ingestion, and health/readiness endpoints.
- SQLite integration tests with real storage, plus a PostgreSQL/PostGIS test
  mode and generated-schema drift check.
- Local run instructions, environment variables, limits, and verification evidence.

Recovery-plan storage is schema only. No generation endpoint exists until Phase 3.
Use async SQLAlchemy consistently. Never silently fall back between databases.
Use UTC timestamps, stable UUID report IDs, deterministic ordering, bounded
pagination, duplicate conflict responses, and rollback on invalid references.

Gate every source file at 250 whitespace-separated words. Do not reduce
readability to satisfy the gate. Documents and fixtures may be longer.

Completion requires actually running available checks. Record environmental
blocks without calling unexecuted Docker or PostgreSQL paths verified.
