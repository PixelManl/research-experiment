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

## Algorithm / runtime boundary

Algorithm and runtime modules should serve the algorithm itself:

- policy/model forward pass;
- loss, reward, objective, or update rules;
- environment interaction and lifecycle primitives;
- rollout, buffer, sampler, trainer, or evaluator mechanics;
- algorithm-local validation and invariants.

Do not put complex statistical summaries, claim-facing metrics, health diagnostics, report aggregation, or ad hoc result classification inside algorithm/runtime modules. Those belong in `metrics.py`, `diagnostics.py`, or `process.py` so the algorithm stays inspectable.

## Recommended module roles

```text
src/<package>/
├── process.py       # data preprocessing and composite result assembly; not an entrypoint
├── metrics.py       # recorded metrics and complex mathematical metric functions
├── diagnostics.py   # diagnostic metrics, health checks, sanity probes
├── artifacts.py     # save/load outputs when needed
└── reports.py       # optional markdown/json summaries
```

`process.py` exists because metric and diagnostic code often needs preprocessing or a composite flow that does not fit in one metric or one diagnostic function.

## Script responsibility

Allowed in script/main:

- load config;
- set output directory;
- set logging;
- set seed;
- write provenance;
- call validation;
- call reusable core methods from `src/<package>/`;
- call named processing helpers for data preprocessing or composite metrics/diagnostics/status results;
- write metrics, diagnostics, artifacts, and status returned by reusable modules;
- write final status.

Forbidden in script/main:

- reward math;
- training logic;
- metric formulas;
- plotting details;
- ad hoc file naming.

## `process.py`

`process.py` contains reusable processing functions used by metrics, diagnostics, figures, or reports. It can preprocess data and assemble composite results that individual `metrics.py` or `diagnostics.py` functions cannot express cleanly.

Use `process.py` for:

- in-memory data preprocessing before metric or diagnostic computation;
- extracting windows, tables, summaries, or lifecycle slices from raw run results;
- coordinating a bounded lifecycle segment by calling algorithm/runtime primitives;
- combining metrics, diagnostics, and status decisions into one structured result;
- returning artifacts-to-write without writing them itself.

Do not use `process.py` for:

- Hydra or argparse entrypoints;
- output directory selection;
- provenance capture;
- direct file writes for formal run outputs;
- sweep, remote, or long-run orchestration;
- core algorithm math that belongs in algorithm/runtime modules.

Good examples:

```python
def preprocess_metric_inputs(result: TrainResult, cfg: Config) -> MetricInputs:
    events = extract_event_table(result)
    rollouts = summarize_rollouts(result.rollouts)
    return MetricInputs(events=events, rollouts=rollouts)


def prepare_diagnostic_batch(result: TrainResult, cfg: Config) -> DiagnosticBatch:
    batch = extract_rollout_windows(result.rollouts, cfg.diagnostics.window)
    return validate_diagnostic_batch(batch)


def summarize_lifecycle_segment(runtime: Runtime, cfg: Config) -> ProcessResult:
    segment = runtime.run_segment(cfg.segment)
    metric_inputs = preprocess_metric_inputs(segment, cfg)
    diagnostic_batch = prepare_diagnostic_batch(segment, cfg)
    metric_values = metrics.compute_all(metric_inputs, cfg.metrics)
    diagnostic_values = diagnostics.run_checks(diagnostic_batch, cfg.diagnostics)
    status = decide_status(metric_values, diagnostic_values, cfg.status_rules)
    return ProcessResult(
        metrics=metric_values,
        diagnostics=diagnostic_values,
        status_decision=status,
    )
```

These functions may be heavier than pure metric functions. They should still be deterministic, named for their data contract, and testable without writing output files.

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
def compute_kl_divergence(inputs: MetricInputs) -> float:
    ...


def compute_cost_rate(inputs: MetricInputs) -> dict[str, float]:
    ...
```

Use `metrics.py` for recorded metrics and complex mathematical metric functions such as KL, confusion matrices, rates, costs, scalar summaries, and comparison tables.

No hidden global config. No output directory writes unless explicitly named `write_*`. If a metric needs expensive aggregation first, put that aggregation in `process.py` and keep the metric formula inspectable here.

## `diagnostics.py`

Diagnostics are diagnostic metrics and health checks. The boundary with `metrics.py` can be fuzzy; the purpose is the same: keep complex computation out of algorithm/runtime modules.

Diagnostics are allowed to be expensive but must be gated:

```yaml
debug:
  diagnostics: true
```

Diagnostics may call `process.py` helpers to prepare heavy diagnostic inputs. They must not become hidden run entrypoints or formal metric paths unless explicitly promoted.

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
- Putting KL/rate/cost/confusion/report aggregation inside algorithm/runtime modules.
