# Local development (PowerShell)

From `E:\Hackathon_Project`:

```powershell
uv venv .venv
uv pip sync --python .venv/Scripts/python.exe apps/api/requirements-dev.lock
.venv/Scripts/python.exe scripts/verify.py
```

Run SQLite development:

```powershell
$env:OPERATOR_TOKEN = [guid]::NewGuid().ToString('N')
Set-Location apps/api
../../.venv/Scripts/python.exe -m app.bootstrap
../../.venv/Scripts/python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Open `http://127.0.0.1:8000/docs`. Authorize writes using the token in your
local environment. Token values must not be committed or pasted into chat.
Direct Python does not automatically load `.env`; set environment variables explicitly.

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
historical synthetic reports, not real-time feeds. No frontend exists yet.
