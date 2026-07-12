# 示例：algorithm / mc / diag / utils 调用形状

```text
src/pkg/
  algorithm/ppo.py      # 主更新，返回 intermediates
  metric/returns.py     # mc.return_mean(...)
  diag/grad_health.py   # diag.grad_norm_ok(...)
  utils/safe_ops.py     # safe_div, safe_log_softmax
```

```python
# algorithm 内：替换式安全算子（示意）
ratio = utils.safe_div(new_prob, old_prob.clamp_min(0.0), eps=1e-8)
# 不要：ratio = new_prob / (old_prob + 1e-8)  复制粘贴满文件

# script 编排
out = algorithm.ppo_update(batch)          # 中间产物
metrics = {
    "return_mean": mc.return_mean(out.traj),
}
diags = {
    "grad_ok": diag.grad_norm_ok(out.grads),
}
# 写入 runs/<slot>/...
```

algorithm 保持像公式；统计与诊断在外；安全细节在 utils。
