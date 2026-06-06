# Research Experiment Scaffold Contract

## Purpose

Create the minimum filesystem structure needed for a Research-Experiment spec to become actionable.

This contract only covers skeleton files and directories.

## Target Layout

```text
.
├── src/<package>/
│   ├── __init__.py
│   ├── config/
│   ├── policy/
│   └── runner/
├── configs/
│   ├── config.yaml
│   ├── schema.py
│   ├── task/<task-slot>.yaml
│   ├── experiment/default.yaml
│   ├── debug/off.yaml
│   ├── debug/smoke.yaml
│   ├── debug/dry_run.yaml
│   └── hydra/
├── scripts/
│   ├── index.md
│   ├── common/
│   ├── remote/
│   └── <task-slot>/index.md
├── tests/
│   ├── index.md
│   ├── common/
│   └── <task-slot>/index.md
├── outputs/
│   ├── index.md
│   └── <task-slot>/index.md
└── docs/
    ├── main/main.md
    └── research-log/
        ├── index.md
        ├── baselines.md
        ├── source-of-truth.md
        ├── invalidated-results.md
        ├── reviewer-objections.md
        └── tasks/<task-slot>.md
```

Optional project-specific directories such as `data/processed/<task-slot>/`, `docs/research-log/decisions/`, `docs/research-log/reports/`, and `docs/research-log/equation-maps/` may be added by the project or future commands.

## Write Policy

- Create missing directories needed by planned files.
- Create missing files with conservative placeholders.
- Skip existing files by default.
- Report conflicts instead of overwriting.
- Use `--force` only after explicit user approval.
- Do not force task scripts when an existing package entrypoint already exists.
- Do not create `plans/`, canonical design documents, source notes, or research planning material.
