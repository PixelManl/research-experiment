# Scripts Organization Contract

Scripts are execution surfaces. Core methods belong in `src/<package>/`; scripts call them.

## When to Read

Read this before:

- adding or reorganizing scripts;
- creating task run, sweep, data-processing, plotting, or inspection entrypoints;
- adding remote or SSH launch helpers;
- deciding whether logic belongs in `scripts/` or reusable `src/<package>/` modules.

## Required layout

```text
scripts/
├── index.md
├── common/
│   ├── legacy_args.py
│   ├── launch.py
│   └── inspect_run.py
├── remote/
│   ├── index.md
│   ├── ssh_check.py
│   └── launch_remote.py
└── <task-slot>/
    ├── index.md
    ├── run.py
    ├── sweep.py
    ├── process_data.py
    └── plot.py
```

## Root `scripts/index.md`

Use a compact table:

```markdown
| Area | Entry | Purpose |
|---|---|---|
| common | `scripts/common/launch.py` | shared launch helpers |
| remote | `scripts/remote/launch_remote.py` | resource/SSH wrapper only |
| ppo-handwritten | `scripts/ppo-handwritten/run.py` | canonical PPO task run |
```

## Task script rules

Each `scripts/<task-slot>/index.md` must define:

- canonical smoke command;
- canonical full command;
- expected output directory;
- required config group;
- whether the script is active, paused, or archived.

## Script responsibilities

`run.py`:

- loads Hydra config;
- sets up logging/provenance/seed;
- validates config and environment;
- orchestrates reusable `src/<package>/` functions;
- calls `src/<package>/process.py` only for named processing helpers used by metrics, diagnostics, figures, or reports;
- writes summary.

`process_data.py`:

- transforms raw data into a versioned processed dataset;
- writes `manifest.json` with input hashes and config;
- never silently overwrites processed data.

`plot.py`:

- reads a run directory or manifest;
- calls `src/<package>/plotting.py`;
- writes figures under the corresponding run or `paper/figures/` only after human approval.

`remote/`:

- checks SSH/resource state;
- starts local task scripts on remote machines;
- never contains experiment math or metrics.

## Forbidden

- New root-level scripts such as `run_exp.py`, `plot_final.py`, `quick_test.py`.
- Duplicating core computation inside scripts.
- Moving the execution entrypoint into `src/<package>/process.py`.
- Adding Hydra or argparse entrypoints to `src/<package>/process.py`.
- Accumulating argparse options in scripts; use Hydra config instead.
- Writing two-line ad hoc metric outputs to terminal instead of structured output files.
