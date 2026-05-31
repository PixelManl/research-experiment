# Provenance Contract

Every formal run must be auditable without reading chat history.

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

## Required capture

At run start:

1. Save the exact command to `command.txt`.
2. Save composed Hydra config to `.hydra/config.yaml`.
3. Save git commit hash to `provenance.json` (格式详见 `../project-structure/outputs-organization.md`).
4. Save whether the tree is dirty.
5. Save `git diff --binary` to `git.diff.patch`.
6. Save Python/package/CUDA/device summary to `environment.txt`.
7. Save seed and deterministic flags.
8. Save task-slot and run name.

## Git diff patch

The patch file is mandatory even when empty.

Implementation requirement:

```python
def write_git_diff_patch(output_dir: Path) -> None:
    patch = subprocess.run(
        ["git", "diff", "--binary"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    (output_dir / "git.diff.patch").write_text(patch)
```

If the repository is not a git repo, fail unless `cfg.debug.allow_no_git=true`.

## Status file

Write `status.json` at both start and finish:

```json
{
  "status": "running|success|failed|invalidated",
  "task_slot": "ppo-handwritten",
  "started_at": "...",
  "finished_at": null,
  "failure_reason": null
}
```

If an exception occurs, allow the program to crash after writing failure status. Do not swallow errors.

## Invalidated runs

When a baseline, formula, reward, or data bug invalidates prior outputs:

- update `outputs/<task-slot>/index.md`;
- update `docs/research-log/invalidated-results.md`;
- update `docs/research-log/source-of-truth.md`;
- state which dates/runs must not be cited.

## Forbidden

- “I remember this run used lr=...” as provenance.
- Only saving terminal output.
- Only saving a metrics screenshot.
- Running with dirty code and no patch.
