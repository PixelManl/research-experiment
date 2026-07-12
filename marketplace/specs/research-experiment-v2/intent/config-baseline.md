# 配置基线：paper / ori / 将跑配置

## 一句话

**paper（及协商 baseline）优先于 ori 源码默认；正式跑前确认将跑配置，而不是把整本 plan 再通读一遍。**

## 三层语义（不要扩成五个「真源」）

| 层 | 回答 | 放哪 |
|----|------|------|
| ① 意图 | 应该用什么 | `docs/plan` 抽取表 + 本页 baseline 表 + PAPER.md |
| ② 项目配置 | 仓库里怎么写 | `configs/`（Hydra，见 [../organize/config-entry.md](../organize/config-entry.md)） |
| ③ 当次证据 | 这次机器跑了什么 | run 目录 `.hydra/config.yaml`（configs/代码进 git 时仍以当次合成为准） |

## baseline 表（短，可放 `configs/baseline.md` 或 plan）

```markdown
| key | paper | ori | we use | why |
|-----|-------|-----|--------|-----|
| clip.eps | 0.2 | 0.1 | 0.2 | 跟 paper |
| entropy | on | off | on | 跟 paper |
```

- **we use** 必须落到 yaml。  
- 跟 ori 不跟 paper → 必须写 why，且算 **T2（人知悉）**。  
- 禁止 Agent 打开 ori 抄 default 覆盖 yaml。

## 跑前检查（轻量，不重读整本 plan）

plan 可以很长。**不要**要求每次开跑把 plan 全文再检查一遍。

只做：

```text
1. 打开 baseline 表（或 plan 里「Paper 抽取 / 超参」那一张表）
2. 对照本次 Hydra 将加载的 task/experiment 组关键键
3. 有意偏差 → 在 command overrides 或 plan 一节「本次偏差」写一句
4. 启动
```

写代码 / 改设定时再读 plan 实现清单；**开跑门禁 ≠ 设计评审**。

## 与 paper-to-plan

- 模块行为、公式：仍走 [paper-to-plan.md](./paper-to-plan.md) 与 PAPER.md。  
- 超参开关：以本页表 + yaml 为准。  
- 实现 1:1 对照 plan；**跑前**只核对表与 yaml，不重复审计整篇叙述。

## Agent 禁令

- 禁止静默使用 ori 默认导致与 paper 冲突。  
- 禁止要求「每次 run 全文 review plan」。  
- 禁止无 baseline/抽取表就开正式对比实验。
