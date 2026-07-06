# Hydra Configuration Contract

**WARNING**: Configuration drift is a SILENT RESEARCH KILLER. Read [config-source-of-truth.md](./config-source-of-truth.md) FIRST.

Hydra is the experiment control plane. Do not grow a 60-argument `argparse` interface.

## When to Read

Read this before:

- adding or changing config groups, runtime parameters, or debug modes;
- creating a formal experiment entrypoint;
- adapting legacy argparse interfaces;
- deciding whether a run should be controlled by config or command-line flags.

## CRITICAL: Config Source of Truth

**BEFORE** reading anything else, read [config-source-of-truth.md](./config-source-of-truth.md).

The most common failure mode in research experiments is **CONFIG DRIFT**:
- Paper says: "only actor enabled"
- Original code: "critic + actor enabled"
- Agent runs: "critic + actor enabled" (copying code, not paper)
- Result: WRONG baseline comparison, ALL downstream results INVALIDATED

**SOLUTION**: YAML 就是 truth 的表征，直接读取 yaml 就可以验证配置。
1. `configs/truth/config.yaml` - 默认配置副本（真源，一般不修改）
2. `configs/truth/config_truth.md` - 配置内容说明文档（用于协商核对参数）

**GOLDEN RULE**: IF config doesn't match `configs/truth/config.yaml` AND human hasn't explicitly approved the change THEN DON'T RUN THE EXPERIMENT.

## Required config shape

```text
configs/
├── config.yaml              # 主配置文件（头顶必须说明真源位置）
├── schema.py
├── task/
│   └── <task-slot>.yaml
├── experiment/
│   └── default.yaml
├── debug/
│   ├── off.yaml
│   ├── dry_run.yaml
│   └── smoke.yaml
├── hydra/
│   └── default.yaml
└── truth/
    ├── config.yaml          # 默认配置副本（真源，一般不修改）
    └── config_truth.md      # 配置内容说明文档
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

This `run(cfg)` belongs to the script entrypoint layer. Do not implement it as `src/<package>/process.py::run`; `process.py` is for reusable data preprocessing and composite metrics/diagnostics/status helpers.

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
