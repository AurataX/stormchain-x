# API contract

Interactive contract: `/docs`; OpenAPI JSON: `/openapi.json`.

| Method | Path | Behavior |
|---|---|---|
| GET | /health | Process liveness |
| GET | /ready | Database/schema readiness; 503 on failure |
| GET | /api/v1/assets | Paginated GeoJSON with synthetic provenance |
| GET | /api/v1/assets/{id}?scenario_id=cyclone-demo | Asset, latest 100 observations, connected edges |
| GET | /api/v1/dependencies | Directed typed edges |
| GET | /api/v1/observation-sources | Reliability/half-life metadata |
| GET | /api/v1/observations?scenario_id=cyclone-demo | Evidence; optional asset_id |
| POST | /api/v1/observations | Validated persistent report; operator bearer token required |
| GET | /api/v1/scenarios | Configurations |
| GET | /api/v1/scenarios/{id} | One configuration |

Paginated lists support `limit` (1–500; default 100) and `offset` (≥0).
Observation history orders by event time descending, then ID.

POST fields: UUID `id`, `scenario_id`, `asset_id`, `source_id`, `observed_state`,
`raw_confidence` (0–1), timezone-aware past `recorded_at`, optional `notes` (≤1000).
Receipt time is server-owned. Unsupported fields/states return 422; invalid
credentials 401; missing references 404; duplicate ID 409; unconfigured writes 503.
Road reports additionally accept optional access_status: OPEN, BLOCKED, or UNKNOWN.
Non-road access reports return 422. Physical damage and passability are separate.

Raw inventory assets expose `assessment_status: NOT_COMPUTED`. Use the graph
endpoint for scenario/time-specific fused assessments. Scenario creation is
not implemented; recovery endpoints are listed below.
Recovery and briefings:

| Method | Path | Behavior |
|---|---|---|
| POST | /api/v1/recovery/plans | Operator token; body scenario_id + optional past as_of; 201 new version |
| GET | /api/v1/recovery/plans?scenario_id= | Versions newest first; `limit` 1–100 (default 20); 404 unknown scenario |
| GET | /api/v1/recovery/plans/{uuid} | One saved plan; never recomputed |
| POST | /api/v1/briefings | Operator token; saved plan ID, question, optional asset ID; Gemini read-only fact lookup and cited briefing |

`plan_payload` holds `actions` (start/end hour, crew, cost), `solver` (status
OPTIMAL/FEASIBLE/INFEASIBLE, objective, best_bound, gap), `unselected`,
`verification_priority` and `assumptions`. `deterministic_rationale` holds the
diff against the previous version, its fingerprint and the saved input snapshot.
See the [recovery review](phase-3-review.md) for semantics.

Briefings are generated on demand; they never change a plan or observation. The
backend caps model-selected fact IDs at 12, validates them against the saved
snapshot, and rejects unknown final citation IDs. Model prose is still an
inference, not a verified causal or scientific result. Missing model configuration
returns 503; malformed model output or unknown IDs return 502.

Read access is local demo access, not production tenant authorization.

Graph and simulation:

| Method | Path | Behavior |
|---|---|---|
| GET | /api/v1/infrastructure/graph?scenario_id=cyclone-demo | Typed edges, assessments, conservative access; optional as_of |
| POST | /api/v1/simulation/cascade | Authorized snapshot, seeded simulation, persisted result |
| GET | /api/v1/simulation/runs/{uuid} | Original saved inputs/result; no silent recalculation |

POST accepts scenario_id, past timezone-aware as_of (defaults to current UTC),
seed (0–2147483647), samples (1–1000, default 200), and horizon_hours (0–168,
exclusive lower bound; default 12). Unknown fields return 422.
Graph supports scenario_id and as_of only. Missing scenarios/runs return 404.
See [engine semantics](phase-2-engine.md) before interpreting probabilities or loss.
