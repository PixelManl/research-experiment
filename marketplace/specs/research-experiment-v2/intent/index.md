# Intent Index

对齐「我们要什么」与「做出什么」：main / plan / paper / 配置基线。

## Guidelines Index

| Guide | Description | When to Read |
|-------|-------------|--------------|
| [main-and-plan.md](./main-and-plan.md) | main vs plan | 开任务、改目标 |
| [paper-to-plan.md](./paper-to-plan.md) | PAPER.md；抽取；1:1；公式↔行 | 按论文做模块时 |
| [config-baseline.md](./config-baseline.md) | paper/ori/将跑配置；轻量跑前门禁 | **改超参、正式跑前** |

## Pre-Development Checklist

- [ ] 读 main：目标仍成立。  
- [ ] 本 slot 有 plan；实现对照清单（改代码时），非每次开跑全文。  
- [ ] 论文模块有 PAPER.md；超参表与 yaml 一致。  
- [ ] 跑前只核 baseline 短表 + Hydra 将加载键。

## Quality Check

- [ ] 无「main 要 A、yaml/ori 实际 B」且未记录。  
- [ ] 跟 ori 不跟 paper 有 why。  
- [ ] 语义变更后旧 baseline 对比已标不可比。
