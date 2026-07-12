# 示例：docs/plan/ppo-baseline.md

```markdown
# Plan — ppo-baseline

## 对齐 main

- main 目标：用论文 A 的 surrogate 设定做可复现基线。

## Paper 原文

- 模块 policy-surrogate：`docs/plan/modules/policy-surrogate/PAPER.md`（§3.2 摘录）

## Paper 抽取

| 项 | Paper | ori | 我们采用 | 备注 |
|----|-------|-----|----------|------|
| clip ε | 0.2 | 0.1 | 0.2 | 跟 paper，不跟 ori |
| entropy bonus | 有 | 无 | 有 | 与 clip 同组件组 |

## 实现清单

- [ ] clip 与 PAPER §3.2 一致
- [ ] entropy 与同组联动
- [ ] tests/<slot>/test_surrogate.py 最小用例

## 组件组

见 `docs/plan/modules/policy-surrogate/COMPONENTS.md`（或 examples/linkage 样例）
```
