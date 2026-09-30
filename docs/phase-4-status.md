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

- Earlier real Google basemap checks were blocked by `ApiTargetBlockedMapError`;
  the latest supplied key passed a live browser initialization smoke check below.
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

## Repeated local API outage — 2026-09-30

- Reproduced scenario proxy GET 502; direct readiness requests on 8000 and 8001
  both refused connections. The configured API on 8001 was stopped.
- Restarted `uvicorn app.main:app --host 127.0.0.1 --port 8001` with the existing
  ignored console operator token and existing SQLite database; no bootstrap needed.
  API remains running in a hidden background process for the current console.
  PowerShell `Start-Process` failed with duplicate `Path`/`PATH` environment keys;
  Python `subprocess.Popen` with `CREATE_NO_WINDOW` successfully started it.
- Python urllib smoke through port 3000: graph, plans, scenario and observation
  sources each returned 200; empty observation POST returned 422. Direct `/ready`
  returned 200. The first smoke attempt ran before API startup and still saw 502.
- `npm run typecheck` passed. `.venv/Scripts/python.exe scripts/verify.py` initially
  gave 15 passed, 4 skipped and 40 temporary-directory permission errors; permitted
  rerun passed with 55 tests and 4 PostgreSQL skips. Size, docs, schema, Ruff lint
  and formatting passed. Existing httpx deprecation warning remains.
- Changed `.gitignore` to exclude local API logs, this handoff and `docs/tasks.md`.
  Existing changes to `next-env.d.ts` and untracked `pnpm-lock.yaml` were preserved.
  No application code change was needed. Use `scripts/dev.ps1` for future sessions
  so both services run together; starting only the console does not start the API.
- Next incomplete task remains real Google basemap/roads and full keyboard
  acceptance. No Docker testing or cloud changes were performed.

## Updated Google Maps key — 2026-09-30

- User supplied a replacement Maps JavaScript API key. Set
  `NEXT_PUBLIC_GOOGLE_MAPS_API_KEY` in ignored `apps/web/.env.development.local`,
  preserving the shared operator token. No key value is recorded here.
- Live Playwright/Chrome smoke against port 3000 (no Google mock) found one
  `.gm-style` map container and no reported Google `MapError`/`MapWarning` codes
  or nonempty application alerts after an eight-second observation window.
  This verifies initialization, not complete visual or interaction acceptance.
- Initial sandbox browser launch failed; permitted rerun passed. No application
  source changed; no cloud configuration changed. Changed this handoff and tasks;
  local key configuration remains ignored. Full road/marker interactions, visible
  attribution, keyboard navigation and real-map viewport checks remain incomplete.

## Local production build verification — 2026-09-30

- User clarified there is no deployed server and requested verification before
  deployment. No external deployment or cloud configuration was performed.
- Created ignored `.env.production.local` using the existing operator token and
  Maps key, with explicit local `API_URL` on 8001. Development env files are not
  loaded in production mode. No values were printed or committed.
- `npm run build` first compiled but failed at the TypeScript worker with
  sandbox `spawn EPERM`; permitted rerun passed. Started production Next.js via
  `node node_modules/next/dist/bin/next start -H 127.0.0.1 -p 3001`; left running.
- urllib GET smoke against port 3001: graph, plans, scenario and sources all 200.
- `npx playwright test --config test-results/production.config.cjs`: 10 passed
  against port 3001, with real API and explicitly mocked Google Maps. This covers
  evidence persistence, stale-plan recalculation/comparison, marker lifecycle,
  network/auth failure states and six viewport/theme combinations. The ignored
  temporary config overrides only baseURL/output directory and uses existing tests.
- Separate live Google Chrome check (no mock) passed 360/768/1280px in light/dark:
  visible map, seven markers, marker selection opens inspector, one selected ring,
  no horizontal overflow, Google error/warning codes or uncaught page errors.
  Confirmed the script used the key from the production environment without
  printing it. Screenshots are in ignored `apps/web/test-results`; inspected the
  1280px light screenshot and confirmed rendered basemap and visible attribution.
- `.venv/Scripts/python.exe scripts/verify.py`: 55 passed, 4 PostgreSQL skips;
  size, docs, schema, Ruff lint and formatting passed. Existing httpx warning remains.
- Changed local-development documentation, this handoff and tasks; Next regenerated
  `apps/web/next-env.d.ts` during build. Production environment and browser artifacts
  remain ignored. No application logic changed. This verifies a single local server
  with SQLite, not Cloud Run/PostgreSQL, public authentication or remote key restrictions.
- Next incomplete Phase 4 task: real road-overlay interaction and complete keyboard
  focus/navigation acceptance; measured contrast remains unverified.

## Gemini briefing extension — 2026-09-30

- `POST /api/v1/briefings` reads a saved plan, prior version, selected observations,
  assets and dependencies from one scenario. Gemini chooses up to 12 fact IDs through
  one read-only `lookup_saved_facts` call. The backend validates those IDs, requests
  a structured explanation, and validates citation IDs against the selected facts.
  The console shows the answer and expandable saved facts; it does not alter plans.
- The existing `GEMINI_API_KEY` path and `gemini-3.5-flash` default were retained.
  Configured Vertex project/location take precedence. No Vertex project/location is
  set in this process, so Vertex execution remains unverified. No GCP resource or
  configuration was changed.
- Live small synthetic Gemini API call returned `OK`. A live two-step lookup plus
  briefing initially returned 502 with a 600-token output cap. Using `low` thinking
  and 1500 output tokens returned a cited, uncertainty-aware explanation. This is
  a smoke call, not a semantic accuracy benchmark.
- A live `TestClient` POST against the disposable SQLite demo and the existing
  Gemini key returned 200 for saved plan v2 with three valid citation IDs. It
  correctly noted that the tested versions had identical actions. This checks
  the complete local endpoint/model path, not Vertex AI or browser/model delivery.
- Final `.venv/Scripts/python.exe scripts/verify.py`: 60 passed, 4 PostgreSQL
  skips; source-size, docs links, schema drift, Ruff lint and format passed.
  The first final-gate run found one 107-character line; shortening it restored
  the lint pass. Focused briefing tests: 5 passed. `npm.cmd run typecheck` and
  `npm.cmd run build` passed. Local API/console Playwright: 11 passed, including
  a 360px briefing display with a mocked model response. Local servers stopped.
- Changed files: briefing API/schema/services and tests, settings and dependency
  locks, console briefing/panel/layout/CSS and browser test, `.env.example`, API,
  local development, task and this status documentation. Existing light-map theme
  changes were already committed separately; no deployment was performed here.
- Next: verify Vertex with a project and location, then test actual model responses
  through the console. Real road-overlay interaction, complete keyboard navigation,
  and measured contrast remain incomplete Phase 4 checks.
