# Deployment runbook (planned)

Phase 1 supplies local containers; no cloud resources have been deployed.

Release sequence for Phase 5:

1. Pass API, PostgreSQL/PostGIS, browser, source-size, and dependency checks.
2. Choose GCP project/region and approve estimated spend.
3. Create Artifact Registry, Cloud SQL, service accounts, and secrets.
4. Build immutable images; record digests and dependency versions.
5. Back up the database; run reviewed schema migrations as a separate job.
6. Deploy API with connection limits and authenticated write access.
7. Deploy console with private backend credentials kept server-side.
8. Run remote health, ingestion, persistence, and full demonstration checks.
9. Record URLs, revision IDs, evidence, and rollback instructions.

Rollback selects the previous Cloud Run revision. Database rollback requires
a reviewed compatible migration or backup restore; never delete data casually.

Do not expose the Phase 1 shared-token prototype as production authorization.
Before a public launch add identity-based access, request-size/rate limits,
audit retention policy, and security review.
