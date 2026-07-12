# 配置基线：paper / ori / 将跑配置

## 一句话

**paper（及协商 we use）优先于 ori；意图超参只维护一张权威表并落到 yaml；开跑只核短表，不重读整本 plan。**

## 三层语义

| 层 | 回答 | 放哪 |
|----|------|------|
| ① 意图 | 应该用什么 | **一张**超参权威表 + PAPER.md（模块行为） |
| ② 项目配置 | 仓库里怎么写 | `configs/` Hydra yaml（见 [../organize/config-entry.md](../organize/config-entry.md)） |
| ③ 当次证据 | 这次机器跑了什么 | run 目录 `.hydra/config.yaml` |

改超参看 **intent（本页）**；改入口/Hydra 结构看 **organize/config-entry**。

## 权威表只写一处（防双写漂移）

| 角色 | 规则 |
|------|------|
| **权威意图表** | 二选一，项目内固定：**要么** `docs/plan/<slot>.md` 的「Paper 抽取 / 超参」表，**要么** `configs/baseline.md`——**不要两处各写一套 we use** |
| **落地** | `we use` **必须**进入 Hydra yaml；冲突时以 **yaml 实际值** 为准开跑，并回头修权威表 |
| **镜像** | 若需要第二份展示，必须注明「镜像自 xxx，勿手改」 |

表头统一（与 paper 抽取一致）：

```markdown
| key | paper | ori | we use | why |
|-----|-------|-----|--------|-----|
| clip.eps | 0.2 | 0.1 | 0.2 | 跟 paper |
| entropy | on | off | on | 跟 paper |
```

- 跟 ori 不跟 paper → 必填 why，且 **T2（人知悉）**。  
- 禁止 Agent 打开 ori 抄 default 盖 yaml。

## 跑前检查（轻量）

**不要**每次开跑通读整本 plan。只做：

```text
1. 打开【唯一】权威超参表
2. 对照本次 Hydra 将加载的 task/experiment 关键键（或 .hydra 将写出的合成结果）
3. 有意偏差 → command override 或 plan「本次偏差」一句
4. 启动
```

写代码 / 改设定时再读 plan **实现清单**；开跑门禁 ≠ 设计评审。

## 与 paper-to-plan

- 模块行为、公式、实现清单： [paper-to-plan.md](./paper-to-plan.md)。  
- 超参开关：本页权威表 → yaml；公式↔代码列在 plan，不替代本表。

## Agent 禁令

- 禁止 plan 与 baseline.md 两套 we use 并行手改。  
- 禁止静默 ori 默认。  
- 禁止要求「每次 run 全文 review plan」。  
- 禁止无权威表就开正式对比实验。
