# Hydra 配置片段参考

> 参考非合同。复制到项目 `configs/` 后按包名/slot 改写。  
> 铁律：**yaml > arg**；正式入口 Hydra；smoke = 真路径。

## `configs/config.yaml`（入口示意）

```yaml
# defaults 指向各组；真实默认值只写在 yaml 里
defaults:
  - task: ppo-baseline      # → configs/task/ppo-baseline.yaml
  - experiment: default
  - debug: off
  - hydra: default
  - _self_

run:
  name: default
  seed: 0

# 业务字段由 task / experiment 组展开
```

## `configs/task/<task-slot>.yaml`

```yaml
# configs/task/ppo-baseline.yaml
task:
  slot: ppo-baseline

# 与 plan 权威表 we use 一致的超参写在这里（示例）
# algorithm:
#   clip_eps: 0.2
```

## `configs/hydra/default.yaml`（输出到 runs/）

```yaml
# 合成配置与当次文件落在 runs/<slot>/日期/时间-名/
hydra:
  run:
    dir: runs/${task.slot}/${now:%Y-%m-%d}/${now:%H%M%S}-${run.name}
  job:
    chdir: false
```

跑完后该目录应有 `.hydra/config.yaml`（当次配置证据）。  
其它最少集见 [../runs/run-dir-layout.md](../runs/run-dir-layout.md)。

## `configs/debug/smoke.yaml`

```yaml
# 真路径极小规模；不是 unit test mock
debug:
  enabled: true
  mode: smoke
  max_steps: 2   # 项目自定

run:
  name: smoke
```

用法示意：`python scripts/<slot>/run.py debug=smoke`

## `configs/debug/dry_run.yaml`

```yaml
debug:
  enabled: true
  mode: dry_run

run:
  name: dry-run
```

只验配置/路径/入口，可不跑满训练。

## `configs/debug/off.yaml`

```yaml
debug:
  enabled: false
  mode: off
```

## 可选：`configs/baseline.md`（超参权威表）

若权威表不放 plan、放这里——**与 plan 二选一**，禁止两套 we use：

```markdown
| key | paper | ori | we use | why |
|-----|-------|-----|--------|-----|
| clip.eps | 0.2 | 0.1 | 0.2 | 跟 paper |
```

`we use` 必须与对应 yaml 一致。

## arg / CLI

- 不要在 `algorithm/` 里堆 argparse 默认值。  
- 可选 `src/<package>/config/cli.py`：**只**处理显式覆盖；数字 default **从 yaml/OmegaConf 读**，勿手写第二套。
