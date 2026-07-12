# Code Index

## Guidelines Index

| Guide | Description | When to Read |
|-------|-------------|--------------|
| [algorithm-split.md](./algorithm-split.md) | algorithm / mc / diag / utils；门控；fail-closed | 写算法与指标时 |
| [philosophy.md](./philosophy.md) | 设计哲学清单 | 争论「这段放哪」 |

## Pre-Development Checklist

- [ ] 分层：algorithm vs metric vs diag vs utils。  
- [ ] 风险算子走 utils；NaN 走 fail-closed。  
- [ ] 联动见 linkage。

## Quality Check

- [ ] algorithm 无大段 metric/diag。  
- [ ] metric/diag 无 run IO 入口。  
- [ ] 无未记录的 nan 遮掩。
