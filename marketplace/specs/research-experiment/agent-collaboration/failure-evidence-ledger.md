# Failure Evidence Ledger Contract

Failed experiments are evidence. They should help decide whether to stop, reframe, or debug.

## When to Read

Read this before:

- marking a run failed, invalidated, superseded, or unusable for claims;
- citing old outputs after a bug, baseline change, formula change, or data change;
- deciding whether failure is a bug, evidence against the hypothesis, or a stop/reframe signal;
- updating source-of-truth or invalidated-results records.

## Required files

```text
docs/research-log/source-of-truth.md
docs/research-log/invalidated-results.md
docs/research-log/tasks/<task-slot>.md
```

## Source-of-truth entry

```markdown
## YYYY-MM-DD — <short fact>

Fact:
Evidence:
Affected outputs:
Action:
Owner:
```

Example:

```markdown
## 2026-05-20 — PPO baseline reward bug

Fact: reward normalization used post-terminal rewards incorrectly.
Evidence: `tests/ppo-handwritten/test_reward_contract.py`, run `outputs/ppo-handwritten/...`
Affected outputs: all `outputs/ppo-handwritten` before 2026-05-20
Action: mark invalidated; rerun baseline after fix
Owner: Karen
```

## Invalidated results table

```markdown
| Date | Task slot | Runs affected | Reason | Replacement |
|---|---|---|---|---|
| 2026-05-20 | ppo-handwritten | `ppo-handwritten#0001`..`#0005` | reward bug | pending |
```

Cite registry run ids. Mark the runs themselves with `runs.py invalidate <id> --reason ... --by ...` so `runs.py check` can catch any later citation of them.

## Agent duty

Before citing any old result, AI must check:

- `source-of-truth.md`;
- `invalidated-results.md`;
- `runs.py show <id>` — the run's current validity in the registry;
- baseline ledger.

## Forbidden

- Hiding failed runs.
- Retelling failed runs as “almost worked” without evidence.
- Using old invalidated data because it supports the story.
- Continuing parameter sweeps when a cheaper bug/assumption diagnostic is available.
