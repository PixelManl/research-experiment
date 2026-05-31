# Failure Evidence Ledger Contract

Failed experiments are evidence. They should help decide whether to stop, reframe, or debug.

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
| 2026-05-20 | ppo-handwritten | before 2026-05-20 | reward bug | pending |
```

## Agent duty

Before citing any old result, AI must check:

- `source-of-truth.md`;
- `invalidated-results.md`;
- `outputs/<task-slot>/index.md`;
- baseline ledger.

## Forbidden

- Hiding failed runs.
- Retelling failed runs as “almost worked” without evidence.
- Using old invalidated data because it supports the story.
- Continuing parameter sweeps when a cheaper bug/assumption diagnostic is available.
