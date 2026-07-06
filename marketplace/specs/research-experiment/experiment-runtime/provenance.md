# Provenance Contract

Every formal run must be auditable without reading chat history.

## Purpose

This contract makes formal runs reproducible, comparable, and invalidatable from files alone. A reader should be able to inspect a run directory and know what code, config, command, environment, and status produced it — and restore the exact code state with one git command.

## When to Read

Read this before:

- creating or modifying a formal run entrypoint;
- launching heavy compute or remote jobs;
- comparing outputs in a report or figure;
- deciding whether old outputs remain valid after a code, data, baseline, or formula change.

## Integration point

One context manager owns all capture. Run commands gain no new arguments:

```python
@hydra.main(version_base=None, config_path="../../configs", config_name="config")
def main(cfg: DictConfig) -> None:
    with provenance.tracked_run(cfg) as run:
        result = train(cfg, run.out_dir)
        run.metrics(return_mean=result.return_mean)
```

On enter it allocates the registry run id, snapshots the git tree, writes all provenance files, and appends the `run` event; on exit (including crashes) it writes final status and appends the `end` event. Reference implementation: `examples/run-registry/provenance.py`. For unmodifiable legacy/external code, use `runs.py wrap` (Level 0) instead; see [run-registry.md](./run-registry.md).

## Required files per run

```text
outputs/<task-slot>/<YYYY-MM-DD>/<run-id>/
├── .hydra/
├── command.txt
├── environment.txt
├── git.diff.patch
├── provenance.json
├── run.log
├── status.json
└── metrics.json
```

## Required capture at run start

1. Registry run id (`<task-slot>#<seq>`) — allocated automatically.
2. Git snapshot ref `refs/runs/<task-slot>/<seq>` of the exact tree (see below).
3. Exact command to `command.txt`.
4. Composed Hydra config to `.hydra/config.yaml` and its hash.
5. Git commit hash and dirty flag.
6. `git diff --binary` to `git.diff.patch` (mandatory even when empty).
7. Python/package/CUDA/device summary to `environment.txt`, including `sys.executable`.
8. Seed and deterministic flags.
9. Host name and timezone-aware ISO 8601 timestamp — remote and multi-machine runs are not auditable without them.

## `provenance.json`

```json
{
  "run_id": "ppo-handwritten#0007",
  "task_slot": "ppo-handwritten",
  "git_commit": "abc1234...",
  "git_dirty": true,
  "git_snapshot": "9f3e21d...",
  "git_snapshot_ref": "refs/runs/ppo-handwritten/0007",
  "git_diff_patch": "git.diff.patch",
  "config_path": ".hydra/config.yaml",
  "config_hash": "5f2a8c1e77b0",
  "command": "python scripts/ppo-handwritten/run.py run.name=gae-fix",
  "executable": "C:/envs/rl/python.exe",
  "host": "gpu-1",
  "seed": 0,
  "created_at": "2026-06-03T09:14:12+08:00",
  "notes": ""
}
```

No status field. Execution status lives in `status.json`; validity lives only in the registry ([run-registry.md](./run-registry.md)).

## Git snapshot

A commit hash alone is not a version identifier when the tree is dirty: two runs at the same commit can execute different code. Each run therefore gets a snapshot ref — a real commit of the working tree including uncommitted and untracked files, created via a temporary index without touching the working tree or branch history:

```text
refs/runs/<task-slot>/<seq>
```

- Restore any run's exact code: `git worktree add <dir> refs/runs/<task-slot>/<seq>`.
- Compare any two runs' exact code: `git diff <snap-a> <snap-b>` (what `runs.py compare` does).
- `git.diff.patch` remains as a quick human-browsable view; the snapshot is the reproducibility mechanism.
- Precondition: heavy paths (`outputs/`, `data/`, checkpoints) must be gitignored or they enter every snapshot.
- Optional cross-machine sync: `git push origin "refs/runs/*:refs/runs/*"`.

If the repository is not a git repo, fail unless `cfg.debug.allow_no_git=true`.

## Status file

`status.json` records the execution axis only:

```json
{
  "status": "running|success|failed",
  "task_slot": "ppo-handwritten",
  "started_at": "2026-06-03T09:14:12+08:00",
  "finished_at": null,
  "failure_reason": null
}
```

Written at start and finish. If an exception occurs, write failure status, append the `end` event, then let the program crash. Do not swallow errors.

## Invalidated runs

When a baseline, formula, reward, or data bug invalidates prior outputs:

```bash
python scripts/common/runs.py invalidate "<task-slot>#<seq>" --reason "..." --by <human>
```

This appends the registry event and regenerates index views. Additionally update:

- `docs/research-log/invalidated-results.md` (cite run ids);
- `docs/research-log/source-of-truth.md`;
- state which run ids must not be cited.

## Forbidden

- "I remember this run used lr=..." as provenance.
- Only saving terminal output or a metrics screenshot.
- Running with dirty code and no snapshot/patch.
- Reconstructing a command with a different Python executable than the run used.
- Local timestamps without UTC offset; provenance without `host`.
- Storing validity in `provenance.json` or `status.json`.

## Related Specs

- [run-registry.md](./run-registry.md)
- [hydra-configuration.md](./hydra-configuration.md)
- [python-command.md](./python-command.md)
- [logging.md](./logging.md)
- [smoke-dry-run.md](./smoke-dry-run.md)
- [../project-structure/outputs-organization.md](../project-structure/outputs-organization.md)
- [../agent-collaboration/pre-heavy-run-review.md](../agent-collaboration/pre-heavy-run-review.md)
