# GCP API usage plan

Use services because they support the demo, not because they are enabled.

| API | Role | Phase |
|---|---|---|
| run.googleapis.com | Container hosting | 5 |
| artifactregistry.googleapis.com | Immutable container artifacts | 5 |
| sqladmin.googleapis.com | Managed PostgreSQL/PostGIS | 5; currently not enabled |
| secretmanager.googleapis.com | Database/operator secrets | 5; currently not enabled |
| cloudbuild.googleapis.com | Optional managed image builds | 5 |
| logging.googleapis.com | Runtime error diagnosis | 5 |
| monitoring.googleapis.com | Readiness and latency metrics | 5 |
| storage.googleapis.com | Optional data/export objects | Only when needed |
| aiplatform.googleapis.com | Optional wording of grounded briefings | After deterministic demo |

OR-Tools is a local Python library: no Vertex AI, Maps, or Route Optimization
API is required for CP-SAT. MapLibre does not require a Google Maps API key.
BigQuery, Pub/Sub, and Compute VMs are unnecessary for the current monolith.

Official references:

- [Cloud Run deployment](https://docs.cloud.google.com/run/docs/deploying)
- [Cloud SQL connection from Cloud Run](https://docs.cloud.google.com/sql/docs/postgres/connect-run)
- [PostGIS extension support](https://docs.cloud.google.com/sql/docs/postgres/extensions)

Before cloud work, verify current permissions, quotas, pricing, regions, and
least-privilege identities. Do not enable APIs or provision resources under
the present read-only authorization.
