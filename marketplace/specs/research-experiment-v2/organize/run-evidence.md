# Run 证据包与 Git 铁律

## 一句话

**正式计算前把主体代码置于可说明的 git 状态；每次 run 目录留下身份卡。没有最少集证据，不得标「当前」，不得写进结论。**

策略：**A-default** — 允许 dirty tree，但必须留下完整 `git.diff.patch`；无 patch 不得标当前。

## 跑前：git 处理

```text
1. git status
2. 与本次实验相关的改动：
   - 优先 git add + commit（message 可短）
   - 若暂不 commit：必须接受 dirty 规则，禁止假装干净
3. 确认 Hydra 入口与将用配置组（见 [config-entry.md](./config-entry.md)、[../intent/config-baseline.md](../intent/config-baseline.md)）
4. 再启动计算
5. 证据写入本次 runs/<slot>/<日期>/<run-name>/
```

| 状态 | 可标「当前」？ | 必须留下 |
|------|----------------|----------|
| 干净 + 已 commit | ✅（且最少集齐） | commit 哈希 + 空 patch 即可 |
| dirty | 仅当有完整 patch | commit + dirty=true + **非空** git.diff.patch |
| 非 git 仓库 | ❌ 正式 run | — |

「完整 patch」：相对该 commit 的 **已跟踪文件** diff（`git diff` / `git diff HEAD`）。未跟踪大文件应 gitignore，勿塞进 patch。

## 配置证据：正式路径 = Hydra

**正式实验必须用 Hydra**（见 [config-entry.md](./config-entry.md)）。配置证据优先为 run 目录内：

```text
.hydra/config.yaml    # 本次合成配置
```

- configs 已进 git **不能替代** 当次合成结果；也 **不能替代** 代码侧 commit/dirty/patch。  
- **不要**再手写一份与 `.hydra` 重复的 `config.snapshot.yaml`（双份易漂）。

### `config.snapshot.yaml` 何时才用？

| 场景 | 是否正式 | 做法 |
|------|----------|------|
| 正常正式 run | 是 | **只要** `.hydra/`，不要 snapshot |
| 遗留/迁移脚本尚未 Hydra | **不算**推荐正式路径 | 可写 snapshot 自用；**不得**标「当前」作结论，直到迁到 Hydra |
| 调试用临时脚本 | 否 | 随意；勿进 runs index 当前 |

## 磁盘布局

### 最少集（缺一不得标「当前」）

```text
runs/<task-slot>/<YYYY-MM-DD>/<HHMMSS>-<run-name>/
  git_commit.txt       # 或并入 evidence.json 的 commit 字段
  git_dirty.txt        # true | false
  git.diff.patch       # 干净 = 空文件；dirty = 非空完整 diff
  .hydra/config.yaml   # 正式路径必须有（见上表例外）
  command.txt
  seed.txt             # 或 evidence 内 seed 字段；可附确定性开关
```

### 推荐附加（有更好，无则仍可标当前）

```text
  environment.txt      # python 路径、关键包版本
  metrics.json
  status.txt           # success | failed
  run.log
```

**smoke run：** 也应尽量写最少集，但 **默认不要标「当前」**（除非人明确把该 smoke 当作基线结论）。

## 「当前 / 废弃」纪律（仅针对 runs）

1. **仅 `runs/<slot>/index.md`：** 每 slot **至多一个「当前」**（叙事主线）。  
2. **data 不受「一个当前」限制**——多条 data 可同时为「在用」，只要源 run 未废（见 [task-slots.md](./task-slots.md)）。  
3. **success ≠ 可引用**；可引用 = runs 的 **当前** 且 **最少集齐**。  
4. 替换当前：旧条目标 **废弃** + **原因** + 新条最少集齐。  
5. 禁止按日期猜最新；禁止只改 index、run 目录空空。  
6. failed run：建议仍进 index 标废弃或「失败留档」，**不得**标当前。

```markdown
| 状态 | 路径 | 原因 |
|------|------|------|
| **当前** | 2026-07-02/091412-fixed | 最少集齐；修 clip 后 |
| 废弃 | 2026-07-01/103000-bug | clip/entropy 不一致 |
```

## Agent 禁令

- 禁止无最少集的正式 run 标当前。  
- 禁止 dirty 且无完整 patch 仍当干净 commit 引用。  
- 禁止用聊天代替 command / 配置落盘。  
- 禁止把 data 的「多条在用」误判为违反「一个当前」（那只约束 **runs**）。  
- 禁止用 `config.snapshot` + 非 Hydra 入口冒充正式当前结论。
