# Experiment Modules Index

This layer defines how task logic is split across script entrypoints, process helpers, metrics, diagnostics, evaluation, figures, and reports. The goal is flat and reviewable code, not decorative architecture.

## Documentation Files

| File | Purpose | When to Read | Priority |
|---|---|---|---|
| [process-metric-diagnose.md](./process-metric-diagnose.md) | Split responsibilities across scripts, process helpers, metrics, diagnostics, artifacts, and reports | Writing run scripts, metric/diagnostic processing, or refactoring large files | Must Read |
| [evaluation-and-baselines.md](./evaluation-and-baselines.md) | Baseline ledger, metric definitions, and result validity | Adding metrics, changing baselines, comparing methods | Must Read |
| [figures.md](./figures.md) | Figure code, source data, and plotting specifications | Creating plots, paper figures, or shared figure layouts | Must Read |
| [reports.md](./reports.md) | Markdown/JSON reports and claim-ready summaries | Writing task reports, experiment summaries, or paper-facing evidence | Conditional |

## Quick Navigation by Task

Writing a task run or processing layer?

- Read [process-metric-diagnose.md](./process-metric-diagnose.md).
- Keep `scripts/<task-slot>/run.py` responsible for config, logging, provenance, seeding, validation, and top-level orchestration.
- Keep algorithm/runtime modules focused on algorithm mechanics, not complex metric, diagnostic, or report aggregation.
- Keep `src/<package>/process.py` as reusable data preprocessing and composite result assembly for metrics, diagnostics, figures, reports, and status decisions; it is not an execution entrypoint.
- Put core training/evaluation logic in reusable `src/<package>/` modules such as runner, policy, loss, objective, or environment adapters.

Adding or changing metrics?

- Read [process-metric-diagnose.md](./process-metric-diagnose.md) and [evaluation-and-baselines.md](./evaluation-and-baselines.md).
- Keep metric functions pure or near-pure.
- Put data preprocessing or composite metric/diagnostic/status assembly in `process.py` when it would otherwise bloat the script, algorithm, or metric formula.
- Record metric definition changes before comparing old and new outputs.

Changing a baseline?

- Read [evaluation-and-baselines.md](./evaluation-and-baselines.md).
- Update the baseline ledger and source-of-truth files.
- Check whether old outputs must be invalidated before making claims.

Adding diagnostics?

- Read [process-metric-diagnose.md](./process-metric-diagnose.md).
- Gate expensive or debug-only diagnostics behind config.
- Keep diagnostics separate from the formal metric path.
- Use `process.py` for reusable diagnostic input preparation or composite diagnostic/status assembly, not for launching diagnostic runs.

Creating figures or reports?

- Read [figures.md](./figures.md), [reports.md](./reports.md), and [../agent-collaboration/claims-and-decisions.md](../agent-collaboration/claims-and-decisions.md).
- Link figures and tables to valid run ids and source data.
- Do not create paper-facing figures from invalidated or undocumented outputs, and do not treat figures as claims without the required decision evidence.

## Core Rules Summary

- Script/main code is the execution surface, but must not contain reward math, training internals, metric formulas, plotting details, or ad hoc file naming.
- Algorithm/runtime modules serve algorithm mechanics only; complex statistics and diagnostics belong outside them.
- `process.py` is a reusable preprocessing and composite-result module, not an entrypoint or output writer; split only when there is real reuse, testing, review, or diagnostic separation value.
- Baseline and metric changes must be recorded before results are compared or cited.
- Figure and report artifacts must trace back to valid outputs and frozen definitions.
