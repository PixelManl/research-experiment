# Experiment Modules Index

How task logic splits across scripts, process helpers, metrics, diagnostics,
evaluation, figures, and reports. Goal: flat, reviewable code — not decorative
architecture.

## Guidelines Index

| Guide | Description | When to Read |
|-------|-------------|--------------|
| [process-metric-diagnose.md](./process-metric-diagnose.md) | Split scripts / process / metrics / diagnostics / artifacts / reports | Run scripts, metric processing, large-file refactors |
| [evaluation-and-baselines.md](./evaluation-and-baselines.md) | Baseline ledger, metric definitions, result validity | Adding metrics, changing baselines, comparing methods |
| [figures.md](./figures.md) | Figure code, source data, plotting specifications | Plots, paper figures, shared layouts |
| [reports.md](./reports.md) | Markdown/JSON reports and claim-ready summaries | Task reports, experiment summaries, paper-facing evidence |

## Pre-Development Checklist

- [ ] Writing a task run layer → [process-metric-diagnose.md](./process-metric-diagnose.md):
      `scripts/<task-slot>/run.py` owns config/logging/provenance/seed/validation/orchestration;
      algorithm modules stay on mechanics only.
- [ ] Reusable preprocessing / composite assembly goes in `process.py` when it would
      otherwise bloat scripts or metric formulas.
- [ ] Metric/baseline changes → [evaluation-and-baselines.md](./evaluation-and-baselines.md);
      record definition changes before comparing old vs new outputs.
- [ ] Diagnostics stay separate from formal metrics and are config-gated when expensive.
- [ ] Figures/reports → [figures.md](./figures.md), [reports.md](./reports.md), and
      [../agent-collaboration/claims-and-decisions.md](../agent-collaboration/claims-and-decisions.md);
      link only to valid, source-backed run ids.
- [ ] Do not put reward math, training internals, metric formulas, or plotting details
      into the thin execution surface.

## Quality Check

- [ ] Script/main remains the execution surface without embedding core math or ad hoc naming.
- [ ] `process.py` is reusable preprocessing/composite assembly — not an entrypoint or
      output writer.
- [ ] Baseline and metric definition changes are recorded before claims.
- [ ] Figures and reports trace to valid run ids; invalidated outputs are not cited.
- [ ] Expensive diagnostics are gated and not mixed into the formal metric path.
