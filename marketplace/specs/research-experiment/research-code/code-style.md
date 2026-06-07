# Research Code Style Contract

Research code priorities:

1. correct;
2. inspectable;
3. reproducible;
4. reasonably fast;
5. only then optimized.

## When to Read

Read this before:

- writing or refactoring core research code;
- deciding whether to split or keep logic inline;
- adding clever tensor tricks, in-place operations, or performance shortcuts;
- reviewing whether a task script has become glue-heavy.

## Simple does not mean sloppy

Use clear torch primitives and direct logic.

Good:

```python
log_probs = F.log_softmax(logits, dim=-1)
chosen = log_probs.gather(dim=-1, index=actions.unsqueeze(-1)).squeeze(-1)
```

Bad:

```python
# Hard to audit: math trick to avoid a temporary tensor
chosen = ((actions == torch.arange(n)).float() * logits).sum(-1) - torch.log(torch.exp(logits).sum(-1))
```

## Optimization rule

Do not introduce math tricks, in-place operations, fused custom kernels, or clever broadcasting for performance unless:

- a profile shows the bottleneck;
- a test proves numerical equivalence;
- the code comment explains why the optimized version is safe;
- the simple reference implementation remains in a test or comment.

## Function extraction rule

Extract functions when it clarifies a concept or contract. Do not over-extract early.

Good extraction:

- `compute_gae(...)`
- `normalize_advantage(...)`
- `validate_rollout_batch(...)`

Bad extraction:

- `_do_part1(...)`
- `_helper2(...)`
- tiny wrappers that hide the math.

## Main flow

`main` and task scripts must read like a short story:

```python
setup_run()
set_global_seed(cfg.run.seed, cfg.determinism.enabled)
validate_config()
raw_result = run_experiment(cfg)
processed = process.summarize_lifecycle_result(raw_result, cfg)
write_metrics(processed.metrics)
write_diagnostics(processed.diagnostics)
write_status(processed.status_decision)
```

No metric formulas, plotting details, and ad hoc diagnostics in `main`. `process.py` may be called for named preprocessing or composite result helpers, but it must not be the run entrypoint or output writer.

## Forbidden

- broad `try/except` around scientific computation;
- continuing after invariant failure;
- silent fallback to CPU or different data;
- passing bare `dict`s between modules (use `dataclass`, `NamedTuple`, or `TypedDict`);
- large glue code blocks for one-off outputs;
- old implementation branches left in `if False`.
