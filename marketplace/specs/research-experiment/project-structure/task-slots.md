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
outputs/<task-slot>/
docs/research-log/tasks/<task-slot>.md
```

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
- Outputs: `outputs/<task-slot>/index.md`
- Ledger: `docs/research-log/tasks/<task-slot>.md`
```

## Lifecycle states

- `active`: current work.
- `paused`: evidence incomplete; do not add new sweeps until decision is made.
- `invalidated`: key assumption or baseline changed; old outputs must not support claims.
- `archived`: useful history, no active code path.

## Forbidden

- Reusing a task-slot for a different scientific question.
- Creating a new task-slot only because the first run failed.
- Continuing an invalidated task-slot without updating the source-of-truth ledger.
