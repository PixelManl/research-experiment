# Data Schema Contract

Do not pass naked dicts between modules. Data contracts must be explicit.

## When to Read

Read this before:

- adding `Transition`, `RolloutBatch`, `RunResult`, artifact, or metric-result objects;
- passing research data across module boundaries;
- adapting external library outputs into internal code;
- replacing dict-based data flow with typed contracts.

## Required module

```text
src/<package>/schema.py
```

Use `dataclass(frozen=True)` or `NamedTuple`.

Example:

```python
@dataclass(frozen=True)
class Transition:
    obs: torch.Tensor       # [B, *obs_shape]
    action: torch.Tensor    # [B]
    reward: torch.Tensor    # [B]
    done: torch.Tensor      # [B], bool
    info: tuple[dict, ...]  # boundary only; do not use as core contract

@dataclass(frozen=True)
class RolloutBatch:
    obs: torch.Tensor       # [T, B, *obs_shape]
    actions: torch.Tensor   # [T, B]
    rewards: torch.Tensor   # [T, B]
    dones: torch.Tensor     # [T, B], bool
    values: torch.Tensor    # [T + 1, B]
```

## Rules

- Dataclass fields must include shape comments.
- Boundary adapters may accept dicts from external libraries, but must convert immediately.
- Internal modules accept schema objects, not dicts.
- Optional fields must be explicit and validated.

## Boundary adapter pattern

```python
def transition_from_env_step(step: EnvStep) -> Transition:
    transition = Transition(...)
    validate_transition(transition)
    return transition
```

## Forbidden

```python
# Wrong
batch["reward"]
batch["done"]
batch["whatever_new_key"]
```

Use:

```python
batch.rewards
batch.dones
```

## Test requirement

Any new schema requires:

```text
tests/<task-slot>/test_schema_contract.py
```

Check construction, shapes, dtype, and invalid cases.
