# 示例：组件组 policy-surrogate

```markdown
## Bundle: policy-surrogate

| 成员 | 路径 | 改 clip 时 |
|------|------|------------|
| hard_clip / ratio | src/pkg/clip.py | 必改 |
| dist.entropy() | src/pkg/entropy.py | 必查：mask/停用是否仍成立 |
| approx_kl log | src/pkg/diagnostics.py | 必查尺度 |
| tests | tests/ppo-baseline/test_surrogate.py | 必跑 |

改组内任一点：打开本表 → Grep 调用点 → 同轮改完或写明不改原因。
```
