# Public repository review — 2026-09-29

GitHub API metadata and official repository documentation were inspected.
Popularity is a discovery signal, not evidence of correctness or suitability.

| Repository | Stars observed | License | Decision |
|---|---:|---|---|
| [FastAPI template](https://github.com/fastapi/full-stack-fastapi-template) | 45,809 | MIT | Reference deployment/test organization; do not import its Vite/SQLModel stack |
| [OR-Tools](https://github.com/google/or-tools) | 14,125 | Apache-2.0 | Use official scheduling examples in Phase 3 |
| [MapLibre GL JS](https://github.com/maplibre/maplibre-gl-js) | 11,774 | README identifies BSD-3-Clause | Candidate map renderer in Phase 4 |
| [shadcn/ui](https://github.com/shadcn-ui/ui) | 124,834 | MIT | Inspect individual accessible primitives in Phase 4 |

MapLibre's API license field returned NOASSERTION; inspect its complete license
files before copying source rather than relying on metadata alone.

No repository source was copied or cloned into this project. Existing work
already matches the requested stack, so importing a full starter would add
migration work. Reuse maintained packages and small documented patterns instead.

When adapting actual source, record commit, path, license, local destination,
changes, and relevant tests. Keep required notices. Avoid dependencies or visual
effects chosen solely because a repository has many stars.
