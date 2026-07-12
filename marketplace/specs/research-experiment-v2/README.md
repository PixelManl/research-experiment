# Research-Experiment Spec v2

读完本页应能串起系统：**组织 → 意图/配置 → 干净代码 → 有证据的 run**。

## 职责

1. **组织**：`<task-slot>` 对齐 scripts / runs / data / tests；configs 推荐 `task/<slot>.yaml`。  
2. **意图**：`docs/main` 要什么；`docs/plan` 怎么做；PAPER.md → 1:1；**配置三层**见下。  
3. **链路**：组件组联动（clip + entropy）。  
4. **真源表**：只回答去哪查。  
5. **代码**：algorithm 干净；mc / diag；utils 安全替换 + fail-closed。  
6. **证据**：正式 run 前 git 处理；目录含 commit/patch、Hydra 配置、command、seed。

## 真源表

| 问题 | 看哪里 |
|------|--------|
| 我们要什么？ | `docs/main/` |
| 这次怎么做、论文？ | `docs/plan/` + PAPER.md |
| 超参该跟谁？ | baseline 表 + yaml；[intent/config-baseline.md](./intent/config-baseline.md) |
| 配置入口？ | Hydra；[organize/config-entry.md](./organize/config-entry.md)（**yaml > arg**） |
| 脚本/数据/测试？ | `scripts\|data\|tests/<slot>/` + index |
| 这次跑信什么？ | `runs/<slot>/...` **证据包** + index 的 **当前** |
| 主算法/指标/诊断？ | [code/algorithm-split.md](./code/algorithm-split.md) |
| 改代码还动谁？ | [linkage/coupled-changes.md](./linkage/coupled-changes.md) |
| 下阶段值不值？ | [guides/route-value.md](./guides/route-value.md) |

## 推荐形状

```text
src/<package>/algorithm|metric|diag|utils/
src/<package>/config/args.py   # arg 独立；default 与 yaml 一致
configs/config.yaml
configs/task/<slot>.yaml
configs/debug/smoke.yaml       # 真路径小跑，非 mock
scripts|runs|data|tests/<slot>/
docs/main/  docs/plan/
```

## 设计哲学（短）

见 [code/philosophy.md](./code/philosophy.md)。  
文件>聊天；意图>实现；组织>重审计；联动>单点；algorithm 干净；**正确>可检查>可复现>快**。

## Spec 层

- [organize/](./organize/index.md) — slot、证据、Hydra、tests  
- [intent/](./intent/index.md) — main/plan/paper/baseline  
- [linkage/](./linkage/index.md) — 组件联动  
- [code/](./code/index.md) — 分层与 fail-closed  
- [guides/](./guides/index.md) — before/after/route-value  
- [examples/](./examples/index.md) — 参考非合同  

## Agent 禁令

- 无证据标当前；按日期猜最新。  
- 静默 ori 默认盖 paper/yaml。  
- argparse 默认与 yaml 不一致；arg 埋进 algorithm。  
- mock 测试冒充 smoke。  
- algorithm 堆 metric/diag/满地 eps。  
- 做完阶段就当路线有价值（先看 route-value）。

## 使用

复制本目录到 `.trellis/spec/` 后按仓库改编。Specs are meant to be customized.
