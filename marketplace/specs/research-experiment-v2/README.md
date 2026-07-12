# Research-Experiment Spec v2

本模板做 **组织 / 意图 / 链路 / 真源表**，外加一条 **代码分层** 哲学。读完本页应能串起整个系统。

## 四条职责 + 代码分层

1. **组织**：一切按 `<task-slot>` 收纳；`scripts` / `runs` / `data` 同槽，各级有短 `index.md`。
2. **意图**：`docs/main` = 我们要什么；`docs/plan` = 这次怎么做（含论文原文 md 与抽取）；实现 **1:1 对照 plan**。
3. **链路**：改一个组件要想联动（如 hard-clip 与 `dist.entropy()`）；有搜索/MCP 就用，没有就手列依赖。
4. **真源表**：只回答「去哪查」，不再发明多层互相抢戏的「真源口号」。
5. **代码分层**：**algorithm 干净**；统计 `metric`/`mc.xx`；诊断 `diag.xx`；零梯度风险算子从 **utils 替换**接入。

| 问题 | 看哪里 |
|------|--------|
| 我们要什么？ | `docs/main/` |
| 这次怎么做、论文怎么落？ | `docs/plan/`（含 paper 原文 md） |
| 脚本在哪？ | `scripts/<task-slot>/` + `index.md` |
| 可复用、整理后的数据？ | `data/<task-slot>/` + `index.md`（**不是** runs） |
| 某次实验产出、当前算数的 run？ | `runs/<task-slot>/` + `index.md`（**不是** data） |
| 主算法 / 指标 / 诊断 / 安全算子？ | [code/algorithm-split.md](./code/algorithm-split.md) |
| 改代码还要动谁？ | plan 里的组件表 + [linkage/coupled-changes.md](./linkage/coupled-changes.md) |

## 推荐仓库形状

```text
src/<package>/
  algorithm/               # 主算法（干净）
  metric/                  # 统计 → mc.xx
  diag/                    # 诊断 → diag.xx
  utils/                   # 安全除法/log 等，替换式调用
scripts/<task-slot>/
  index.md
  ...                      # 可按日期分子目录，见 organize
runs/<task-slot>/
  index.md                 # 必须标：当前 / 废弃
  <YYYY-MM-DD>/...
data/<task-slot>/
  index.md                 # 必须写：来自哪个 run；废弃标记
  ...
docs/
  main/                    # 给定目标与总标定
  plan/                    # 任务设计；论文原文 .md；实现清单
```

**runs ≠ data（硬约束）**

- `data`：提取、整理后的**可复用事实/中间产物**（真实发现、处理好的集）。
- `runs`：某次计算的**过程与证据**（日志、ckpt、当次 dump）。
- data 必须 **软关联** 到产生它的 run；run 的结论作废时，依赖该 run 的 data 要 **删除或标废弃**，并沿 A→B→C→D 链路处理下游。

## 设计哲学（短）

全文清单见 [code/philosophy.md](./code/philosophy.md)。摘要：

1. **文件大于聊天**；**意图先于实现**（main/plan/paper，不抄 ori）。
2. **组织先于审计**；**联动先于单点聪明**。
3. **algorithm 干净**；**mc / diag 外置**；**utils 安全算子替换**裸风险计算。
4. **正确 > 可检查 > 可复现 > 快**；脚本只编排，不写内核公式。

## Spec 层（安装后）

- [organize/](./organize/index.md) — task-slot、scripts/runs/data、跨天怎么放
- [intent/](./intent/index.md) — main/plan、paper 原文进模块、1:1 实现
- [linkage/](./linkage/index.md) — 组件联动
- [code/](./code/index.md) — algorithm / metric / diag / utils + 哲学清单
- [guides/](./guides/index.md) — 开干前 / 改完后
- [examples/](./examples/index.md) — **参考示例**（非合同）；照抄前先读 index

## Agent 禁令（短）

- 禁止把 runs 里的原始 dump 当成 data 真源长期引用。
- 禁止只按日期「最新」当正确结果；只看 `runs/<slot>/index.md` 的 **当前**。
- 禁止跳过 plan 直接按 ori 源码定超参/模块行为。
- 禁止改 clip/reward/mask 等却不查同组件链路。
- 禁止在仓库根目录堆一次性脚本。
- 禁止在 algorithm 里堆 metric/diag/满地 `+eps`；统计走 mc，诊断走 diag，安全算子走 utils。

## 使用

复制本目录到目标项目的 `.trellis/spec/`，按真实仓库改路径与例子。  
Specs are meant to be customized.
