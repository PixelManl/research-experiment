# Code Index

核心代码怎么拆：algorithm 保持干净；metric / diag / utils 各司其职。

## Guidelines Index

| Guide | Description | When to Read |
|-------|-------------|--------------|
| [algorithm-split.md](./algorithm-split.md) | algorithm / metric / diag / utils 边界与调用方式 | 写/改算法、指标、诊断、数值安全时 |
| [philosophy.md](./philosophy.md) | 设计哲学（含 v1 压后保留） | 开项目或争论「这段该放哪」时 |

## Pre-Development Checklist

- [ ] 本次改动落在哪一层：algorithm / metric / diag / utils / scripts？
- [ ] algorithm 是否只产**中间产物**，统计走 `mc.xx`，诊断走 `diag.xx`？
- [ ] 有除法、log、归一化等零梯度/NaN 风险时，是否从 **utils 安全算子**替换，而不是在 algorithm 里堆 eps 糊墙？
- [ ] 若动算法语义：已看 [../linkage/coupled-changes.md](../linkage/coupled-changes.md)。

## Quality Check

- [ ] algorithm 中无大块 metric 公式、无大块诊断探针、无 ad-hoc 安全除法复制粘贴。
- [ ] metric/diag 只消费中间产物（或明确输入），不反向塞进训练主循环细节。
- [ ] 风险算子有 utils 统一实现，algorithm 侧是替换调用。
