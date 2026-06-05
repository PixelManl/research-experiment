# Outputs Organization Contract

Outputs must be traceable, indexable, and invalidatable. The goal is not to keep every artifact forever; the goal is to know what each artifact means.

## When to Read

Read this before:

- creating a formal run output directory;
- writing metrics, figures, diagnostics, artifacts, or processed data;
- marking runs valid, failed, invalidated, superseded, or claim-ready;
- comparing, citing, cleaning, or archiving outputs.

## Path convention

Use:

```text
outputs/<task-slot>/<YYYY-MM-DD>/<HHMMSS>-<run-name>/
```

Example:

```text
outputs/ppo-handwritten/2026-05-31/143012-smoke-gae-check/
```

Avoid `MM:dd` because `:` is inconvenient or invalid on some filesystems and shells.

## Required run directory contents

Every formal run must contain:

```text
run.log
status.json
metrics.json
provenance.json
git.diff.patch
command.txt
environment.txt
.hydra/
artifacts/
figures/
diagnostics/
```

Minimum `provenance.json`:

```json
{
  "task_slot": "ppo-handwritten",
  "run_status": "exploratory|valid|claim-ready|failed|invalidated|superseded",
  "git_commit": "...",
  "git_dirty": true,
  "git_diff_patch": "git.diff.patch",
  "config_path": ".hydra/config.yaml",
  "command": "python scripts/ppo-handwritten/run.py debug=smoke",
  "created_at": "YYYY-MM-DDTHH:MM:SS",
  "notes": "short human-readable note"
}
```

## Index files

`outputs/index.md`:

```markdown
| Task slot | Latest valid run | Status | Notes |
|---|---|---|---|
| ppo-handwritten | `2026-05-31/143012-smoke-gae-check` | valid | smoke passes |
```

`outputs/<task-slot>/index.md`:

```markdown
| Date/run | Status | Config | Metrics | Claim usage |
|---|---|---|---|---|
| `2026-05-31/143012-smoke-gae-check` | valid | `.hydra/config.yaml` | `metrics.json` | smoke only |
```

Keep indexes short. Do not paste large logs or full metric tables.

## Validity states

- `exploratory`: may inform debugging, not claims.
- `valid`: passed required checks and can support internal decisions.
- `claim-ready`: human approved; can support paper/report claims.
- `failed`: failed due to code/config/runtime; may still contain useful debug evidence.
- `invalidated`: must not support future claims.
- `superseded`: replaced by a later valid run.

## Data processing outputs

Persistent processed data belongs in:

```text
data/processed/<task-slot>/<dataset-version>/
```

A data processing script under `scripts/<task-slot>/process_data.py` must write:

```text
manifest.json
input_hashes.json
config.yaml
```

Run-specific derived artifacts remain under `outputs/<task-slot>/.../artifacts/`.

## Git ignore recommendation

Track indexes, ignore heavy outputs:

```gitignore
outputs/**
!outputs/
!outputs/index.md
!outputs/*/
!outputs/*/index.md
```

Do not rely on ignored outputs as the only record of scientific conclusions; important conclusions belong in `docs/research-log/`.
