# Process / Metrics / Diagnostics Contract

The goal is a flat but not messy design, with a strict boundary between execution entrypoints and reusable research code.

## When to Read

Read this before:

- deciding where task flow, metrics, diagnostics, artifacts, or reports belong;
- moving logic out of scripts or `main`;
- splitting a large `process.py` file;
- adding debug-only probes or expensive diagnostics.

## Execution boundary

`scripts/<task-slot>/` owns execution. `src/<package>/process.py` is not an entrypoint.

Allowed execution surfaces:

- `scripts/<task-slot>/run.py`;
- `scripts/<task-slot>/sweep.py`;
- `scripts/<task-slot>/process_data.py`;
- `scripts/<task-slot>/plot.py`;
- shared launch wrappers under `scripts/common/` or `scripts/remote/`.

Forbidden in `src/<package>/process.py`:

- `@hydra.main`;
- `argparse`;
- choosing output directories;
- writing `status.json` as the top-level run owner;
- launching sweeps or remote jobs;
- acting as `python -m <package>.process`;
- owning an end-to-end training/evaluation run such as `process.run(cfg)`.

## Recommended module roles

```text
src/<package>/
├── process.py       # reusable heavy processing helpers for metrics/diagnostics/reports
├── metrics.py       # metrics, scalar summaries, tables
├── diagnostics.py   # debug checks, sanity plots, expensive probes
├── artifacts.py     # save/load outputs when needed
└── reports.py       # optional markdown/json summaries
```

`process.py` exists because metric and diagnostic code often needs a heavy preparation layer that should not live inside `metrics.py`, `diagnostics.py`, or a task script.

## Script responsibility

Allowed in script/main:

- load config;
- set output directory;
- set logging;
- set seed;
- write provenance;
- call validation;
- call reusable core methods from `src/<package>/`;
- call named processing helpers when metrics or diagnostics need prepared inputs;
- write final status.

Forbidden in script/main:

- reward math;
- training logic;
- metric formulas;
- plotting details;
- ad hoc file naming.

## `process.py`

`process.py` contains reusable processing functions used by metrics, diagnostics, figures, or reports. It should prepare structured intermediate data, not run the experiment.

Good examples:

```python
def build_metric_inputs(run_dir: Path, cfg: Config) -> MetricInputs:
    events = load_event_table(run_dir)
    rollouts = load_rollout_summary(run_dir)
    return MetricInputs(events=events, rollouts=rollouts)


def prepare_diagnostic_batch(result: TrainResult, cfg: Config) -> DiagnosticBatch:
    batch = extract_rollout_windows(result.rollouts, cfg.diagnostics.window)
    return validate_diagnostic_batch(batch)
```

These functions may be heavier than pure metric functions. They should still be deterministic, named for their data contract, and testable without launching a run.

Bad examples:

```python
@hydra.main(...)
def main(cfg):
    ...


def run(cfg):
    train()
    write_outputs()
    launch_sweep()
```

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
def compute_reward_summary(inputs: MetricInputs) -> dict[str, float]:
    ...
```

No hidden global config. No output directory writes unless explicitly named `write_*`. If a metric needs expensive aggregation first, put that aggregation in `process.py` and keep the metric formula inspectable here.

## `diagnostics.py`

Diagnostics are allowed to be expensive but must be gated:

```yaml
debug:
  diagnostics: true
```

Diagnostics may call `process.py` helpers to prepare heavy diagnostic inputs. They must not become hidden run entrypoints.

## File size guide

Not a hard rule, but if one file exceeds ~400 lines, ask:

- Is it one coherent narrative?
- Are there independent tested concepts inside?
- Would a human reviewer know where to look?

If not, split.

## Anti-patterns

- Adding a Hydra entrypoint to `src/<package>/process.py`.
- Telling users to run `python -m <package>.process`.
- Moving task orchestration from `scripts/<task-slot>/run.py` into `process.py`.
- Hiding metric formulas inside a large processing block.
- Hiding expensive diagnostics inside the formal metric path.
