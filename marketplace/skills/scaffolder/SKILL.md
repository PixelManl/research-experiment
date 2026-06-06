---
name: scaffolder
description: Create or audit a conservative filesystem scaffold for a Research-Experiment project. Use when an agent needs to initialize a near-empty repository or add a task-slot with aligned configs, tests, scripts, outputs, and research-log placeholders according to the Research-Experiment Trellis spec.
---

# Research Experiment Scaffolder

Create or audit a Research-Experiment filesystem scaffold.

## Use when

- the repository is empty or near-empty and needs an initial skeleton;
- a new task-slot needs aligned config, test, script, output, and research-log files;
- a read-only audit is needed before adding files.

## Do not use for

- scientific decisions;
- algorithm code, training loops, baselines, metrics, reports, or claims;
- plans, canonical design docs, or source notes;
- read-only inspection tasks that should not write anything.

## Commands

Run from this skill directory, or replace `scripts/...` with the installed skill path.

```bash
python scripts/scaffold_research_experiment.py audit --root <target-repo>
python scripts/scaffold_research_experiment.py add-task --root <target-repo> --task-slot <task-slot>
python scripts/scaffold_research_experiment.py init-project --root <target-repo> --package <package> --task-slot <task-slot>
```

## Rules

- Run `audit` first.
- Dry-run first; use `--apply` only after review.
- Use `--force` only with explicit approval.
- Do not create `.trellis/spec/`.
- Do not create scaffold files for read-only inspection or validation tasks.
- Do not create `plans/`, canonical design plans, paper/source notes, or long-lived research planning material.
- Do not force `run.py` or `plot.py` when an existing project already uses a package entrypoint.
- Prefer missing indexes and task ledgers over modifying existing content.

## Files

- `scripts/scaffold_research_experiment.py`
- `references/scaffold_contract.md`
- `references/task_slot_contract.md`
- `references/adaptation_patterns.md`
