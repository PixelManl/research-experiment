# Project Structure Index

Filesystem contract for research experiment projects. This index is navigation
only; detailed rules live in the linked files.

## Guidelines Index

| Guide | Description | When to Read |
|-------|-------------|--------------|
| [directory-layout.md](./directory-layout.md) | Repository boundaries and required top-level layout | Initializing a project, moving files, deciding where code belongs |
| [task-slots.md](./task-slots.md) | `<task-slot>` naming, mapping, and lifecycle | Creating, pausing, invalidating, or archiving a research workstream |
| [staged-task-expansion.md](./staged-task-expansion.md) | PRD stage expansion for continuous research threads | Deciding Stage A/B/C or A1/A2/A3 vs a new Trellis task |
| [tests-organization.md](./tests-organization.md) | Task-scoped test organization | Adding or reorganizing tests |
| [scripts-organization.md](./scripts-organization.md) | Task-scoped scripts plus common/remote helpers | Adding experiment scripts, remote scripts, or reusable helpers |
| [outputs-organization.md](./outputs-organization.md) | Output paths, indexes, run validity states | Designing run outputs, cleaning results, invalidating outputs |
| [cleanup-dead-code.md](./cleanup-dead-code.md) | Dead-code, old-version, and variant cleanup | Removing old implementations, preserving variants, finishing a task |

## Pre-Development Checklist

- [ ] Confirm the work uses a stable `<task-slot>` shared by `tests/`, `scripts/`,
      `outputs/`, and `docs/research-log/tasks/` ([task-slots.md](./task-slots.md)).
- [ ] Before creating a new Trellis task for a follow-up stage, read
      [staged-task-expansion.md](./staged-task-expansion.md).
- [ ] For complex Trellis 0.6 tasks: `prd.md` = stage/value, `design.md` =
      contracts, `implement.md` = execution/validation gates.
- [ ] Adding tests → [tests-organization.md](./tests-organization.md); keep them
      under `tests/<task-slot>/` unless genuinely common.
- [ ] Adding scripts → [scripts-organization.md](./scripts-organization.md);
      task scripts under `scripts/<task-slot>/`, shared under `common/` / `remote/`.
- [ ] Creating/cleaning outputs → [outputs-organization.md](./outputs-organization.md);
      formal path `outputs/<task-slot>/<YYYY-MM-DD>/<run-id>/`.
- [ ] Removing old code → [cleanup-dead-code.md](./cleanup-dead-code.md); prefer
      git history + ledger notes over `old.py` / `v2.py`.
- [ ] Keep root and task-slot indexes short: directory, command, status, links.

## Quality Check

- [ ] Same research workstream uses the same `<task-slot>` across tests/scripts/outputs/ledger.
- [ ] Continuous research expanded stages inside the current PRD when the scientific
      object, code path, and claim boundary stayed continuous.
- [ ] No task-specific glue left in repo root or reusable `src/<package>/` modules.
- [ ] Deprecated implementations are traced via git/ledger, not dead files.
- [ ] `tests/index.md`, `scripts/index.md`, and task indexes remain short and linked.
- [ ] Output layout still matches the outputs contract; invalid runs are marked,
      not silently deleted without ledger notes.
