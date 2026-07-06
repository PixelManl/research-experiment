# Run Registry Contract

The registry is the machine-readable source of truth for run identity, status, and lineage. Markdown indexes are generated views of it. Agents locate, compare, and audit runs through one CLI instead of walking date directories and writing one-off scripts.

## Purpose

This contract answers, from files alone and in one command:

- Which run is the current canonical result for a task-slot?
- What changed (code, config, metrics) between run A and run B?
- Which runs must not support claims?

It also removes the two failure modes of hand-edited index tables: silent drift (agent forgets to update) and ambiguous truth (two runs both look "valid" with no ordering).

## When to Read

Read this before:

- locating, citing, or comparing past runs;
- promoting, superseding, or invalidating a run;
- writing provenance capture code or wrapping legacy entrypoints;
- regenerating `outputs/**/index.md`.

## Files

```text
outputs/<task-slot>/runs.jsonl     # append-only event log; git-tracked; THE truth
outputs/<task-slot>/index.md       # generated view; never hand-edited
scripts/common/runs.py             # the only read/write CLI surface
```

Run directories under `outputs/<task-slot>/<YYYY-MM-DD>/<HHMMSS>-<run-name>/` keep full provenance detail; registry lines are the summary and index of them.

## Run identity

- `run_id = <task-slot>#<seq>`, e.g. `ppo-handwritten#0007`. Sequence is per-slot, zero-padded, allocated under a lock at append time.
- Every run gets a git snapshot ref `refs/runs/<task-slot>/<seq>`: a real commit object capturing the exact working tree (including uncommitted and untracked files), created without touching the working tree or branch history. A commit hash alone is NOT a version identifier when the tree is dirty; the snapshot is.
- Reproduce any run: `git worktree add <dir> refs/runs/<task-slot>/<seq>`.
- Precondition: `outputs/`, `data/`, and other heavy paths must be gitignored, otherwise snapshots capture them. See the gitignore snippet in `examples/repo-files/gitignore-snippet.md`.

## Two status axes

Execution axis — written by the running process, answers "did it finish":

```text
running | success | failed
```

Validity axis — changed only by explicit registry events, answers "can it be trusted":

```text
exploratory | valid | claim-ready | invalidated | superseded
```

A run can be `success` + `invalidated` (ran fine, config was wrong) or `failed` + kept as failure evidence. The two axes never conflict because no file stores them together: `status.json` owns execution state only; validity exists only as registry events. `provenance.json` has no status field.

## Events

Append-only JSONL, one event per line. History is never rewritten; corrections are new events.

```jsonl
{"ev":"run","id":"ppo-handwritten#0007","path":"2026-06-03/091412-gae-fix","exec":"running","git":"abc1234","dirty":true,"snap":"9f3e21d","cfg_hash":"5f2a8c1e77b0","seed":0,"host":"gpu-1","cmd":"python scripts/ppo-handwritten/run.py run.name=gae-fix","at":"2026-06-03T09:14:12+08:00"}
{"ev":"end","id":"ppo-handwritten#0007","exec":"success","metrics":{"return_mean":234.1},"at":"2026-06-03T11:02:40+08:00"}
{"ev":"promote","id":"ppo-handwritten#0007","to":"valid","role":"canonical","supersedes":["ppo-handwritten#0004"],"by":"karen","note":"GAE fix rerun; 0004 superseded","at":"2026-06-03T12:00:01+08:00"}
{"ev":"invalidate","id":"ppo-handwritten#0003","reason":"reward bug before 2026-05-20 fix","by":"karen","at":"2026-06-03T12:01:00+08:00"}
{"ev":"note","id":"ppo-handwritten#0007","note":"used for fig 3 draft","at":"2026-06-04T09:00:00+08:00"}
```

Current state = fold(events) in file order: execution status is the last `run`/`end` exec value; validity starts `exploratory`, changed by `promote`/`invalidate`; a run listed in another promote's `supersedes` becomes `superseded`.

Timestamps are ISO 8601 with UTC offset. `host` is required; remote and multi-machine runs are meaningless without it.

## Canonical uniqueness

- Per task-slot, at most ONE run has `role: canonical` with validity `valid` or `claim-ready`. `latest <slot>` returns it or reports vacancy — never a guess.
- Promoting to `valid` as canonical while a canonical exists requires `--supersedes <old-id>` (old one becomes `superseded`), or a non-canonical role: `--role replicate --group <name>` (e.g. seed-sweep members) or `--role ablation`.
- Invalidating the canonical run leaves the slot canonical-VACANT. Nothing silently falls back to an older run; re-promote explicitly.

