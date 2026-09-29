# Project entry point

Follow [AGENTS.md](AGENTS.md). The same contract applies to every coding agent.

Read [documentation index](docs/README.md), [system](docs/system.md),
[architecture](docs/architecture.md), [implementation](docs/implementation.md),
[design](docs/design/README.md), [tasks](docs/tasks.md), and
[deployment](docs/deployment.md).

Do not mistake the aspirational source blueprint for implemented functionality.
Phase 2 is now authorized. Wait for confirmation before Phase 3.
The current implementation is Python backend through Phase 2; there is no
frontend yet. Start from [current handoff](docs/phase-2-review.md), not old status messages.
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
