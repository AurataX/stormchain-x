# STORMCHAIN-X

Uncertainty-aware cyclone infrastructure recovery decision-support prototype.

The Python backend implements constrained persistence, synthetic infrastructure,
observation ingestion, evidence fusion, dependency/access graphs, and seeded
cascade simulations with saved inputs/results. Optimization is Phase 3;
the Next.js operations console is Phase 4 and does not exist yet.

Start with [local development](docs/local-development.md),
[architecture](docs/architecture.md), and [verification](docs/verification.md).
See [Phase 2 semantics](docs/phase-2-engine.md) and
[Docker cleanup](docs/docker-cleanup.md) before running simulations.

```powershell
uv venv .venv
uv pip sync --python .venv/Scripts/python.exe apps/api/requirements-dev.lock
.venv/Scripts/python.exe scripts/verify.py
```

See [documentation index](docs/README.md) for design, hosting, API contracts,
phase tasks, and the read-only GCP inventory. Agents must follow
[AGENTS.md](AGENTS.md) and [CLAUDE.md](CLAUDE.md).

All infrastructure and observations are synthetic. This project does not
operate real infrastructure or claim validated disaster predictions.