## Promotion gates

Enforced mechanically by `runs.py promote`, not by discipline:

| Target | Requires |
|---|---|
| `valid` | exec `success`; snapshot ref exists (or clean tree at a commit that exists) |
| `claim-ready` | already `valid`; clean pushed commit OR snapshot ref pushed to origin; human named in `--by` |

`claim-ready` promotion also scans figure sidecars and `docs/research-log/` for references to invalidated runs before allowing the promotion. Local-only evidence can be force-accepted with `--allow-local`, which records the override in the event.

## CLI surface

```text
runs.py latest <slot>                        # canonical run or explicit vacancy (exit 3)
runs.py list <slot> [--validity valid] [--exec success] [--since 2026-05-28] [--json]
runs.py show <id> [--json]                   # folded state + events + provenance.json
runs.py compare <id-a> <id-b>                # git diff between snapshots + config keys + metric deltas
runs.py promote <id> --to valid|claim-ready [--supersedes ...] [--role ...] [--by ...] [--note ...]
runs.py invalidate <id> --reason ... --by ...
runs.py note <id> --text ...
runs.py render [<slot>|--all]                # regenerate index.md views
runs.py check [<slot>]                       # invariants; exit 1 on violation
runs.py backfill <slot>                      # register pre-registry run dirs (no snapshot; marked backfilled)
runs.py wrap --slot <slot> --name <name> -- <command ...>   # zero-intrusion wrapper for legacy/external code
```

Write commands auto-regenerate the affected `index.md`. Agents must use these commands instead of globbing `outputs/` or writing ad hoc aggregation scripts; if a needed query is missing, extend `runs.py` (T1) rather than bypassing it.

## Registration levels

- Level 1 (default): `provenance.tracked_run(cfg)` inside the entrypoint appends `run`/`end` automatically, snapshots, and writes the provenance files. Run commands gain no new arguments; humans decide nothing at launch time. Promotion is a separate explicit post-hoc act (T2: agent drafts, human approves).
- Level 0 (fallback): `runs.py wrap -- <command>` registers from outside the process for code you cannot or should not modify. Captures exit code and logs, but no in-process metrics or composed config.
- Remote runs: the registry lives in the launching repo. Register via the launcher (wrap-style) or `backfill` after copying outputs back; a remote run without registration is exploratory by definition.

## `check` invariants

1. Every line parses; ids well-formed; per-slot seq unique.
2. Registered run paths exist on disk (backfilled/remote gaps reported, not fatal).
3. Canonical uniqueness per slot.
4. `valid`/`claim-ready` runs: snapshot ref (or clean commit) resolvable in git.
5. `cfg_hash` matches the stored composed config when present.
6. `claim-ready` runs: snapshot or commit reachable from origin (warn-only if no remote).
7. Generated `index.md` files are not stale.
8. No figure sidecar or research-log document cites an invalidated/superseded run id.

## Forbidden

- Hand-editing `runs.jsonl` or any generated `index.md`.
- Deleting or rewriting registry lines; corrections are new events.
- Storing validity anywhere except registry events (no `run_status` in `provenance.json`, no status column maintained by hand).
- One-off scripts that walk `outputs/` to answer a query `runs.py` already answers.
- Promoting to canonical `valid` without superseding or explicitly branching the existing canonical.
- Citing a run in figures/reports by directory path instead of run id.
- Heavy files outside gitignore (breaks snapshot correctness and repo size).

## Reference implementation

`examples/run-registry/` contains a liftable implementation: `runs.py` (stdlib-only, single file, library + CLI) and `provenance.py` (`tracked_run` context manager). Copy to `scripts/common/runs.py` and `src/<package>/provenance.py`, then adapt. Projects preferring a package module can move the core to `src/<package>/registry.py` and keep `runs.py` as a thin CLI.

## Related Specs

- [provenance.md](./provenance.md)
- [../project-structure/outputs-organization.md](../project-structure/outputs-organization.md)
- [../project-structure/task-slots.md](../project-structure/task-slots.md)
- [../experiment-modules/figures.md](../experiment-modules/figures.md)
- [../agent-collaboration/failure-evidence-ledger.md](../agent-collaboration/failure-evidence-ledger.md)
