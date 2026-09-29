# Repository structure

```text
AGENTS.md / CLAUDE.md / README.md
docs/
  architecture.md / system.md / algorithms.md
  implementation.md / tasks.md / verification.md
  database.md / api.md / local-development.md
  hosting.md / deployment.md / references.md
  design/README.md / tokens.md / interactions.md / libraries.md
apps/api/
  Dockerfile / pyproject.toml / requirements.txt
  app/
    main.py / bootstrap.py
    core/       configuration, database, authorization
    models/     SQLAlchemy tables
    schemas/    validated request/response contracts
    services/   evidence, graph, cascade, snapshots, seeding, GeoJSON
    api/v1/endpoints/
  data/         synthetic fixture JSON
  database/     generated schema and PostGIS migration
  tests/        isolated API/database integration tests
scripts/        size, schema, documentation, and verification checks
docker-compose.yml / .env.example
.github/workflows/verify.yml   automated quality gates
```

Phase 4 adds `apps/web/src/app`, route-local `_components`, `components/ui`,
`features/{assets,observations,recovery}`, and `lib`. Shared components move
only when reused. No empty executable frontend or optimizer placeholders now.

Atelier principles: thin routes, cohesive services, language-specific names,
central tokens, and small files. Ponytail: no speculative services, interfaces,
workspace orchestrator, or monorepo tooling for a single frontend.
