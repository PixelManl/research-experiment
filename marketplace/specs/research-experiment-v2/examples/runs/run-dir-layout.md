# 示例：单次 run 目录（对齐最少集）

> 参考非合同。标「当前」的门槛以 [../../organize/run-evidence.md](../../organize/run-evidence.md) **最少集** 为准。

## 干净树（可标当前，若其它最少集也齐）

```text
runs/ppo-baseline/2026-07-02/091412-fixed/
  git_commit.txt       # abc1234
  git_dirty.txt        # false
  git.diff.patch       # 空文件即可
  .hydra/
    config.yaml        # 本次合成配置【正式必须】
  command.txt
  seed.txt
  # --- 以下推荐，非标当前门槛 ---
  environment.txt
  metrics.json
  status.txt           # success
  run.log
```

## dirty 树（必须有非空 patch 才可标当前）

```text
runs/ppo-baseline/2026-07-02/150000-wip/
  git_commit.txt       # abc1234（脏改所基于的 HEAD）
  git_dirty.txt        # true
  git.diff.patch       # 非空：git diff HEAD > git.diff.patch
  .hydra/config.yaml
  command.txt
  seed.txt
```

禁止：`dirty=true` 但 `git.diff.patch` 为空或不存在，仍写入 index **当前**。

## 与 index

`runs/ppo-baseline/index.md` 仅在 **最少集齐全** 时可将路径标为 **当前**；推荐文件缺失不阻拦「当前」。
