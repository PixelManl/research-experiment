# Validation and Assertions Contract

科研代码应该 fail fast。不要用 try-catch 把错误变成“看起来能跑”。

## Required module

```text
src/<package>/validate.py
```

Put preconditions and cross-field checks here.

## Main flow pattern

Good:

```python
validate_config(cfg)
validate_rollout_batch(batch)
loss = compute_loss(batch, cfg)
```

Bad:

```python
if batch is not None:
    if batch.rewards is not None:
        if batch.rewards.shape[0] > 0:
            ...
```

## Assertion style

Use `assert` or explicit exceptions for invariants. The project is research code; crashing early is correct.

Good:

```python
assert rewards.ndim == 2, f"expected [T, B], got {tuple(rewards.shape)}"
finite_or_raise(loss, "loss")
```

Avoid broad exception handling:

```python
# Wrong
try:
    train()
except Exception:
    print("failed, continuing")
```

## Validation levels

- `validate_config(cfg)`: config and paths.
- `validate_schema(obj)`: dataclass/NamedTuple data contract.
- `finite_or_raise(tensor, name)`: finite checks (delegated to `numerics.py`).
- `validate_pre_heavy_run(cfg)`: compute budget, smoke result, provenance readiness.

## When try/except is allowed

Only at the top-level boundary to write `status.json`, then re-raise.

```python
try:
    result = process.run(cfg)
except Exception as exc:
    write_failure_status(output_dir, exc)
    raise
```

## Forbidden

- catching errors and returning default metrics;
- falling back to different algorithm/data silently;
- skipping validation because “this is just a quick run”;
- writing validation logic as scattered nested if blocks in `main`.
