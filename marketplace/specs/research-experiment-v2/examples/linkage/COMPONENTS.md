# 示例：组件组 policy-surrogate

```markdown
## Bundle: policy-surrogate

| 成员 | 路径 | 改 clip 时 |
|------|------|------------|
| hard_clip / ratio | src/pkg/algorithm/clip.py | 必改 |
| dist.entropy() | src/pkg/algorithm/entropy.py | 必查 mask/停用 |
| approx_kl | src/pkg/diag/kl.py | 诊断尺度（diag，非 algorithm） |
| return_mean | src/pkg/metric/returns.py | 指标（mc） |
| tests | tests/ppo-baseline/test_surrogate.py | 必跑 |

改组内任一点：打开本表 → Grep 调用点 → 同轮改完或写明不改原因。
```
