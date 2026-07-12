# Research Code Index

Research code contract: reviewable math, tensor shapes, numerical safety,
explicit schemas, and reproducible randomness. This index is navigation only.

## Guidelines Index

| Guide | Description | When to Read |
|-------|-------------|--------------|
| [code-style.md](./code-style.md) | Simple, readable, direct research code | Writing or refactoring core implementation |
| [math-formula-mapping.md](./math-formula-mapping.md) | Formula-to-code alignment | Translating papers; changing loss/reward/objectives |
| [tensor-shapes-typing.md](./tensor-shapes-typing.md) | Tensor shape, dtype, and data-flow annotations | Models, rollout batches, losses, metrics, adapters |
| [validation-assertions.md](./validation-assertions.md) | Assertions and invariant validation | Preconditions, schemas, boundary checks |
| [numerics.md](./numerics.md) | Safe numerical primitives; NaN/Inf handling | log-prob, entropy, advantage norm, instability |
| [data-schema.md](./data-schema.md) | Dataclass / NamedTuple contracts | Transitions, batches, results across modules |
| [determinism.md](./determinism.md) | Global seed and reproducibility control | Training entrypoints, baseline comparisons |
| [profiling.md](./profiling.md) | Evidence-based performance optimization | Only after profile evidence shows a bottleneck |

## Pre-Development Checklist

- [ ] Changing math/loss/reward/objective → read
      [math-formula-mapping.md](./math-formula-mapping.md),
      [tensor-shapes-typing.md](./tensor-shapes-typing.md),
      [validation-assertions.md](./validation-assertions.md); add numerics rules when
      touching log-prob, entropy, advantage, clip, mask, or NaN risk.
- [ ] New cross-module objects use dataclass/NamedTuple schemas, not naked dicts
      ([data-schema.md](./data-schema.md)).
- [ ] Compound checks live in `validate.py` / explicit helpers; failures stop the run
      ([validation-assertions.md](./validation-assertions.md)).
- [ ] Numerical primitives live in `numerics.py`; do not silently mask NaN/Inf
      ([numerics.md](./numerics.md)).
- [ ] Entrypoints set seeds via the determinism contract
      ([determinism.md](./determinism.md)).
- [ ] Optimize only with profile evidence ([profiling.md](./profiling.md),
      [code-style.md](./code-style.md)).
- [ ] Plan task-scoped tests for formula behavior, shapes, and numerical edges.

## Quality Check

- [ ] Formula implementations map back to paper/note equation identifiers.
- [ ] Tensor shapes and data-flow assumptions are inspectable by a human reviewer.
- [ ] No naked dicts across internal module boundaries for research data.
- [ ] Numerical edge cases have tests or explicit validation; failed unstable runs
      are preserved, not deleted.
- [ ] Randomness/seeds are recorded for formal comparisons.
- [ ] Performance changes are justified by profile evidence, not taste.
