# Experiment Runtime Index

How an experiment is started, configured, recorded, reproduced, and run
concurrently. This index is navigation only; runtime contracts live in the
linked files.

## Guidelines Index

| Guide | Description | When to Read |
|-------|-------------|--------------|
| [config-source-of-truth.md](./config-source-of-truth.md) | Config truth system; prevent config drift | **Every experiment** — highest priority |
| [hydra-configuration.md](./hydra-configuration.md) | Hydra entry, strict config, debug groups | Adding entrypoints, config fields, experiment groups |
| [run-registry.md](./run-registry.md) | Run id, two-axis status, git snapshot, `runs.py` CLI | Locating / comparing / promoting / invalidating runs |
| [python-command.md](./python-command.md) | Cross-platform Python interpreter rules | Running helpers, standardizing commands |
| [provenance.md](./provenance.md) | Config, commit, snapshot, command, env, status capture | Formal runs, comparing results |
| [smoke-dry-run.md](./smoke-dry-run.md) | Minimum smoke and dry-run checks | Before heavy compute; after main-flow changes |
| [logging.md](./logging.md) | Log levels, stdout/stderr capture | Entrypoints, concurrent runs, diagnostics |
| [remote-concurrency.md](./remote-concurrency.md) | Remote resources, concurrency prerequisites | SSH/remote jobs, multi-process or multi-machine sweeps |

## Pre-Development Checklist

- [ ] **Config truth first**: read [config-source-of-truth.md](./config-source-of-truth.md);
      confirm `configs/truth/config.yaml` and `configs/truth/config_truth.md` exist
      and match what the run will use.
- [ ] Formal entry uses Hydra; new parameters go into schema/config groups, not a
      growing argparse surface ([hydra-configuration.md](./hydra-configuration.md)).
- [ ] Formal run path includes `<task-slot>`, date, and run name; registration goes
      through provenance / `runs.jsonl` ([provenance.md](./provenance.md),
      [run-registry.md](./run-registry.md)).
- [ ] Python commands use the verified project interpreter
      ([python-command.md](./python-command.md)).
- [ ] Before heavy compute: smoke evidence + pre-heavy-run review
      ([smoke-dry-run.md](./smoke-dry-run.md),
      [../agent-collaboration/pre-heavy-run-review.md](../agent-collaboration/pre-heavy-run-review.md)).
- [ ] Remote/concurrent work: log redirection + concurrency manifest
      ([remote-concurrency.md](./remote-concurrency.md), [logging.md](./logging.md)).
- [ ] Locate/compare/promote/invalidate runs only via `runs.py`, never by walking
      date directories or writing one-off aggregation scripts.

## Quality Check

- [ ] Config was verified against truth before the formal run.
- [ ] Formal runs are registered in `outputs/<task-slot>/runs.jsonl` with git
      snapshot; validity changes only via `runs.py promote|invalidate`.
- [ ] Provenance artifacts present: config, commit, snapshot, command, env, logs,
      status, metrics.
- [ ] Smoke evidence exists for any expensive job; `runs.py check` (if used) passed.
- [ ] Failures write failure status before crashing; errors are not swallowed into
      a fake success.
- [ ] Concurrent/remote runs have file-backed logs and recorded resource assumptions.
