# Run 证据包与 Git 铁律

## 一句话

**正式计算前把主体代码置于可说明的 git 状态；每次 run 目录留下身份卡。没有证据包，不得标「当前」，不得写进结论。**

策略：**A-default** — 允许 dirty tree，但必须留下完整 `git.diff.patch`；无 patch 不得标当前。

## 跑前：git 处理

```text
1. git status
2. 与本次实验相关的改动：
   - 优先 git add + commit（message 可短）
   - 若暂不 commit：必须接受 dirty 规则，禁止假装干净
3. 确认 Hydra 入口与将用配置组（见 config-entry / config-baseline）
4. 再启动计算
5. 证据写入本次 runs/<slot>/<日期>/<run-name>/
```

| 状态 | 可标「当前」？ | 必须留下 |
|------|----------------|----------|
| 干净 + 已 commit | ✅（且证据齐） | commit 哈希 |
| dirty | 仅当有完整 patch | commit + dirty=true + git.diff.patch |
| 非 git 仓库 | ❌ 正式 run | — |

## 配置证据：优先 Hydra 落盘，不重复造轮子

若 **configs 已进 git**，且 Hydra 把**合成后的配置**写进 run 目录（标准为 `.hydra/config.yaml` 等），则：

- **不必**再手写一份重复的 `config.snapshot.yaml`（避免双份漂移）。
- **必须**保证该次 run 目录内能打开「本次实际配置」（通常即 `.hydra/`）。
- 代码侧 git 证据仍要：commit / dirty / patch —— **配置进 git ≠ 代码进 git**。

若未使用 Hydra 输出目录：则必须显式写入 `config.snapshot.yaml`（合成结果）。

## 磁盘布局

```text
runs/<task-slot>/
  index.md
  <YYYY-MM-DD>/<HHMMSS>-<run-name>/
    git_commit.txt          # 或并入 evidence.json
    git_dirty.txt           # true | false
    git.diff.patch          # 干净可为空文件
    .hydra/                 # Hydra：合成配置真源（推荐）
    command.txt             # 完整启动命令
    seed.txt                # 或写在 metrics/evidence 内【必须】
    environment.txt         # 推荐：python 路径、关键包版本
    metrics.json
    status.txt              # success | failed
    run.log                 # 可选
```

### 最少集（缺一不得标「当前」）

1. **git commit**  
2. **dirty + patch**（干净则空 patch）  
3. **本次配置**（`.hydra/config.yaml` 或 `config.snapshot.yaml`）  
4. **command**  
5. **seed**（及相关确定性开关，可写入同一 evidence 文件）

## 「当前 / 废弃」纪律（P0-G）

1. 每 slot **至多一个「当前」**（叙事主线）。  
2. **success ≠ 可引用**；可引用 = **当前** 且 **证据齐全**。  
3. 替换当前：旧条目标 **废弃** + **错误/替换原因**（便于归因）+ 新条证据齐。  
4. 禁止按日期排序猜「最新即正确」。  
5. 禁止只改 index、run 目录空空。

废弃表示例：

```markdown
| 状态 | 路径 | 原因 |
|------|------|------|
| **当前** | 2026-07-02/091412-fixed | 证据齐；修 clip 后 |
| 废弃 | 2026-07-01/103000-bug | clip/entropy 不一致；勿引用 |
```

## Agent 禁令

- 禁止无 git 证据的正式 run 标当前。  
- 禁止 dirty 且无 patch 仍当干净 commit 引用。  
- 禁止用聊天代替 command / 配置落盘。
