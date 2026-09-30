# Local development (PowerShell)

From the repository root:

```powershell
uv venv .venv
uv pip sync --python .venv/Scripts/python.exe apps/api/requirements-dev.lock
.venv/Scripts/python.exe scripts/verify.py
```

Run the API and Phase 4 console together (stop an existing console first):

```powershell
./scripts/dev.ps1
```

Open `http://127.0.0.1:3000`. The launcher starts the API on port 8001 and
supplies the same operator token to both servers. Starting only `npm run dev`
does not start the Python API. A proxy 502 means the configured backend cannot
be reached; check `http://127.0.0.1:8001/ready` when using the launcher.
The console has no `/contact` route; use `/`.

Google Maps reads `NEXT_PUBLIC_GOOGLE_MAPS_API_KEY` from
`apps/web/.env.development.local` (ignored). This browser key must allow the
Maps JavaScript API and the local website origin. Optional
`NEXT_PUBLIC_GOOGLE_MAPS_MAP_ID` overrides the sample `DEMO_MAP_ID`.
Restart the console after changing public environment variables.
`ApiTargetBlockedMapError` means the key's API restrictions block this API.
No API enablement or cloud configuration is performed by the local launcher.

With both servers running and Chrome installed, run `npm run test:browser` from
`apps/web`. These tests mock Google Maps explicitly and use the real local API;
the workflow test writes labeled synthetic reports and new demo plan versions.

For local production-mode verification, keep the API running on 8001 and configure
ignored `apps/web/.env.production.local` with `API_URL=http://127.0.0.1:8001`,
the same server-side `OPERATOR_TOKEN`, and `NEXT_PUBLIC_GOOGLE_MAPS_API_KEY`.
The development environment files are not loaded by the production build.
Keep the key out of source files. The browser Maps key is public by design;
the operator token must remain server-side.

From `apps/web`, run:

```powershell
npm run build
node node_modules/next/dist/bin/next start -H 127.0.0.1 -p 3001
```

Open `http://127.0.0.1:3001`. Public Maps variables are embedded at build time;
rebuild after changing them. The ignored local production file configures this
single-machine check only. A future deployment must supply its own backend URL,
operator credentials and domain-restricted Maps key through its environment.
Local success does not establish remote deployment or production authorization.

For a backend-only SQLite session:

```powershell
$env:OPERATOR_TOKEN = [guid]::NewGuid().ToString('N')
Set-Location apps/api
../../.venv/Scripts/python.exe -m app.bootstrap
../../.venv/Scripts/python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Open `http://127.0.0.1:8000/docs`. Authorize writes using the token in your
local environment. Token values must not be committed or pasted into chat.
Direct Python does not automatically load `.env`; set environment variables explicitly.

For optional briefings, set server-side `GOOGLE_CLOUD_PROJECT` and
`GOOGLE_CLOUD_LOCATION` with existing Application Default Credentials. Vertex AI
takes precedence. `GEMINI_API_KEY` is the local Gemini API alternative. The
default model is `gemini-3.5-flash`; `VERTEX_MODEL` overrides it for either path.
Restart the API after changing its environment. An unset provider gives 503.
The console proxy passes its operator token to the briefing endpoint.

Docker alternative (Docker Desktop running):

```powershell
# First setup only: copy .env.example to .env and replace both values.
docker compose config --quiet
docker compose up --build -d
docker compose ps
curl.exe --fail http://127.0.0.1:8000/ready
docker compose down --volumes --rmi all --remove-orphans
```

Use URL-safe generated hex passwords for this local Compose URL. Run
the cleanup command after tests finish: it deliberately removes local demo data.
Follow [cleanup policy](docker-cleanup.md). The init service exits
successfully after initialization; the API waits for it.

All fixture observations have a fixed 2026-09-28 simulation clock; they are
historical synthetic reports, not real-time feeds. See [Phase 4 status](phase-4-status.md)
for the console's implemented behavior and remaining browser checks.
