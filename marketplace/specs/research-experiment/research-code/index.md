# Research Code Index

This layer defines the research code contract: clear implementation, reviewable math, traceable tensor shapes, numerical stability, explicit data schemas, and reproducible randomness.

## Documentation Files

| File | Purpose | When to Read | Priority |
|---|---|---|---|
| [code-style.md](./code-style.md) | Simple, readable, direct research code | Writing or refactoring core implementation | Must Read |
| [math-formula-mapping.md](./math-formula-mapping.md) | Formula-to-code alignment | Translating papers, changing loss/reward/objectives | Must Read |
| [tensor-shapes-typing.md](./tensor-shapes-typing.md) | Tensor shape, dtype, and data-flow annotations | Adding models, rollout batches, losses, metrics, or adapters | Must Read |
| [validation-assertions.md](./validation-assertions.md) | Assertions and invariant validation | Adding preconditions, schemas, or boundary checks | Must Read |
| [numerics.md](./numerics.md) | Safe numerical primitives and NaN/Inf handling | Implementing log-prob, entropy, advantage normalization, or debugging instability | Must Read |
| [data-schema.md](./data-schema.md) | Dataclass / NamedTuple contracts for research data | Passing transitions, batches, results, or artifacts across modules | Must Read |
| [determinism.md](./determinism.md) | Global seed and reproducibility control | Adding training entrypoints, baseline comparisons, or concurrent runs | Must Read |
| [profiling.md](./profiling.md) | Evidence-based performance optimization | Only after profile evidence shows a real bottleneck | Conditional |

## Quick Navigation by Task

Changing math, loss, reward, or objective code?

- Read [math-formula-mapping.md](./math-formula-mapping.md), [tensor-shapes-typing.md](./tensor-shapes-typing.md), and [validation-assertions.md](./validation-assertions.md).
- Read [numerics.md](./numerics.md) when the change touches loss functions, log-prob, entropy, advantage normalization, clipping, masking, or NaN/Inf risk.
- Add or update task-scoped tests that check formula behavior, invariants, numerical edge cases, and tensor shapes.

Adding a rollout, transition, batch, or result object?

- Read [data-schema.md](./data-schema.md).
- Read [tensor-shapes-typing.md](./tensor-shapes-typing.md).
- Do not pass naked dicts across module boundaries.

Debugging NaN, Inf, or unstable training?

- Read [numerics.md](./numerics.md).
- Preserve the failed run directory and status.
- Add or update a numerics regression test before retrying.

Adding validation or assertions?

- Read [validation-assertions.md](./validation-assertions.md).
- Put compound checks in `validate.py` or explicit validation helpers.
- Let failures stop the run instead of hiding them behind broad try/catch blocks.

Optimizing performance?

- Read [profiling.md](./profiling.md) and [code-style.md](./code-style.md).
- Optimize only with profile evidence.
- Do not replace readable tensor math with tricks unless tests and comments justify it.

## Core Rules Summary

- Start with the most mathematically direct implementation; optimize only with evidence.
- Formula implementations must map back to paper or note equation identifiers.
- Cross-module research data must use dataclass or NamedTuple schemas, not naked dicts.
- Numerical safety belongs in `numerics.py`; do not silently mask NaN/Inf.
- Tensor shapes and data-flow assumptions must be easy for a human reviewer to inspect.
