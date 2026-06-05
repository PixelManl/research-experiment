# Experiment Modules Index

This layer defines how task logic is split across process, metrics, diagnostics, evaluation, figures, and reports. The goal is flat and reviewable code, not decorative architecture.

## Documentation Files

| File | Purpose | When to Read | Priority |
|---|---|---|---|
| [process-metric-diagnose.md](./process-metric-diagnose.md) | Split responsibilities across process, metrics, diagnostics, artifacts, and reports | Writing a task flow, moving logic out of main scripts, refactoring large files | Must Read |
| [evaluation-and-baselines.md](./evaluation-and-baselines.md) | Baseline ledger, metric definitions, and result validity | Adding metrics, changing baselines, comparing methods | Must Read |
| [figures.md](./figures.md) | Figure code, source data, and plotting specifications | Creating plots, paper figures, or shared figure layouts | Must Read |
| [reports.md](./reports.md) | Markdown/JSON reports and claim-ready summaries | Writing task reports, experiment summaries, or paper-facing evidence | Conditional |

## Quick Navigation by Task

Writing a task's main scientific flow?

- Read [process-metric-diagnose.md](./process-metric-diagnose.md).
- Keep script/main responsible for config, logging, provenance, seeding, validation, and calling process code.
- Put training/evaluation flow in `process.py` or task-scoped process helpers.

Adding or changing metrics?

- Read [process-metric-diagnose.md](./process-metric-diagnose.md) and [evaluation-and-baselines.md](./evaluation-and-baselines.md).
- Keep metric functions pure or near-pure.
- Record metric definition changes before comparing old and new outputs.

Changing a baseline?

- Read [evaluation-and-baselines.md](./evaluation-and-baselines.md).
- Update the baseline ledger and source-of-truth files.
- Check whether old outputs must be invalidated before making claims.

Adding diagnostics?

- Read [process-metric-diagnose.md](./process-metric-diagnose.md).
- Gate expensive or debug-only diagnostics behind config.
- Keep diagnostics separate from the formal metric path.

Creating figures or reports?

- Read [figures.md](./figures.md), [reports.md](./reports.md), and [../agent-collaboration/claims-and-decisions.md](../agent-collaboration/claims-and-decisions.md).
- Link figures and tables to valid run ids and source data.
- Do not create paper-facing figures from invalidated or undocumented outputs, and do not treat figures as claims without the required decision evidence.

## Core Rules Summary

- Script/main code must not contain reward math, training logic, metric formulas, plotting details, or ad hoc file naming.
- `process.py` may be linear and explicit; split only when there is real reuse, testing, review, or diagnostic separation value.
- Baseline and metric changes must be recorded before results are compared or cited.
- Figure and report artifacts must trace back to valid outputs and frozen definitions.
