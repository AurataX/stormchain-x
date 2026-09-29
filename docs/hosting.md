# Hosting decision

Local demonstration: Docker Compose with API and PostgreSQL/PostGIS. A
SQLite mode supports quick development when Docker is unavailable.

Target hosting: Cloud Run for API and future web console; Cloud SQL for
PostgreSQL/PostGIS; Artifact Registry for images; Secret Manager for secrets.
Cloud Logging captures structured runtime failures. Add Cloud Storage only
when an actual export/data object needs storage.

Cloud SQL supports PostGIS: [official extension documentation](https://docs.cloud.google.com/sql/docs/postgres/extensions).

No public deployment or paid resource provisioning in Phase 1.
Costs depend on region, instance sizing, uptime, and traffic; no invented quote.
Before provisioning, record a current pricing estimate and get authorization.

Bound Cloud Run instance counts and database pool sizes together. Configure
private or connector-mediated database access, least-privilege service accounts,
managed secrets, and HTTPS. SQLite is unsuitable for multi-instance Cloud Run.

For the hackathon, keep a rehearsed local route available if venue networking
fails. Cloud deployment is complete only after remote API and browser smoke tests.
