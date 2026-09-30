# Redeploy the Cloud Run services from the current working tree.
# Usage: ./scripts/deploy.ps1 [-Target api|web|all]
# Needs gcloud logged in. Runtime settings (tokens, API_URL, Gemini key) persist between deploys.
param([ValidateSet("api", "web", "all")] [string] $Target = "all")
# gcloud writes progress to stderr, so check exit codes rather than stopping on stderr.
function Run { & gcloud @args; if ($LASTEXITCODE -ne 0) { throw "gcloud failed ($LASTEXITCODE)" } }
$root = Split-Path $PSScriptRoot
$common = @("--region", "asia-south1", "--project", "astute-lyceum-484806-g3", "--quiet")

if ($Target -ne "web") {
  Run run deploy stormchain-api --source "$root/apps/api" @common
}
if ($Target -ne "api") {
  # .env.local is git-ignored and holds the Maps key; Next.js reads it at build time as .env.production.
  $key = Join-Path $root "apps/web/.env.local"
  if (-not (Test-Path $key)) { throw "apps/web/.env.local with NEXT_PUBLIC_GOOGLE_MAPS_API_KEY is required" }
  $tmp = Join-Path $env:TEMP "stormchain-web-build"
  Remove-Item $tmp -Recurse -Force -ErrorAction SilentlyContinue
  robocopy "$root/apps/web" $tmp /E /XD node_modules .next test-results /XF .env.local | Out-Null
  Copy-Item $key "$tmp/.env.production"
  Run run deploy stormchain-web --source $tmp @common
}
Run run services list --region asia-south1 --project astute-lyceum-484806-g3 --format "table(metadata.name,status.url)"
