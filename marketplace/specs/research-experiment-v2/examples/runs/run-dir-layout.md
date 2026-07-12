# 示例：单次 run 目录应有的文件

```text
runs/ppo-baseline/2026-07-02/091412-fixed/
  git_commit.txt
  git_dirty.txt          # false
  git.diff.patch         # 可为空
  .hydra/
    config.yaml          # 本次合成配置（优先证据）
  command.txt
  seed.txt               # 或写入 evidence
  environment.txt
  metrics.json
  status.txt             # success
  run.log
```

`runs/ppo-baseline/index.md` 仅在上述齐全时可将该路径标为 **当前**。
