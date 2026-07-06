# Task-Slot Contract

A `<task-slot>` is the stable filesystem identity for one research workstream.

## When to Read

Read this before:

- creating a new research workstream;
- renaming, pausing, invalidating, or archiving a task-slot;
- adding aligned tests, scripts, outputs, or task ledgers;
- deciding whether a failed run needs a new task-slot or belongs to the existing one.

## Naming

Use short kebab-case:

```text
ppo-handwritten
cvar-sam-baseline
reward-shaping-v3
offline-ablation
```

Do not include dates in the task-slot name. Dates belong under `outputs/<task-slot>/<YYYY-MM-DD>/`.

## Required mapping

Every active task-slot must have the same name across:

```text
tests/<task-slot>/
scripts/<task-slot>/
outputs/<task-slot>/          # runs.jsonl + generated index.md + run dirs
docs/research-log/tasks/<task-slot>.md
```

Run identity inside a slot is `<task-slot>#<seq>` from the run registry; see [../experiment-runtime/run-registry.md](../experiment-runtime/run-registry.md).

## Task-slot index format

Each task-slot index should fit on one screen.

```markdown
# <task-slot>

Purpose: one sentence.

Canonical smoke command:
`python scripts/<task-slot>/run.py debug=smoke task.slot=<task-slot>`

Current status: active | paused | invalidated | archived

Links:
- Tests: `tests/<task-slot>/index.md`
- Scripts: `scripts/<task-slot>/index.md`
- Runs: `runs.py list <task-slot>` (registry: `outputs/<task-slot>/runs.jsonl`)
- Ledger: `docs/research-log/tasks/<task-slot>.md`
```

## Staged expansion vs new task-slot

A failed run, No-Go result, reviewer objection, or new substage does not automatically require a new task-slot or Trellis task.

Before creating a new task for a follow-up, read [staged-task-expansion.md](./staged-task-expansion.md). If the scientific object, code path, and claim boundary remain continuous, keep the current Trellis task as the control plane and append a new Stage to its PRD.

Create a new task-slot only when the research workstream itself changes: new scientific object, new claim target, new output family, mostly independent code path, archived prior task, or substantially different risk level.

## Lifecycle states

- `active`: current work.
- `paused`: evidence incomplete; do not add new sweeps until decision is made.
- `invalidated`: key assumption or baseline changed; old outputs must not support claims.
- `archived`: useful history, no active code path.

## Forbidden

- Reusing a task-slot for a different scientific question.
- Creating a new task-slot only because the first run failed.
- Creating a new Trellis task only because a continuous thread needs local substages such as A1/A2/A3.
- Continuing an invalidated task-slot without updating the source-of-truth ledger.

## Related Specs

- [staged-task-expansion.md](./staged-task-expansion.md)
- [tests-organization.md](./tests-organization.md)
- [scripts-organization.md](./scripts-organization.md)
- [outputs-organization.md](./outputs-organization.md)
