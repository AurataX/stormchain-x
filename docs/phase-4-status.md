# Phase 4 status

Console in `apps/web` (Next.js 16.3.7, React 19.3.0, Google Maps JavaScript API, Lucide).
Structure follows [structure](structure.md): `src/app` (+ `_components`),
`features/{assets,observations,recovery}`, `lib`. Every control calls a real endpoint.

Run both servers with one shared token (API on 8001, console on 3000):

```powershell
./scripts/dev.ps1
```

Port 8001 avoids clashes with other local services on 8000 (a 502 from the console
means the API is unreachable at `API_URL`, default `http://127.0.0.1:8000`).

The web server proxies `/api/v1/*` to `API_URL` (default `http://127.0.0.1:8000`) and
adds the operator token to POSTs server-side, so the token never reaches the browser.
Anyone who can open the console can write: local demo only, not production auth.

## Behavior

- Map: Google Maps advanced markers, synthetic roads, dashed point-to-point dependencies,
  token-based status colors, planned and selected rings. Fits the coastal fixture bounds;
  follows system theme. Legend sits below the map, clear of Google's attribution.
  Google service/key failures show an error; the asset table remains usable.
- Layout: compact divided KPI strip, fixed scenario constraints, map beside recovery plan,
  scrollable asset/evidence panels and a situation summary when no asset is selected.
  Overview/Plan/Evidence tabs below 1100px; light/dark checked at 360/768/1280px.
- Inspector, evidence form (refreshes graph, marks plan stale), Generate / Recalculate,
  solver status (non-OPTIMAL labelled), verification list (heuristic label), version
  comparison, assumptions, loading/empty/error/disconnected states.
- "Evidence as of" sets graph and plan `as_of`; default is now, so the 2026-09-28
  fixture evidence has decayed. Stale is a session flag, not recomputed on reload.

## Evidence (Windows, Node 26.5.1)

- `npx tsc --noEmit` clean; `npx next build` succeeded.
- Through the running web server: observation POST 201, plan POST v1 OPTIMAL gap 0.0
  (road-main and road-coastal selected with dependent repairs), graph GET, future
  `as_of` gives 422, `..` path gives 404.

## NOT verified

- Real Google basemap rendering is blocked by the supplied key's `ApiTargetBlockedMapError`.
  Advanced marker integration is tested with an explicitly labeled mock, not a live map.
  Full keyboard focus order, real road clicks, Google attribution visibility, and measured
  contrast remain unverified. Reduced-motion preference was enabled in layout tests.
- No frontend lint configuration. shadcn/ui and Radix were not adopted (native
  elements suffice); recorded per [libraries](design/libraries.md).
- PostgreSQL still unverified (Docker offline).

## Local proxy recovery — 2026-09-30

- Reproduced console GET 502 with connection refusal at both 8000 and 8001.
  Tracked `.env.development` selects 8001; neither backend was running.
- Ran `app.bootstrap` against the existing SQLite demo database, then
  `uvicorn app.main:app --host 127.0.0.1 --port 8001` using the project Python.
  The API was left running for the existing console session.
- Generated a shared operator token in ignored `apps/web/.env.development.local`
  and the API environment. No token was printed or committed.
- Python urllib smoke through port 3000: graph, plans, scenario, and observation
  sources each returned 200; empty observation POST returned 422 after authorization.
- `npm run typecheck` passed. `.venv/Scripts/python.exe scripts/verify.py`
  initially failed with 40 fixture errors from Windows temporary-directory permissions
  (15 passed, 4 skipped); rerun with permissions passed: 55 passed, 4 skipped.
  Source-size, documentation links, schema drift, Ruff lint and formatting passed.
  PostgreSQL tests were skipped because no isolated database was configured.
- Changed `.gitignore`, `docs/local-development.md`, this handoff and `docs/tasks.md`.
  Local setup file and SQLite database are untracked runtime artifacts.
- `/contact` is absent from the console and its links; 404 is expected.
  Next incomplete Phase 4 task remains browser workflow, keyboard, and viewport testing.

## Google Maps and density refresh — 2026-09-30

- User authorized replacing MapLibre with the supplied Google Maps integration and
  reducing empty space. See [design direction](design/console-refresh.md).
- Google key stored in ignored `.env.development.local`; operator token retained.
  MapLibre dependency, style/layer/highlight helpers and worker-copy script removed.
  Added a shared script loader, typed advanced markers, road/dependency overlays,
  compact CSS, situation summary, and Playwright tests/configuration.
- `npm run typecheck` and `npm run build` passed. Build initially hit sandbox
  `spawn EPERM`; permitted rerun passed. Initial typecheck held stale incremental
  diagnostics after adding global Google types; removing generated `tsconfig.tsbuildinfo`
  and rerunning passed without weakening checks.
- `npm run test:browser`: **10 passed** using installed headless Chrome, real local API,
  and labeled Google mock. Six light/dark viewport tests, marker cleanup/selection,
  network/auth errors, and persisted evidence → stale plan → recalculation/comparison.
  First two test runs had selector failures (8 and 6); corrected selectors to target
  map content, the scoped alert and accessible combobox. Final layout rerun passed.
- Browser workflow wrote labeled synthetic blocked-road reports and new plan versions
  into the disposable demo database. Screenshots are ignored under `apps/web/test-results`.
- `.venv/Scripts/python.exe scripts/verify.py`: **55 passed, 4 PostgreSQL skips**;
  source-size, links, Ruff lint/format and schema drift passed. npm audit: 0 vulnerabilities.
- Real Google request returned `ApiTargetBlockedMapError`; no GCP API/configuration,
  billing, IAM, or deployment changes were made. Next task: correct key API restrictions
  outside this read-only authorization, then verify real basemap/roads and keyboard flow.
- Changed files: web package/lock and TypeScript config, new Playwright config/tests,
  asset map/loader/marker/line/summary modules, compact/map/data CSS, layout imports,
  constraints/evidence/console/legend components, and design/status/task/local-dev docs.
