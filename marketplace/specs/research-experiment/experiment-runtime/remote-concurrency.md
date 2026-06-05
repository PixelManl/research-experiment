# Remote and Concurrency Contract

Remote scripts manage resources; they do not contain experiment logic.

## When to Read

Read this before:

- launching SSH, remote, batch, sweep, or multi-machine jobs;
- running multiple experiments concurrently;
- writing remote launch helpers or resource snapshots;
- deciding how seeds, logs, output paths, and manifests behave under concurrency.

## Required layout

```text
scripts/remote/
├── index.md
├── ssh_check.py
├── launch_remote.py
└── resource_snapshot.py
```

## Remote script responsibilities

Allowed:

- check SSH availability;
- inspect GPU/CPU/memory;
- create remote output directory;
- call task scripts with Hydra overrides;
- copy back `outputs/<task-slot>/...`;
- write launch metadata.

Forbidden:

- computing metrics;
- implementing algorithms;
- changing reward formulas;
- embedding large config logic.

## Concurrency preconditions

Before launching concurrent runs:

1. smoke run passed locally or on target machine;
2. output directory pattern creates unique run directories;
3. stdout/stderr are captured to files;
4. each run has a unique seed or explicitly shared seed;
5. resource budget is documented;
6. no run writes to the same mutable artifact path.

## Concurrency manifest

For a batch/sweep, write:

```text
outputs/<task-slot>/<YYYY-MM-DD>/<batch-id>/batch_manifest.json
```

Minimum fields:

```json
{
  "task_slot": "ppo-handwritten",
  "runs": [
    {"seed": 0, "command": "...", "output_dir": "..."}
  ],
  "resource_plan": "2 GPUs, max 4 concurrent processes",
  "launched_by": "local|remote",
  "status": "running|success|partial|failed"
}
```

## Required after remote run

Copy or persist:

- `provenance.json`;
- `git.diff.patch`;
- `.hydra/config.yaml`;
- logs;
- metrics;
- failure status.

If a remote run cannot capture provenance, it is exploratory only.
