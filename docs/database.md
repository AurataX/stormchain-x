# Database contract

| Table | Purpose |
|---|---|
| asset_types | Infrastructure categories and explicit criticality weights |
| assets | Stable identifiers, GeoJSON, capacities, backup attributes, provenance |
| dependencies | Directed typed edges with foreign keys and no self edges |
| observation_sources | Reliability and half-life metadata, not yet fused |
| observations | Scenario-scoped immutable evidence, confidence and two UTC clocks |
| scenarios | Communication mode, category, integer budget and crew inventory |
| recovery_plans | Future plan persistence schema; no seeded or generated plans |
| simulation_runs | Phase 2 complete inputs/results, fingerprint, engine version and timestamp |

Money uses integer cents with currency; duration uses integer minutes.
Observation IDs are caller-supplied UUIDs. Duplicate IDs return 409, avoiding
silent duplicate evidence on retries. Unknown references return 404.

`app/models` is the source of truth. Run `python scripts/schema.py --write`
after reviewed model changes. `apps/api/database/schema.sql` contains the
generated PostgreSQL DDL plus PostGIS extension/geometry/index setup.

PostgreSQL derives EPSG:4326 `geom` from GeoJSON in a stored generated column;
the GiST index supports future spatial queries. SQLite stores GeoJSON only.

Bootstrap is explicit and idempotent for missing rows, preserving existing
records. Run one bootstrap process at a time. It initializes fresh schemas;
`create_all` does not migrate existing table definitions. Phase 2 includes one
explicit, idempotent access_status column migration preserving old reports as
NULL/unknown. A general versioned migration framework remains deferred.

Future action catalogs, communication events, and evaluation
results receive tables in their own phases. Do not create unused tables now.
