# Cleanup and Dead-Code Contract

Dead code is a research risk. It lets AI and humans accidentally reuse old baselines, old math, and old stories.

## When to Read

Read this before:

- finishing a task;
- deleting or keeping old implementations;
- preserving failed variants, probes, or legacy baselines;
- reviewing whether temporary files, dead paths, or obsolete args remain.

## Forbidden patterns

- `*_old.py`, `*_backup.py`, `*_v2.py`, `final_final.py`.
- Large commented-out blocks of previous implementations.
- Keeping unused CLI args “just in case”.
- Keeping old metric definitions without a ledger entry.
- Duplicating a function to change two lines.

## Allowed history mechanisms

Use:

- git commits, branches, or tags;
- `docs/research-log/decisions/`;
- `docs/research-log/invalidated-results.md`;
- concise comments linking to an issue/decision;
- `legacy/` only when still executed by a baseline or test.

## Keep/kill decision

Before finishing a task, classify every new or changed file:

| Class | Keep? | Requirement |
|---|---:|---|
| Core method | yes | imported by script/test and documented |
| Task script | yes | in `scripts/<task-slot>/index.md` |
| Task test | yes | in `tests/<task-slot>/index.md` |
| Temporary probe | no | delete or convert to diagnostic |
| Old implementation | no | use git history or ledger |
| Failed experiment output | maybe | mark failed/invalidated in output index |

## Required final cleanup check

Before task finish:

```bash
git status --short
git diff --stat
```

Then answer in the task summary:

1. Which temporary files were removed?
2. Which old code paths were deleted?
3. Which indexes were updated?
4. Which outputs were marked invalidated or superseded?

## If human wants to keep a variant

Move it to a named, tested variant:

```text
src/<package>/algorithms/<variant_name>.py
tests/<task-slot>/test_<variant_name>_contract.py
docs/research-log/decisions/YYYY-MM-DD-keep-<variant_name>.md
```

No untracked “maybe useful later” code.
