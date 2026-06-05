# Global Determinism Contract

Every formal run must state how randomness is controlled.

## When to Read

Read this before:

- adding training, evaluation, data-loading, or rollout entrypoints;
- launching sweeps, remote runs, or concurrent jobs;
- comparing baselines or claiming reproducibility;
- changing worker, environment, DataLoader, or multiprocessing seed behavior.

## Required config

```yaml
run:
  seed: 0
determinism:
  enabled: true
  torch_deterministic_algorithms: false
  cudnn_benchmark: false
  warn_only: true
```

## Required setup function

```text
src/<package>/determinism.py
```

Minimum behavior:

```python
def set_global_seed(seed: int, deterministic: bool) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
```

If deterministic algorithms are enabled, record that in `provenance.json` (see `../experiment-runtime/provenance.md`).

## Worker seeds

For DataLoader, vectorized envs, or multiprocessing, document the seed derivation:

```text
worker_seed = run.seed + 1000 * rank + worker_id
env_seed = run.seed + env_id
```

## Required logging

At run start, log:

- global seed;
- worker/env seed policy;
- deterministic flags;
- device;
- any nondeterministic known operations.

## Test requirement

For smoke mode, if deterministic mode is enabled, two runs with the same seed should match a small deterministic metric or trajectory hash.

## Forbidden

- Random seed hidden in script code.
- Changing seed after some modules have already initialized.
- Running sweeps where seed is implicit.
- Claiming reproducibility without recording seed and code diff.
