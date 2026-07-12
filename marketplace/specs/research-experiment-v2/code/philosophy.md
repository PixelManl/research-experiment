# 设计哲学（精简清单）

可读完一页。细节在对应层展开。

## 你提出的代码哲学（核心）

1. **algorithm 保持干净** — 只实现主算法；额外内容不进主干。
2. **统计归 metric** — algorithm 出中间产物；`mc.xx` / `metric.xx` 做统计。
3. **诊断归 diag** — 与 metric 同构；`diag.xx` 吃输入做诊断，不堆进核心算法。
4. **风险算子归 utils** — 除法/log/归一化等用安全实现 **替换** 裸算子，不阻塞、不糊墙在 algorithm 正文。

详见 [algorithm-split.md](./algorithm-split.md)。

## 从 v1 仍值得保留的哲学

| 哲学 | 含义 | 落点 |
|------|------|------|
| 文件大于聊天 | 结论、废弃、当前 run、设定写进文件 | organize / intent / README 真源表 |
| 意图先于实现 | main/plan（含 paper 原文）再写码；不抄 ori 默认 | intent |
| 组织先于重审计 | 先 slot + index，不强制重型 CI | organize |
| 联动先于单点聪明 | 组件组一起改（clip+entropy） | linkage |
| 正确 > 可检查 > 可复现 > 快 | 不为炫技牺牲可读 | code（本页） |
| 简单直写公式 | 优先直观 torch；技巧需 profile+测试 | code |
| 脚本只编排 | script 不写 reward/训练内核/metric 公式 | code + organize |
| runs ≠ data | 证据 vs 整理后的可复用数据；软链与废弃链 | organize |
| paper > ori 默认 | 超参与模块行为以 plan/PAPER 为准 | intent |

## 刻意不再堆进 v2 的（避免再次复杂）

- **不**恢复：双轴 claim-ready 状态机、T1/T2/T3 **长文**、heavy-model 外审包、全量 Hydra **百科专章**。  
- **仍保留（短）**：`guides/before-work.md` 的 T1/T2/T3 短表；`guides/after-change.md` 的 observation→claim 短表。  
- **仍强制**：正式入口用 **Hydra**（见 organize/config-entry）——「不堆专章」≠「不要 Hydra」。  
需要更长 v1 原文时查 git 历史，不灌回默认心智。

## 决策口诀

```text
这段是主算法吗？     → algorithm
是要记的数吗？       → metric (mc.xx)
是要查的健康/探针吗？ → diag (diag.xx)
是数值安全/通用小工具？ → utils 替换 + fail-closed
是某次跑的证据吗？   → runs（证据包）
是提取后的可复用材料？ → data（链到 run）
是我们要什么/怎么做？ → docs/main · docs/plan
配置默认从哪来？     → yaml（Hydra）；arg 仅显式覆盖
开跑要不要重读 plan？ → 否；只核 baseline 短表
测试 mock 还是 smoke？ → unit 可 mock；smoke 真路径
```
