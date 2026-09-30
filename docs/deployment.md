# Deployment

The demo runs on Google Cloud Run (`asia-south1`), built from source with Cloud Build.

| Service | Notes |
|---|---|
| `stormchain-api` | FastAPI, 512 MiB, one always-on instance, SQLite under `/tmp` reseeded on start |
| `stormchain-web` | Next.js console, scales to zero, proxies `/api/v1/*` to the API |

Runtime settings: the API takes `DATABASE_URL`, `OPERATOR_TOKEN`, `GEMINI_API_KEY`
and `VERTEX_MODEL`; the console takes `API_URL` and `OPERATOR_TOKEN`. The Maps key
is bundled at build time from `NEXT_PUBLIC_GOOGLE_MAPS_API_KEY`, so restrict it by
HTTP referrer to the console URL.

```powershell
gcloud run deploy stormchain-api --source apps/api --region asia-south1
gcloud run deploy stormchain-web --source <console build folder> --region asia-south1
```

Public access needs `allUsers` with `roles/run.invoker` on both services. Organizations
that enforce domain-restricted sharing must allow it for the project first.

## Before real use

The hosted demo keeps data in SQLite and resets on restart. A production launch needs
Cloud SQL with PostGIS, reviewed migrations, identity-based access instead of the shared
token, request limits, audit retention, and a security review.

## Rollback and cleanup

Route traffic to the previous Cloud Run revision to roll back. To remove the demo,
delete both services and their Artifact Registry images.
