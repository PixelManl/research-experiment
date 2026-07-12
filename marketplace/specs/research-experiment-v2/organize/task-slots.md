# Task-Slot 与目录组织

## 规则一句话

**同一个研究工作流 = 同一个 `<task-slot>`**；scripts / runs / data / tests（及推荐 configs/task）同名对齐；重点靠短 `index.md`。

## Slot 命名

- 稳定短名：`ppo-baseline`、`data-clean-v1`。  
- **不要**把日期写进 slot 名。  
- 日期放在 slot **内部**。

## 目录

```text
scripts/<task-slot>/
runs/<task-slot>/          # 某次计算的过程与证据（见 run-evidence.md）
data/<task-slot>/          # 提取整理后的可复用数据（≠ runs）
tests/<task-slot>/         # 见 tests.md
configs/task/<task-slot>.yaml   # 推荐：配置也按 slot 拆
```

### runs ≠ data

| | data | runs |
|--|------|------|
| 是什么 | 整理后的可复用事实 | 单次实验产出与证据 |
| 例子 | 清洗表、特征缓存 | log、ckpt、`.hydra/`、metrics |
| 错误 | 把整次 run 当 data | 唯一干净集只扔在 runs 从不提炼 |

**会进下次训练的整理材料 → data；这次机器算了什么 → runs。**

### data 软链 run + 废弃链

`data/<slot>/index.md`：

```markdown
| data | 来自 run | 状态 | 备注 |
|------|----------|------|------|
| tables/x.parquet | 2026-07-02/091412-fixed | 当前 | |
```

- run 废弃 → 依赖它的 data 删或标废弃。  
- 链路 A→B→C→D 中 B 错 → B 及下游皆废。

### 「当前」= 证据齐全（与 run-evidence 一致）

- 每 slot 至多一个 **当前**。  
- 可引用 = 当前 + [run-evidence.md](./run-evidence.md) 最少集。  
- 废弃须写 **原因**（归因）。  
- 禁止按日期猜最新。

```markdown
| 状态 | 路径 | 原因 |
|------|------|------|
| **当前** | 2026-07-02/091412-fixed | 证据齐 |
| 废弃 | 2026-07-01/103000-bug | clip 错；勿引用 |
```

## 跨天

Slot 不变；`runs|scripts/.../<YYYY-MM-DD>/`；slot 级 index 汇总当前/废弃。

## index 写什么

- scripts：入口  
- runs：当前 + 废弃（含原因）  
- data：路径、源 run、状态  
- tests：见 tests.md  

## Agent

- 新脚本/run/data/tests → 进对应 slot 并更新 index。  
- 标当前前检查证据包。
