# Research-Experiment Spec v2

读完本页应能串起系统：**组织 → 意图/配置 → 干净代码 → 有证据的 run**。

## 职责

1. **组织**：`<task-slot>` 对齐 scripts / runs / data / tests；configs 推荐 `task/<slot>.yaml`。  
2. **意图**：`docs/main` / `docs/plan` / PAPER.md → 1:1；**配置三层**见下表。  
3. **链路**：组件组联动（clip + entropy）。  
4. **真源表**：只回答去哪查。  
5. **代码**：algorithm 干净；mc / diag；utils + fail-closed。  
6. **证据**：跑前 git；**最少集**齐才可标 runs「当前」。

## 配置三层（意图 → yaml → 当次）

| 层 | 回答 | 看哪里 |
|----|------|--------|
| ① 意图 | 应该用什么 | **一张**权威超参表 + PAPER；[intent/config-baseline.md](./intent/config-baseline.md) |
| ② 项目 | 仓库怎么配 | Hydra `configs/`；[organize/config-entry.md](./organize/config-entry.md)（**yaml > arg**） |
| ③ 当次 | 这次跑了什么 | `runs/.../.hydra/config.yaml`；[organize/run-evidence.md](./organize/run-evidence.md) |

改超参 → intent；改入口结构 → organize/config-entry。权威表只维护一处，并落到 yaml。

## 真源表

| 问题 | 看哪里 |
|------|--------|
| 我们要什么？ | `docs/main/` |
| 这次怎么做、论文？ | `docs/plan/` + PAPER.md |
| 脚本 / **runs** / 数据 / 测试？ | `scripts\|runs\|data\|tests/<slot>/` + index |
| 这次 run 信什么？ | 证据**最少集** + runs index 的 **当前**（data 可多条在用） |
| 主算法/指标/诊断？ | [code/algorithm-split.md](./code/algorithm-split.md) |
| 改代码还动谁？ | [linkage/coupled-changes.md](./linkage/coupled-changes.md) |
| 下阶段值不值？ | [guides/route-value.md](./guides/route-value.md) |

## 推荐形状

```text
src/<package>/algorithm|metric|diag|utils/
src/<package>/config/cli.py    # 可选：只解析显式覆盖；default 从 yaml 读，勿手写第二套
configs/config.yaml
configs/task/<slot>.yaml
configs/debug/smoke.yaml
scripts|runs|data|tests/<slot>/
docs/main/  docs/plan/
```

## 设计哲学（短）

见 [code/philosophy.md](./code/philosophy.md)。  
不恢复 v1 长文仪式，但 **guides 里 T1/T2/T3 与 claim 短表仍有效**。  
**必须 Hydra** 做正式入口——「不堆全量 Hydra 专章」≠ 不要 Hydra。

## Spec 层

- [organize/](./organize/index.md) — slot、证据、Hydra、tests  
- [intent/](./intent/index.md) — main/plan/paper/baseline  
- [linkage/](./linkage/index.md) · [code/](./code/index.md) · [guides/](./guides/index.md) · [examples/](./examples/index.md)

## Agent 禁令

- 无最少集标当前；dirty 无 patch；只改 index、run 目录空。  
- 按日期猜最新；废弃不写原因。  
- 把 data 多条在用当成违规（「一个当前」只限 runs）。  
- 静默 ori；yaml/代码两套 default；arg 埋进 algorithm。  
- 非 Hydra + snapshot 冒充正式当前。  
- mock 冒充 smoke；algorithm 堆 metric/diag/eps。  
- 做完阶段就当路线有价值。

## 使用

复制到 `.trellis/spec/` 后按仓库改编。

**落盘骨架**：对照 [examples/scaffold/LAYOUT.md](./examples/scaffold/LAYOUT.md) 建目录；Hydra 片段见 [examples/configs/snippets.md](./examples/configs/snippets.md)。examples 均为参考，非第二套合同。
