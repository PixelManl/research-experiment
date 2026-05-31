# Break-Loop and CI Contract

After fixing a bug, ask: how will this class of bug never happen again?

## Required break-loop question

For every bug fix, answer in the task report:

```markdown
Bug:
Root cause:
Why tests/specs missed it:
Prevent-repeat mechanism:
New/updated test:
New/updated spec:
Invalidated outputs:
```

## Mapping from bug class to prevention

| Bug class | Prevention |
|---|---|
| tensor shape swap | shape validation + tiny tensor test |
| wrong formula | equation map + formula test |
| numerical instability | `numerics.py` safe primitive + edge test |
| stale baseline | baseline ledger + invalidated outputs |
| bad config key | Hydra structured config / struct mode |
| remote log loss | logging/provenance contract |
| output overwrite | output path uniqueness test/check |

## Minimal CI gate

At minimum, maintain a command that runs:

```bash
python -m compileall src scripts
pytest tests/common -q
```

Task-specific gate:

```bash
pytest tests/<task-slot> -q
python scripts/<task-slot>/run.py debug=smoke
```

Use CI if available; otherwise run manually and paste commands/results into the task report.

## Forbidden

- fixing the same bug repeatedly without a test/spec update;
- adding a test that only checks the current output string;
- closing a task with no explanation of what prevents recurrence.
