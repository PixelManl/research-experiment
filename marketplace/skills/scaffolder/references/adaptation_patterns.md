# Adaptation Patterns

## Existing Project First

When the target repository is not empty, run `audit` first and treat the scaffold as an adapter.

Preserve:

- existing package modules under `src/<package>/`;
- existing Hydra `configs/config.yaml`;
- shared tests such as `tests/contracts/` and `tests/smoke/`;
- root indexes if they already contain project-specific notes;
- existing task ledgers and output indexes.

## Package Entrypoint Pattern

Some research projects use package entrypoints instead of task-local scripts. In that case, `scripts/<task-slot>/index.md` should record commands and planned entries, not force `run.py`.

## Shared Test Pattern

Use `tests/contracts/` and `tests/smoke/` for global invariants. Use `tests/<task-slot>/` for task-specific checks.

## Skeleton-Only Boundary

This skill may create conservative placeholders and indexes, but it must not create research plans, paper/source notes, canonical design documents, baselines, metrics, claims, or experiment results.
