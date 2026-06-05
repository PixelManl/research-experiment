# Numerical Stability Contract

Numerical bugs often make training “look like it is learning” while ruining the result. Safe numerical primitives must be centralized.

## Purpose

This contract prevents silent numerical failures from contaminating training, metrics, and claims. Numerical safety should be explicit, tested, and reusable instead of hidden inside ad hoc training code.

## When to Read

Read this before:

- implementing log-prob, entropy, KL, advantage normalization, clipping, masking, or loss code;
- changing reward, objective, or gradient-carrying tensor operations;
- debugging NaN, Inf, exploding/vanishing values, or unstable training;
- adding safe tensor primitives that may be reused across task-slots.

## Required module

```text
src/<package>/numerics.py
```

## Required safe primitives

Add as needed:

```python
def safe_log_softmax(logits: Tensor, dim: int = -1) -> Tensor: ...
def safe_entropy_from_logits(logits: Tensor, dim: int = -1) -> Tensor: ...
def masked_mean(x: Tensor, mask: Tensor, eps: float = 1e-8) -> Tensor: ...
def normalize_advantage(adv: Tensor, mask: Tensor | None = None, eps: float = 1e-8) -> Tensor: ...
def finite_or_raise(x: Tensor, name: str) -> None: ...
```

## Required replacements

Use:

```python
F.log_softmax(logits, dim=-1)
```

Not:

```python
torch.log(torch.softmax(logits, dim=-1))
```

Use:

```python
std = adv.std(unbiased=False)
adv = (adv - adv.mean()) / std.clamp_min(eps)
```

Not:

```python
adv = (adv - adv.mean()) / adv.std()
```

## In-place operation rule

In-place ops in gradient-carrying code are forbidden unless justified.

Allowed only when:

- tensor does not require grad, or the operation is inside a clearly documented no-grad block;
- a test covers gradient behavior;
- a comment explains the reason.

## Required tests

For each safe primitive:

```text
tests/common/test_numerics.py
# or
tests/<task-slot>/test_numerics.py
```

Check:

- zero variance;
- empty or all-false mask;
- large logits;
- NaN/Inf rejection;
- gradient sanity when relevant.

## Diagnostic requirement

If NaN/Inf appears:

1. stop the run;
2. write failure status;
3. preserve run directory;
4. add or update a numerics test before retrying.

## Forbidden

- using `torch.nan_to_num` or similar to implicitly hide NaNs without fixing the root cause.

## Related Specs

- [math-formula-mapping.md](./math-formula-mapping.md)
- [tensor-shapes-typing.md](./tensor-shapes-typing.md)
- [validation-assertions.md](./validation-assertions.md)
- [determinism.md](./determinism.md)
- [../experiment-runtime/provenance.md](../experiment-runtime/provenance.md)
