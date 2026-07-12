# docs/main 与 docs/plan

## 分工

| | `docs/main/` | `docs/plan/` |
|--|--------------|--------------|
| 是什么 | **给定/标定**：我们想要什么 | **任务书写**：为完成任务怎么做 |
| 典型内容 | 目标、成功标准、总约束、选定「用论文 A 做基线」 | 步骤、论文要点与原文、超参表、实现清单、风险 |
| 谁主导 | 人给的方向（Agent 可整理，不可偷换目标） | 做人/Agent 在推进任务时写 |
| 何时改 | 目标变了才改 | 每个 slot、每个阶段可更新 |

```text
main：我们要 XXX（例如：复现论文 A 的 clip 设定作为基线）
  → plan：写清怎么做 + 贴/链 paper 原文 + 抽取实现表
  → 代码：严格按 plan 实现
  → 若做不到：先改 plan（并必要时改 main），禁止默默偏航
```

## 推荐文件

```text
docs/
  main/
    main.md                 # 总标定；可再拆章节
  plan/
    <task-slot>.md          # 与 slot 对齐的任务 plan
    papers/                 # 可选：全文或章节原文 md
      paper-a-clip.md
    modules/                # 可选：按模块放原文与笔记
      policy-clip/
        PAPER.md            # 该模块必须对照的原文
        notes.md
```

「每一个模块放置 .md 格式的 paper 原文」——见 [paper-to-plan.md](./paper-to-plan.md)。

## 防「想要的 ≠ 最终的」

1. 写码前 plan 里已有可勾选的 **实现清单**。
2. 写码中只许勾清单，不许另起一套未写入的设定。
3. 写码后快速对照：清单每项 ↔ 代码位置；差一项就补 plan 或补代码。

## 配置与 ori

- **采用哪套超参** 写在 plan（来自 paper 原文表），不是「打开 ori 抄 default」。
- ori 仅作实现参考；与 paper/plan 冲突 → 记入 plan，**默认跟 plan/paper**，跟 ori 必须写理由。
