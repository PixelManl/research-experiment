# 示例：data/ppo-baseline/index.md

**data ≠ runs。** 「一个当前」**不**限制 data：可有多条「在用」。

```markdown
# data / ppo-baseline

| data | 来自 run | 状态 | 备注 |
|------|----------|------|------|
| tables/returns_summary.parquet | 2026-07-02/091412-fixed | 在用 | 从当前 run 提取 |
| cache/rollout_feats/ | 2026-07-02/091412-fixed | 在用 | 可同时存在多条 |
| tables/returns_old.parquet | 2026-07-01/103000-bug | 废弃 | 上游 run 已废；待删 |

## 链路清理

raw_run → table_B → plot_D，若 B 的源 run 废弃：B 与 D 标废弃或删除。
```
