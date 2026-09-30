# Starts API (8001) and console (3000) with one shared operator token. Ctrl+C stops both.
# Port 8001 avoids clashing with other local services that commonly hold 8000.
$root = Split-Path $PSScriptRoot
if (Test-Path "$root/.env") {
  Get-Content "$root/.env" | Where-Object { $_ -match '^\s*[^#\s][^=]*=' } | ForEach-Object {
    $key, $value = $_ -split '=', 2
    [Environment]::SetEnvironmentVariable($key.Trim(), $value.Trim(), 'Process')
  }
}
$env:OPERATOR_TOKEN = [guid]::NewGuid().ToString('N')
$env:API_URL = "http://127.0.0.1:8001"
if (-not $env:DATABASE_URL) { $env:DATABASE_URL = "sqlite+aiosqlite:///$root/apps/api/stormchain.db" }
$py = "$root/.venv/Scripts/python.exe"
Push-Location "$root/apps/api"
& $py -m app.bootstrap
$api = Start-Process $py "-m uvicorn app.main:app --host 127.0.0.1 --port 8001" -PassThru -NoNewWindow
Pop-Location
try { Set-Location "$root/apps/web"; npm run dev } finally { Stop-Process -Id $api.Id -Force }
