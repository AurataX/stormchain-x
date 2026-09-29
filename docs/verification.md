# Verification evidence — 2026-09-29

## Current: Phase 2

- Full gate: **53 tests passed**, including all four PostgreSQL tests, with
  both an upgraded Phase 1 database and a fresh Phase 2 database.
- Source-size, Ruff, schema drift, and documentation-link checks passed.
- Live Docker POST cascade → GET saved run succeeded; graph returned 10 assets
  and 16 edges. A single local 200-sample request took 165ms. This is one
  measured smoke request, not a general latency guarantee.
- Engine: cascade-0.2.0; Docker Python 3.12.14, NetworkX 3.7. Windows tests
  used Python 3.12.10. Each persisted run records its runtime versions.
- Latest runtime dependency audit: no known vulnerabilities found.
- Review fixed invalid graph-query handling (422 instead of server error),
  distinguished road passability from physical condition, and tested the
  non-destructive access_status migration.
- No frontend or optimizer exists yet. Read [Phase 2 semantics](phase-2-engine.md)
  for model limitations. Phase 3 requires confirmation.

## Historical: Phase 1

Executed on Windows with Python 3.12.10; Docker Desktop runs Linux containers.

| Check | Actual result |
|---|---|
| `python scripts/verify.py` with TEST_DATABASE_URL | 27 tests passed; no skipped PostgreSQL tests |
| Source-size gate | All authored source files ≤250 whitespace-separated words |
| Ruff lint and format | Passed |
| Schema drift | Generated PostgreSQL DDL matches models |
| PostgreSQL integration | Geometry, GiST index, ingestion, restart and raw DDL passed |
| `docker compose config --quiet` | Passed |
| `docker compose up --build -d` | API/database built and started; init exited successfully |
| HTTP `/ready` | 200; database = postgresql |
| Container health | API and database healthy |
| PostgreSQL spatial extension | PostGIS 3.4 loaded |
| Runtime dependency audit | `uvx pip-audit -r apps/api/requirements.lock --no-deps --disable-pip`: no known vulnerabilities found |
| Live HTTP GeoJSON / OpenAPI | 10 synthetic assets returned; API specification served |

Review reproduced and fixed two bugs: non-ASCII bearer credentials caused
a comparison error; NaN confidence caused validation-error serialization to
fail. Regression tests now assert 401 and 422 respectively. Boolean confidence
is also rejected. Invalid inputs never become evidence.

Phase 1 limits at its original handoff:

- One upstream test-client deprecation warning advises migrating from httpx
  to httpx2. Tests pass; the runtime API does not depend on httpx.
- No UI, fusion, cascades, scheduling, or cloud deployment implemented.
- Bootstrap initializes schemas but does not perform versioned upgrades.
- Local shared-token authorization is not production identity management.
- No independent human or external-agent review has been performed.

GCP inspection was metadata-only. All 63 enabled APIs are recorded separately.
