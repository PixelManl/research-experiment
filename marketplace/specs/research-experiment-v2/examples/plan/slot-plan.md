# 示例：docs/plan/ppo-baseline.md

```markdown
# Plan — ppo-baseline

## 对齐 main

- main 目标：用论文 A 的 surrogate 设定做可复现基线。

## Paper 原文

- 模块 policy-surrogate：`docs/plan/modules/policy-surrogate/PAPER.md`（§3.2 摘录）

## Paper 抽取（本 slot 唯一超参权威表；勿再写 baseline.md 第二套）

| key | paper | ori | we use | why |
|-----|-------|-----|--------|-----|
| clip.eps | 0.2 | 0.1 | 0.2 | 跟 paper |
| entropy | on | off | on | 与 clip 同组 |

## 公式 ↔ 代码

| Eq/节 | 代码 path:fn | 测试 |
|-------|--------------|------|
| §3.2 clip | src/pkg/algorithm/clip.py:ratio_clip | tests/ppo-baseline/test_clip.py |

## 实现清单

- [ ] clip 与 PAPER §3.2 一致
- [ ] entropy 与同组联动
- [ ] tests/<slot>/test_surrogate.py 最小用例

## 组件组

见 examples/linkage/COMPONENTS.md 形状
```

