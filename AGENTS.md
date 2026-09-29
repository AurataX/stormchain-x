# STORMCHAIN-X agent contract

Read [docs/README.md](docs/README.md), [system](docs/system.md),
[architecture](docs/architecture.md), [tasks](docs/tasks.md), and
[design](docs/design/README.md) before edits. Original requirements remain in
[arcitecture.md](docs/arcitecture.md) and [intial.md](docs/intial.md).

Implement only the authorized phase. Phase 2 is authorized; Phase 3 requires confirmation.
Current code includes the Python backend through Phase 2. Frontend is unbuilt
(Phase 4); optimizer is unbuilt (Phase 3). Read [handoff](docs/phase-2-review.md).
Update tasks and verification evidence after changes; never label planned work complete.
Use Atelier structure/design/clean-code principles and Ponytail minimalism.
Keep every authored source file at most 250 whitespace-separated words;
split by responsibility, never compress formatting to evade the limit.
Markdown, generated schema, lockfiles, and fixture data are exempt.
Use `python scripts/check_size.py` to enforce this manually.

Prefer async database sessions, validated inputs, parameterized queries,
explicit transactions, and real persistence tests. Keep synthetic data labeled.
Never infer failure from missing telemetry. Never invent optimizer outputs,
performance claims, credentials, deployment status, or registry components.
No paid provisioning or external deployment without explicit authorization.

Read [agent workflow](docs/agent-workflow.md) and [review checklist](docs/review.md).
These are model-independent requirements: follow them even without Atelier installed.
Inspect files before editing; implement one acceptance criterion at a time.
Run the relevant tests, source-size gate, lint, and schema-drift check before
marking work complete. Never replace tests with assertions in prose.
Preserve readable formatting; do not weaken checks to pass them.
Record changed files, executed commands, failures, and the next incomplete task.
GCP access is READ-ONLY: list/describe metadata only; never enable APIs, change
configuration/IAM, deploy, delete, or read secret values without new authorization.

Local storage is limited: after Docker testing, remove this project's containers,
images, volumes, and build cache following [cleanup](docs/docker-cleanup.md).
Demo database contents are disposable; retain fixtures, code, and test evidence.
Never delete unrelated Docker resources or cloud resources under this rule.

Preserve the user's graphify instruction: `/graphify` invokes the graphify
skill before other work. If a Skill tool is unavailable, read its SKILL.md
through available tools and report any missing capability honestly.
