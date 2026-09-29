# Phase 4 status

Console in `apps/web` (Next.js 16.3.7, React 19.3.0, MapLibre GL 6.11.2, Lucide).
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

- Map: local synthetic geometry only, no external basemap; colors from tokens, planned
  repairs ringed, selection ring, asset table as the keyboard alternative.
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

- No browser test: the Chrome extension was not connected. Rendering, map clicks, focus
  order, UI forms, 360/768/1280px layouts, contrast and reduced motion are unchecked.
  No screenshots exist; make no visual-quality claim.
- No automated frontend tests or lint. shadcn/ui and Radix were not adopted (native
  elements suffice); recorded per [libraries](design/libraries.md).
- PostgreSQL still unverified (Docker offline).
