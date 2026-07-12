# Task-Slot 与目录组织

## 规则一句话

**同一个研究工作流 = 同一个 `<task-slot>`**；脚本、runs、data 用同名目录对齐；重点靠各级 `index.md` 标注，不靠扫整个磁盘。

## Slot 命名

- 用稳定短名：`ppo-baseline`、`data-clean-v1`。
- **不要**把日期写进 slot 名（跨很多天的任务仍是一个 slot）。
- 日期放在 slot **内部**（见下）。

## 三级目录（强制分清）

```text
scripts/<task-slot>/     # 怎么跑
runs/<task-slot>/        # 某次算了什么（过程与证据）
data/<task-slot>/        # 提取整理后的可复用数据（发现与整理）
```

### runs ≠ data（硬约束）

| | `data/` | `runs/` |
|--|---------|---------|
| 含义 | 提取过的、整理后的、**可复用**输入/中间事实 | 单次（或一组）实验的**产出与证据** |
| 例子 | 清洗表、固定划分、特征缓存、从日志**提炼**的结论表 | raw log、ckpt、当次 metrics dump、当次配置快照 |
| 生命周期 | 可跨多次 run；但必须能追溯来源 run | 可废弃；废弃后不应再当「正确结果」 |
| 错误用法 | 把整次 run 目录软链进来当 data | 把「唯一干净数据集」只丢在 runs 里从不提炼 |

**一句：会进下一次训练/分析的「整理后材料」→ data；记录「这次机器算了什么」→ runs。**

### data 必须软关联到 run

每条 data 在 `data/<slot>/index.md`（或旁路 `SOURCE.md`）写明：

```markdown
| data 路径 | 来自 run | 状态 | 备注 |
|-----------|----------|------|------|
| features/train.parquet | runs/.../2026-07-02/091412-clean | 当前 | 从该 run 的 raw 提取 |
| features/old.parquet | runs/.../2026-07-01/bad-run | 废弃 | 上游 B 错误，见下 |
```

- run 的结论变了 / 被标废弃 → **所有声明来自该 run 的 data 必须删除或标废弃**。
- 链路 **A→B→C→D**（例如 raw run → 提取表 → 再统计 → 作图数据）：若 **B 错了**，则 B 与 **依赖 B 的 C、D** 一律删或标废弃；不要只改代码却留着脏 data 占上下文。
- 这样 runs 与 data 解耦：**runs 可多、可废；data 只保留仍成立的提取结果**，避免 Agent 把 7-01 脏产物当永久真源。

## 跨很多天的任务怎么组织？

**Slot 是顶级身份；时间是 slot 下的分层，不是新 slot。**

推荐：

```text
scripts/ppo-baseline/
  index.md                 # 总入口：重要脚本 + 链接到各日
  run_train.py             # 稳定入口（可选）
  2026-07-01/              # 当日试错脚本（可选）
  2026-07-02/
runs/ppo-baseline/
  index.md                 # 当前 = 7-02 某次；7-01 标废弃
  2026-07-01/103000-bug/
  2026-07-02/091412-fixed/
data/ppo-baseline/
  index.md
  2026-07-02/              # 可选：按提取日归类
    train_table.parquet
```

`runs/<slot>/index.md` 示例：

```markdown
# runs / ppo-baseline

| 状态 | 路径 | 说明 |
|------|------|------|
| **当前** | 2026-07-02/091412-fixed | 修 clip 后重跑，作图与结论只引这个 |
| 废弃 | 2026-07-01/103000-bug | reward/clip 错误；勿引用 |

禁止：按文件夹日期排序猜「最新即正确」。
```

原则：

1. **跨天 = 同一 slot 下多日期子目录** + **slot 级 index 当目录**。
2. 只有科学目标变了（换题、换设定主线）才新开 slot。
3. Agent 打开任务时：先读三个 index，再进具体日期目录。

## index.md 写什么（保持短）

- **scripts**：哪些是正式入口、哪些是一次性。
- **runs**：**当前**一条 + 废弃列表（可多）。
- **data**：路径、来源 run、状态（当前/废弃）。

不要把论文、长日志贴进 index。

## Agent 行为

- 新脚本 → 放进对应 `scripts/<slot>/`，更新 index。
- 新 run → 写在 `runs/<slot>/<日期>/...`，更新 runs index；若取代旧结论，旧条目标废弃。
- 新 data → 仅存放**提取整理后**的结果，写上来源 run；上游作废则清理下游。
