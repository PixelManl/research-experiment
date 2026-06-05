# Process / Metrics / Diagnostics Contract

The goal is a flat but not messy design.

## When to Read

Read this before:

- deciding where task flow, metrics, diagnostics, artifacts, or reports belong;
- moving logic out of scripts or `main`;
- splitting a large `process.py` file;
- adding debug-only probes or expensive diagnostics.

## Recommended module roles

```text
src/<package>/
├── process.py       # end-to-end computation for a task
├── metrics.py       # metrics, scalar summaries, tables
├── diagnostics.py   # debug checks, sanity plots, expensive probes
├── artifacts.py     # save/load outputs when needed
└── reports.py       # optional markdown/json summaries
```

## `main` / script responsibility

Allowed in script/main:

- load config;
- set output directory;
- set logging;
- set seed;
- write provenance;
- call validation;
- call `process.run(cfg)`;
- write final status.

Forbidden in script/main:

- reward math;
- training logic;
- metric formulas;
- plotting details;
- ad hoc file naming.

## `process.py`

`process.py` owns the scientific flow:

```python
def run(cfg: Config) -> RunResult:
    data = load_or_generate_data(cfg)
    validate_data(data)
    model = build_model(cfg)
    result = train_or_evaluate(model, data, cfg)
    metrics = compute_metrics(result, cfg)
    save_artifacts(result, metrics, cfg)
    return RunResult(metrics=metrics, artifacts=...)
```

It can be linear and explicit. Do not split just to look “architected”.

## When to split

Split out of `process.py` when:

- a block has its own tests;
- the function is reused by another task-slot;
- the file is becoming hard to review;
- diagnostic code is debug-only or expensive;
- metrics are changing independently from training.

## `metrics.py`

Metrics functions should be pure or near-pure:

```python
def compute_reward_summary(batch: RolloutBatch) -> dict[str, float]:
    ...
```

No hidden global config. No output directory writes unless explicitly named `write_*`.

## `diagnostics.py`

Diagnostics are allowed to be expensive but must be gated:

```yaml
debug:
  diagnostics: true
```

## File size guide

Not a hard rule, but if one file exceeds ~400 lines, ask:

- Is it one coherent narrative?
- Are there independent tested concepts inside?
- Would a human reviewer know where to look?

If not, split.
