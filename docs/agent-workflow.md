# Model-independent working agreement

This contract applies equally to every model and editor. No optional plugin
installation is required to understand or enforce it.

Before work:

1. Read AGENTS.md, system, architecture, tasks, verification, and relevant design docs.
2. Inspect actual files and identify the current phase. Do not infer completion.
3. Trace input → validation → service → persistence → response before editing.
4. Name the smallest acceptance criterion and its test.

During work:

- Reuse existing patterns. Avoid placeholders, silent fallbacks, and speculative frameworks.
- Keep thin routes, async sessions, typed schemas, UTC time, integer money, stable IDs.
- Validate foreign keys, authorization, duplicate submissions, and scenario boundaries.
- Preserve documentation provenance. Never overwrite source requirements with guesses.
- Keep source files ≤250 words with normal formatting and cohesive responsibilities.
- Consult official docs for changing APIs. Record source, license, and version before reuse.
- GCP inventory is read-only metadata; do not inspect credentials or secret contents.

Before handoff:

1. Run relevant tests and the documented quality commands, including local documentation links.
2. Review the diff for unintended scope, data loss, secrets, and stale documentation.
3. Record commands, actual results, environmental blocks, and known limitations.
4. Update tasks only where evidence satisfies acceptance.
5. Stop at the authorized phase boundary.

If a check fails, reproduce and fix the cause. Do not remove the check or
replace code with hardcoded output. If blocked, state the concrete blocker.
