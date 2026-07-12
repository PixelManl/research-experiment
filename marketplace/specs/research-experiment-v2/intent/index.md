# Intent Index

对齐「我们要什么」与「最后做出什么」：`docs/main` + `docs/plan`，论文进 plan，实现 1:1 对照 plan。

## Guidelines Index

| Guide | Description | When to Read |
|-------|-------------|--------------|
| [main-and-plan.md](./main-and-plan.md) | main vs plan 分工与更新时机 | 开任务、改目标、写实现前 |
| [paper-to-plan.md](./paper-to-plan.md) | 模块旁放 paper 原文 md；抽取；1:1 实现 | 采用某篇论文/模块设定时 |

## Pre-Development Checklist

- [ ] 已读 `docs/main/`：目标与约束仍成立。
- [ ] 本 slot 有 `docs/plan/<task-slot>.md`（或等价 plan）；没有则先写再写码。
- [ ] 若依赖论文：plan 目录（或模块子目录）中有 **paper 原文 .md**，不是只靠记忆/ori。
- [ ] 实现清单从 plan 抽取；准备 **对照 plan 写代码**，不对照 ori 默认超参。
- [ ] paper 与 ori 冲突点已写入 plan，并有采用哪一方的说明。

## Quality Check

- [ ] 代码行为能在 plan 中找到对应条目（1:1）。
- [ ] 未出现「main 要 A、代码却是 ori 的 B」且 plan 未记录。
- [ ] 论文相关模块旁仍能找到原文 md 或明确链接。
