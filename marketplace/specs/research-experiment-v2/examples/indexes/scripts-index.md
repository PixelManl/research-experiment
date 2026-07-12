# 示例：scripts/ppo-baseline/index.md

```markdown
# scripts / ppo-baseline

| 脚本 | 用途 | 备注 |
|------|------|------|
| [run_train.py](./run_train.py) | 正式训练入口 | 当前主入口 |
| [eval_only.py](./eval_only.py) | 只评估 | |
| [2026-07-01/probe_clip.py](./2026-07-01/probe_clip.py) | 当日试错 | 可删 |

跨天脚本可放在日期子目录；总入口尽量稳定在 slot 根下。
```
