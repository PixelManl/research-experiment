# 示例：data/ppo-baseline/index.md

**data ≠ runs。** 这里只有提取/整理后的可复用材料，且每条指向来源 run。

```markdown
# data / ppo-baseline

| data | 来自 run | 状态 | 备注 |
|------|----------|------|------|
| tables/returns_summary.parquet | 2026-07-02/091412-fixed | 当前 | 从该 run metrics 提取 |
| tables/returns_old.parquet | 2026-07-01/103000-bug | 废弃 | 上游 run 已废；待删 |
| cache/rollout_feats/ | 2026-07-02/091412-fixed | 当前 | 可复用特征 |

## 链路清理

若提取链为 raw_run → table_B → plot_table_D，且 B 依赖的 run 废弃：

1. 废 run 已在 runs/index 标记
2. table_B、plot_table_D 标废弃或删除
3. 不在文档里继续引用 B/D 路径
```
