# Task-Slot Scaffold Contract

## Purpose

Add a stable filesystem identity for one research workstream.

## Required Alignment

For a task-slot `<task-slot>`, the scaffold should align:

```text
configs/task/<task-slot>.yaml
tests/<task-slot>/index.md
scripts/<task-slot>/index.md
outputs/<task-slot>/index.md
docs/research-log/tasks/<task-slot>.md
```

## Shared Areas

Preserve shared areas such as:

```text
tests/contracts/
tests/smoke/
scripts/common/
scripts/remote/
docs/research-log/decisions/
docs/research-log/equation-maps/
```

Do not convert shared areas into task-slots.

## Entrypoints

Do not assume every task needs `run.py` or `plot.py`.
If an existing project uses a package entrypoint, record that command in `scripts/<task-slot>/index.md`.

## Write Policy

- Create missing task-slot files.
- Skip existing files.
- Do not append to root indexes unless a future command explicitly supports reviewed index updates.
- Report missing links as warnings for human review.
