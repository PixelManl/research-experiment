# Tensor Shapes and Typing Contract

Tensor shape bugs are scientific bugs. Every important tensor flow must be auditable.

## Required shape comment

For nontrivial tensor transformations:

```python
# shapes:
#   logits:  [T, B, A]
#   actions: [T, B]
#   logp:    [T, B]
logp_all = F.log_softmax(logits, dim=-1)
logp = logp_all.gather(-1, actions.unsqueeze(-1)).squeeze(-1)
```

## Data schema annotations

In `src/<package>/schema.py`, define shapes in comments/docstrings (详见 `data-schema.md`):

```python
@dataclass(frozen=True)
class RolloutBatch:
    obs: torch.Tensor       # [T, B, *obs_shape]
    actions: torch.Tensor   # [T, B]
    rewards: torch.Tensor   # [T, B]
    dones: torch.Tensor     # [T, B], bool
    values: torch.Tensor    # [T + 1, B]
```

## Shape validation

Shape validation belongs in `src/<package>/validate.py`, not scattered through main logic.

```python
def validate_rollout_batch(batch: RolloutBatch) -> None:
    T, B = batch.rewards.shape
    assert batch.actions.shape == (T, B)
    assert batch.dones.shape == (T, B)
    assert batch.values.shape == (T + 1, B)
```

## Test requirement

For each new algorithm or data flow, add a tiny tensor test:

```text
tests/<task-slot>/test_tensor_shapes.py
```

It should check:

- expected shape;
- dtype;
- mask behavior;
- batch/time dimension ordering.

## Forbidden

- Passing tensors through naked dicts with undocumented keys.
- Using `view`/`reshape` without explaining dimension semantics.
- Relying on broadcasting when dimensions could be accidentally swapped.
- Silent squeeze that might remove batch dimension when `B=1`.
