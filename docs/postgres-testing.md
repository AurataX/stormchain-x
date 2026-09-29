# PostgreSQL integration tests

Use only a dedicated local database ending in `_test`. Tests insert synthetic
reports; they never clear or drop an application database. The SQL schema test
uses a unique temporary schema and rolls its transaction back.

With Docker Compose running, from the repository root:

```powershell
# Once per local database volume:
docker compose exec -T db createdb -U stormchain stormchain_test

# Load only local credentials; do not print them.
$localSettings = Get-Content .env | ConvertFrom-StringData
$env:TEST_DATABASE_URL = 'postgresql+asyncpg://stormchain:' + `
    $localSettings.POSTGRES_PASSWORD + '@127.0.0.1:5432/stormchain_test'
.venv/Scripts/python.exe scripts/verify.py
Remove-Item Env:TEST_DATABASE_URL
```

If the database already exists, skip `createdb`. Without `TEST_DATABASE_URL`,
the four PostgreSQL tests explicitly skip while the SQLite tests still run.

PostgreSQL tests cover EPSG:4326 geometry, point/line types, validity, GiST
index presence, idempotent seeding, persistent API ingestion, application
restart, and execution of the generated schema in an isolated namespace.

Simulation snapshots also persist and replay across PostgreSQL app restarts.
All database integration tests use real connections. SQLite checks additionally cover
validation, foreign keys, scenario filtering, duplicate report IDs, and auth.
