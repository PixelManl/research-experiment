# Profiling and Optimization Contract

Do not optimize prematurely. Start with readable code, then profile if needed.

## When to Read

Read this before:

- optimizing runtime, memory, tensor allocation, or IO;
- replacing readable code with clever or fused implementations;
- approving performance work after correctness is established;
- deciding whether a slowdown is worth changing scientific code.

## Optimization trigger

Only optimize when one of these is true:

- smoke/full run shows unacceptable runtime;
- `cProfile`, PyTorch profiler, or timing logs identify a bottleneck;
- memory profiling shows an actual allocation problem;
- human explicitly approves optimization work.

## Required before optimization

Record in task ledger:

```markdown
## Optimization trigger

Observed bottleneck:
Profiler command:
Evidence:
Candidate change:
Risk to math/readability:
```

## Reference implementation

If using a clever optimized implementation, keep a simple reference implementation in tests:

```python
def reference_compute_advantage(...):
    ...
```

Then compare optimized vs reference on tiny tensors.

## Forbidden by default

- replacing readable torch ops with sign/ReLU tricks;
- in-place ops in gradient paths;
- manual fusion that hides formula meaning;
- optimizing before correctness tests exist.

## Acceptable early performance practice

- use built-in vectorized torch functions;
- avoid obvious Python loops over large tensors when a direct torch expression is clear;
- batch IO sensibly;
- keep debug logs off in full runs.
