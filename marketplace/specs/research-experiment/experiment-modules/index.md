# Experiment Modules Index

本层规定实验任务内部如何拆分 process、metrics、diagnostics、evaluation、figures 和 reports。

| Topic | File | Status |
|---|---|---|
| Process / metric / diagnose split | `process-metric-diagnose.md` | Template |
| Evaluation and baselines | `evaluation-and-baselines.md` | Template |
| Figures | `figures.md` | Template |
| Reports | `reports.md` | Template |

## Non-negotiable

- `main` 只做启动、配置、溯源、调用流程；不要堆统计胶水。
- `process.py` 可以承载主流程，但超过职责边界时拆到 `metrics.py`、`diagnostics.py`、`artifacts.py`。
- Baseline 变更必须进入 source-of-truth ledger。
