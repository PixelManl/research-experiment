# Experiment Runtime Index

This layer defines how an experiment is started, configured, recorded, reproduced, and run concurrently. This index is navigation only; runtime contracts and implementation details belong in the linked files.

## Documentation Files

| File | Purpose | When to Read | Priority |
|---|---|---|---|
| [hydra-configuration.md](./hydra-configuration.md) | Hydra entrypoint, strict config, debug groups | Adding entrypoints, config fields, experiment groups, or legacy arg adapters | Must Read |
| [provenance.md](./provenance.md) | Config, commit, diff, command, environment, and status capture | Creating formal runs, comparing results, organizing outputs | Must Read |
| [smoke-dry-run.md](./smoke-dry-run.md) | Minimal smoke and dry-run checks | Before heavy compute, after main-flow changes, while debugging config | Must Read |
| [logging.md](./logging.md) | Log levels, stdout/stderr capture, run logs | Adding entrypoints, running concurrently, enabling diagnostics | Must Read |
| [remote-concurrency.md](./remote-concurrency.md) | Remote resources, concurrency preconditions, manifests | SSH/remote runs, multi-process runs, multi-machine sweeps | Conditional |

## Quick Navigation by Task

Adding or changing Hydra config?

- Read [hydra-configuration.md](./hydra-configuration.md).
- Put new parameters in schema/config groups, not a growing argparse surface.
- Confirm unknown keys fail fast for formal runs.

Launching a formal run?

- Read [hydra-configuration.md](./hydra-configuration.md), [provenance.md](./provenance.md), [logging.md](./logging.md), and [../project-structure/outputs-organization.md](../project-structure/outputs-organization.md).
- Ensure the run saves config, command, environment, commit, diff patch, status, metrics, and log.
- Confirm the output path includes `<task-slot>`, date, run id, and validity state handling.

Before heavy compute?

- Read [smoke-dry-run.md](./smoke-dry-run.md) and [../agent-collaboration/pre-heavy-run-review.md](../agent-collaboration/pre-heavy-run-review.md).
- Run smoke first and preserve the evidence.
- Do not launch expensive jobs before provenance and review are complete.

Running remotely or concurrently?

- Read [remote-concurrency.md](./remote-concurrency.md), [logging.md](./logging.md), and [provenance.md](./provenance.md).
- Redirect logs to files before parallel execution.
- Record concurrency manifest and machine/resource assumptions.

Debugging config or data paths?

- Read [smoke-dry-run.md](./smoke-dry-run.md).
- Use dry run for config/path validation and smoke run for a tiny real execution.

## Core Rules Summary

- Formal runs must be Hydra-driven.
- Every formal run must save config, commit, git diff patch, command, environment, log, status, and metrics.
- Heavy compute requires smoke-run evidence and pre-heavy-run review.
- Exceptions may crash after failure status is written; do not swallow errors to make a run look successful.
