# Before Development Checklist

Use this before starting a new research task.

## When to Use

Use this guide before:

- starting a new task-slot;
- making a substantial code, config, baseline, metric, or output change;
- assigning ownership tier for AI/human collaboration;
- defining minimum tests and canonical commands.

## 1. Define task-slot

```text
<task-slot> =
```

Check or create:

- `tests/<task-slot>/index.md`
- `scripts/<task-slot>/index.md`
- `outputs/<task-slot>/index.md`
- `docs/research-log/tasks/<task-slot>.md`

## 2. Classify ownership

- T1 AI can implement:
- T2 AI can draft, human approves:
- T3 human-owned:

## 3. Identify scientific contract

- formula/equation:
- data schema:
- tensor shapes:
- metric definition:
- baseline dependency:
- reviewer objection:

## 4. Define minimum tests

- math invariant:
- shape invariant:
- numerics edge case:
- smoke path:

## 5. Define canonical commands

Interpreter:

```bash
python -c "import sys; print(sys.executable)"
```

Smoke:

```bash
python scripts/<task-slot>/run.py debug=smoke
```

Tests:

```bash
pytest tests/<task-slot> -q
```

## 6. Confirm no stale source

Check:

- `docs/research-log/source-of-truth.md`
- `docs/research-log/invalidated-results.md`
- `docs/research-log/baselines.md`
