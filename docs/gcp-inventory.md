# GCP read-only inventory — 2026-09-29

Scope: active project metadata and relevant hosting resources only. No cloud
configuration, IAM, resources, APIs, objects, or existing applications were modified.
No secret values, bucket contents, application databases, or logs were retrieved.

Project: `astute-lyceum-484806-g3` (NexaLabs), ACTIVE.
Active CLI identity is the user's existing Growth Charters service account.
The existing Cloud Run service `growth-charter-console` is in `us-west1`.
Keep STORMCHAIN-X deployment separate from it.

Artifact Registry has a Docker repository named `gcr.io`.
Three buckets are listed: AI Studio (US-WEST1), Cloud Build (US), and
`ecocred-apk` (US). No contents inspected.
Compute instance and Cloud Run job listings returned no rows.

Enabled APIs relevant to planning:

The [complete enabled list](gcp-enabled-apis.md) contains 63 services.

- Cloud Run, Artifact Registry, Cloud Build, Compute, IAM, IAP.
- Logging, Monitoring, Cloud Trace, Storage, Service Usage.
- Vertex AI, Generative Language, BigQuery, Pub/Sub.
- Maps, Directions, Distance Matrix, Geocoding, Places, Route Optimization.

Cloud SQL Admin (`sqladmin.googleapis.com`) and Secret Manager
(`secretmanager.googleapis.com`) were absent from the enabled list. SQL Component
is enabled but is not equivalent to Cloud SQL Admin readiness.

CLI reported a missing environment tag. It was left unchanged.
This inventory does not establish billing, quotas, permissions, or deployability.
Recheck these explicitly before an authorized deployment.
