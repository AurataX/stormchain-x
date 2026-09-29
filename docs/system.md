# System contract

Audience: hackathon judges and operators exploring a clearly labeled synthetic
coastal district. This is a decision-support prototype, not an emergency dispatch system.

Complete journey, delivered incrementally:
scenario → asset map → evidence → uncertainty → cascades → feasible recovery
schedule → new observation → revised plan → traceable comparison.

Phase 1 delivers persistence, synthetic fixtures, infrastructure relationships,
observation ingestion, scenario retrieval, database health, and tests.
Phase 2 adds evidence fusion, typed graph/access assessment, seeded cascades,
and persisted run snapshots. Recovery recommendations remain Phase 3 work.

All entities use stable identifiers. Observations retain source, observation
time, receipt time, and confidence. Missing evidence remains unknown.
Simulation and optimization will reference immutable scenario/evidence snapshots.
Do not join different scenario histories accidentally.

Local mode uses explicit SQLite configuration. Docker mode uses PostgreSQL/PostGIS.
A PostgreSQL failure must never silently switch to SQLite.

No fake status indicators, hardcoded savings, live-feed claims, or guaranteed
subsecond results. Measure results before presenting them.

Future UI must show loading, empty, error, stale, and disconnected states,
with useful recovery actions. Every displayed control must affect a real API
or clearly identify an unavailable feature.
