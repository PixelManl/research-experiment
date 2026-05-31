# Evaluation and Baselines Contract

Baseline correctness is a scientific dependency. Treat it as a source-of-truth object, not memory.

## Required baseline ledger

```text
docs/research-log/baselines.md
```

Format:

```markdown
| Baseline | Implementation | Config | Validation evidence | Status |
|---|---|---|---|---|
| PPO-handwritten | `src/<package>/algorithms/ppo.py` | `configs/task/ppo-handwritten.yaml` | `tests/ppo-handwritten`, smoke run link | active |
```

## Baseline change rule

If a baseline changes, update:

- `docs/research-log/baselines.md`;
- `docs/research-log/source-of-truth.md`;
- `docs/research-log/invalidated-results.md`;
- affected `outputs/<task-slot>/index.md`.

Then explicitly state which previous comparisons are invalid.

## Metric definition

Each metric must have:

- formula or natural language definition;
- implementation file/function;
- unit or scale;
- aggregation rule;
- test or validation evidence.

Use `metrics.py` for computation and `reports.md`/output summaries for presentation.

## Result validity

A result can support a claim only if:

1. provenance exists;
2. config is available;
3. git diff patch is saved;
4. baseline status was active at run time;
5. relevant objections are resolved or explicitly acknowledged;
6. human approves claim level.

## Forbidden

- changing a baseline and keeping old plots as if comparable;
- letting an agent “remember” a baseline definition;
- reporting a metric without defining aggregation;
- mixing exploratory and claim-ready outputs in one table.
