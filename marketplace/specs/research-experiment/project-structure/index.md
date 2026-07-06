# Project Structure Index

This layer defines the filesystem contract for research experiment projects. This index is navigation only; detailed rules belong in the linked files, not here.

## Documentation Files

| File | Purpose | When to Read | Priority |
|---|---|---|---|
| [directory-layout.md](./directory-layout.md) | Repository boundaries and required top-level layout | Initializing a project, moving files, deciding where code belongs | Must Read |
| [task-slots.md](./task-slots.md) | `<task-slot>` naming, mapping, and lifecycle | Creating, pausing, invalidating, or archiving a research workstream | Must Read |
| [staged-task-expansion.md](./staged-task-expansion.md) | PRD stage expansion protocol for continuous research threads | Deciding whether to append Stage A/B/C or A1/A2/A3 instead of creating a new Trellis task | Must Read |
| [tests-organization.md](./tests-organization.md) | Task-scoped test organization | Adding or reorganizing tests | Must Read |
| [scripts-organization.md](./scripts-organization.md) | Task-scoped scripts plus common/remote helpers | Adding experiment scripts, remote scripts, or reusable helpers | Must Read |
| [outputs-organization.md](./outputs-organization.md) | Output paths, indexes, run validity states | Designing run outputs, cleaning results, invalidating outputs | Must Read |
| [cleanup-dead-code.md](./cleanup-dead-code.md) | Dead-code, old-version, and variant cleanup | Removing old implementations, preserving variants, finishing a task | Conditional |

## Quick Navigation by Task

Starting a new task-slot?

- Read [task-slots.md](./task-slots.md).
- Read [staged-task-expansion.md](./staged-task-expansion.md) before creating a new Trellis task for a follow-up stage.
- Create aligned entries under `tests/`, `scripts/`, `outputs/`, and `docs/research-log/tasks/`.
- Update the nearest `index.md` with one-screen status and links.

Extending an ongoing Trellis task with Stage A/B/C or A1/A2/A3?

- Read [staged-task-expansion.md](./staged-task-expansion.md).
- Expand the current PRD when the scientific object, code path, and claim boundary remain continuous.
- In Trellis 0.6 complex tasks, keep `prd.md` for stage/value control, `design.md` for technical contracts, and `implement.md` for checklist and validation gates.
- Create a new task only when the object, claim target, output family, risk level, or control plane changes.

Adding tests?

- Read [tests-organization.md](./tests-organization.md).
- Keep tests under `tests/<task-slot>/` unless they are genuinely common.
- Link the required command from `tests/index.md` or `tests/<task-slot>/index.md`.

Adding experiment scripts?

- Read [scripts-organization.md](./scripts-organization.md).
- Put one-off task scripts under `scripts/<task-slot>/`.
- Put reusable or remote helpers under `scripts/common/` or `scripts/remote/`.

Creating or cleaning outputs?

- Read [outputs-organization.md](./outputs-organization.md).
- Use `outputs/<task-slot>/<YYYY-MM-DD>/<run-id>/` for formal runs; runs register automatically in `runs.jsonl`.
- Locate/compare runs with `runs.py latest|list|compare`; invalidate with `runs.py invalidate` plus a research ledger entry.

Cleaning old code?

- Read [cleanup-dead-code.md](./cleanup-dead-code.md).
- Prefer git history and ledger notes over `old.py`, `v2.py`, or commented-out code.

## Core Rules Summary

- `tests/`, `scripts/`, `outputs/`, and `docs/research-log/tasks/` must use the same `<task-slot>` for the same research workstream.
- A continuous research thread should expand stages inside the current Trellis task PRD instead of fragmenting into new tasks.
- Trellis 0.6 planning artifacts should stay separated: `prd.md` for value/stages, `design.md` for contracts, `implement.md` for execution and verification.
- Root indexes and task-slot indexes must stay short: directory, command, status, links.
- Task-specific glue does not belong in the repository root or reusable `src/<package>/` modules.
- Deprecated implementations are traced through git and ledger entries, not dead files.
