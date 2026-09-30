# Repository structure

The API and console live in one repository. This map covers the files a
teammate is most likely to open while preparing the demo.

```text
README.md                    Team entry point
AGENTS.md                    Work and verification rules
.env.example                 Configuration names without credentials
docker-compose.yml           Local PostgreSQL/PostGIS and API
apps/
  api/
    app/
      main.py                API assembly and database lifespan
      bootstrap.py           Explicit schema and synthetic fixture setup
      api/v1/endpoints/      HTTP routes
      core/                  Settings, async sessions, authorization
      models/                SQLAlchemy tables
      schemas/               Validated request and response types
      services/              Evidence, graph, cascade, planning, Gemini
    data/                    Fictional coastal district fixture
    database/                Generated schema and PostGIS migration
    tests/                   API, persistence, and solver tests
    requirements*.lock       Pinned Python dependencies
  web/
    src/app/                 Page, styles, and same-origin API proxy
    src/app/_components/     Console layout and state
    src/features/assets/     Map, asset table, legend, inspector
    src/features/observations/ Evidence form
    src/features/recovery/    Plan, comparison, Gemini briefing
    src/lib/                 API client and shared types
    tests/                   Playwright browser checks
    package-lock.json        Pinned web dependencies
docs/                        Architecture, API, design, phase evidence
scripts/                     Dev launcher and verification checks
```

In the API, `snapshot.py` captures the scenario inputs. `fusion.py` and
`topology.py` assess evidence and relationships, `cascade.py` runs seeded
simulations, and `plan_builder.py` with `scheduler.py` builds a recovery plan.
`recovery.py` saves plan versions and their deterministic diff. The briefing
services read those saved records for Gemini. See [architecture](architecture.md),
[API](api.md), and [current verification](phase-4-status.md).
