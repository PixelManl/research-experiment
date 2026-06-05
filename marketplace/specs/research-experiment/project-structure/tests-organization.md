# Tests Organization Contract

Research tests exist to catch math, shape, boundary, gradient-direction, and trajectory-reward errors before they contaminate experiments. They are not meant to grow into an unmaintainable pile of heavyweight training tests.

## When to Read

Read this before:

- adding tests for a task-slot;
- changing reward, rollout, loss, tensor shape, gradient, or smoke-path behavior;
- deleting, disabling, consolidating, or promoting tests;
- deciding whether a test belongs in `tests/<task-slot>/` or `tests/common/`.

## Required layout

```text
tests/
├── index.md
├── common/
│   └── ...
└── <task-slot>/
    ├── index.md
    ├── test_reward_contract.py
    ├── test_tensor_shapes.py
    ├── test_gradient_direction.py
    └── test_smoke_pipeline.py
```

## Root `tests/index.md`

Keep it concise:

```markdown
| Task slot | Required command | Scope | Status |
|---|---|---|---|
| ppo-handwritten | `pytest tests/ppo-handwritten -q` | GAE, reward, smoke | active |
```

## Task test index

`tests/<task-slot>/index.md` must list why each test exists:

```markdown
| File | Invariant checked | Delete/promote rule |
|---|---|---|
| `test_gae_math.py` | Eq. GAE recursion on tiny tensors | Keep while PPO exists |
| `test_reward_contract.py` | terminal/truncation/boundary rewards | Promote if reused |
| `test_smoke_pipeline.py` | end-to-end debug config finishes | Keep |
```

## Test budget

Default budget for one task-slot:

- 3-8 focused unit tests for math/schema/numerics.
- 1 smoke pipeline test.
- 0 heavy training tests.
- Add more only when each test has a named failure mode.

If a task-slot exceeds ~12 test functions, consolidate or promote common invariants to `tests/common/`.

## RL-specific required checks

For RL/trajectory code, test at least:

- reward sign and boundary cases;
- terminal vs truncated transitions;
- advantage normalization when variance is zero or mask is empty;
- gradient direction on a tiny deterministic example;
- rollout schema shapes before training.

## Forbidden

```python
# Wrong: heavyweight training as a unit test
def test_ppo_learns_cartpole_after_1m_steps():
    ...

# Wrong: testing print output instead of contract
assert "looks good" in captured.out
```

Use tiny tensors, deterministic toy environments, and exact or tolerance-based invariants.

## Required before deleting tests

When deleting or disabling a test, update `tests/<task-slot>/index.md` with:

- reason;
- replacement test or ledger link;
- whether the old result is invalidated.
