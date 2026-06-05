# Hydra Configuration Contract

Hydra is the experiment control plane. Do not grow a 60-argument `argparse` interface.

## When to Read

Read this before:

- adding or changing config groups, runtime parameters, or debug modes;
- creating a formal experiment entrypoint;
- adapting legacy argparse interfaces;
- deciding whether a run should be controlled by config or command-line flags.

## Required config shape

```text
configs/
├── config.yaml
├── schema.py
├── task/
│   └── <task-slot>.yaml
├── experiment/
│   └── default.yaml
├── debug/
│   ├── off.yaml
│   ├── dry_run.yaml
│   └── smoke.yaml
└── hydra/
    └── default.yaml
```

## Canonical `configs/config.yaml`

```yaml
defaults:
  - task: ppo-handwritten
  - experiment: default
  - debug: off
  - _self_

task:
  slot: ppo-handwritten

run:
  name: default
  seed: 0
```

## Output directory

Configure Hydra run directory:

```yaml
hydra:
  run:
    dir: outputs/${task.slot}/${now:%Y-%m-%d}/${now:%H%M%S}-${run.name}
  job:
    chdir: false
```

## Strict configuration

Required:

- Use `configs/schema.py` with dataclasses / structured configs for runtime and type checking.
- Unknown config keys must fail fast.
- Adding new command-line keys with `+foo=bar` is forbidden for normal experiments.
- Temporary open config edits must be localized and documented.

Recommended entrypoint pattern:

```python
@hydra.main(version_base=None, config_path="../../configs", config_name="config")
def main(cfg: DictConfig) -> None:
    OmegaConf.set_struct(cfg, True)
    run(cfg)
```

When the project has a robust structured config, type `cfg` as the dataclass root instead of generic `DictConfig`.

## Legacy argparse compatibility

Allowed only at the boundary:

```text
scripts/common/legacy_args.py
```

It may convert old arguments into Hydra overrides, then call the Hydra entrypoint. Do not keep adding parameters to old argparse code.

## Debug config group

`configs/debug/smoke.yaml` must define a fast path:

```yaml
debug:
  mode: smoke
  max_steps: 2
  batch_size: 2
  num_envs: 1
  diagnostics: true
  log_level: DEBUG
run:
  name: smoke
```

`configs/debug/dry_run.yaml` must bypass computation completely:

```yaml
debug:
  mode: dry_run
  # Used to test config parsing and data paths only
```

## Forbidden

```python
# Wrong
parser.add_argument("--lambda1", type=float)
parser.add_argument("--lambda2", type=float)
...
parser.add_argument("--lambda60", type=float)
```

```bash
# Wrong for formal run
python scripts/ppo/run.py --lr 0.0003 --gamma 0.99 --clip 0.2 --seed 3 ...
```

Use:

```bash
python scripts/ppo-handwritten/run.py task=ppo-handwritten experiment=paper_v1 run.seed=3
```
