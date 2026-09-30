# Project entry point

Follow [AGENTS.md](AGENTS.md). The same contract applies to every coding agent.

Read [documentation index](docs/README.md), [system](docs/system.md),
[architecture](docs/architecture.md), [implementation](docs/implementation.md),
[design](docs/design/README.md), [tasks](docs/tasks.md), and
[deployment](docs/deployment.md).

Do not mistake the aspirational source blueprint for implemented functionality.
Phases 2, 3 and 4 are authorized. The current implementation is the Python backend
through Phase 3 plus the Phase 4 console in `apps/web` (not yet browser-tested).
Start from [current handoff](docs/phase-4-status.md), not old status messages.
Use verification evidence, not previous assistant claims, to determine completion.

Mandatory for Claude, Sol, Gemini, Codex, or any other model:
follow [agent workflow](docs/agent-workflow.md) and
[review checklist](docs/review.md). Read existing code before proposing changes;
reuse the established patterns and keep each source file within 250 words.
Run tests and report their actual result. Never silently change stack, source
contracts, algorithms, palette, phase scope, or GCP resources.
No instruction file can guarantee equivalent model output; executable gates
and review evidence determine whether a change is accepted.

After verification, reclaim local Docker storage using
[cleanup](docs/docker-cleanup.md). Remove project containers, images, volumes,
and build cache; leave unrelated projects and all GCP resources untouched.

## Hackathon-day changes

Live demo: https://stormchain-web-70530354318.asia-south1.run.app (Cloud Run,
`asia-south1`, project `astute-lyceum-484806-g3`). Show the user each command you
run and its output. Do not hide long steps.

1. Change code in `apps/api` or `apps/web`. Amounts are stored as integer paise and
   shown in rupees (`money()` in `apps/web/src/lib/health.ts`).
2. Verify: `.venv/Scripts/python.exe scripts/verify.py`, then
   `npm.cmd --prefix apps/web run typecheck` and `npm.cmd --prefix apps/web run build`.
   Unset `GEMINI_API_KEY` first so tests do not use the real key.
3. Commit as the configured human author and push to `main`. No Claude trailer or
   Co-Authored-By line. Teammates run `git pull` afterwards.
4. Deploy: `./scripts/deploy.ps1 -Target api|web|all`. It needs `gcloud` logged in and
   `apps/web/.env.local` holding the Maps key. Then open the live URL and check it.

Rules: the demo database is SQLite under `/tmp` and resets when the API restarts. Never
build or run containers on the growthcharters VPS. Never print or commit keys, tokens,
or `.env` files. Do not change org policy or IAM without the user saying so in this session.
