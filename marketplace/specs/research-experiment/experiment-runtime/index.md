# Experiment Runtime Index

This layer defines how an experiment is started, configured, recorded, reproduced, and run concurrently. This index is navigation only; runtime contracts and implementation details belong in the linked files.

## Documentation Files

| File | Purpose | When to Read | Priority |
|---|---|---|---|
| [config-source-of-truth.md](./config-source-of-truth.md) | **CRITICAL**: 配置真源系统，防止配置漂移 | **每次实验前** - 这是最重要的 | **必须阅读** |
| [hydra-configuration.md](./hydra-configuration.md) | Hydra 入口、严格配置、debug 组 | 添加入口、配置字段、实验组或旧参数适配 | 必须阅读 |
| [run-registry.md](./run-registry.md) | Run 注册表：run id、两轴状态、canonical 唯一性、git snapshot、runs.py CLI | 定位/比较/引用/晋升/失效任何 run | 必须阅读 |
| [python-command.md](./python-command.md) | 跨平台 Python 解释器和命令规则 | 运行辅助脚本、规范命令、跨平台迁移 | 必须阅读 |
| [provenance.md](./provenance.md) | 配置、提交、snapshot、命令、环境和状态捕获 | 创建正式运行、比较结果、组织输出 | 必须阅读 |
| [smoke-dry-run.md](./smoke-dry-run.md) | 最小 smoke 和 dry-run 检查 | 重计算前、主流程变更后、调试配置时 | 必须阅读 |
| [logging.md](./logging.md) | 日志级别、stdout/stderr 捕获、运行日志 | 添加入口、并发运行、启用诊断 | 必须阅读 |
| [remote-concurrency.md](./remote-concurrency.md) | 远程资源、并发前提、清单 | SSH/远程运行、多进程运行、多机扫描 | 按需阅读 |

## Quick Navigation by Task

**BEFORE ANYTHING ELSE** - Read config truth:

- Read [config-source-of-truth.md](./config-source-of-truth.md) - **这是最重要的**
- 确保 `configs/truth/config.yaml` 存在且是真源
- 确保 `configs/truth/config_truth.md` 存在且内容正确
- **每次实验前必须验证配置**

Adding or changing Hydra config?

- Read [hydra-configuration.md](./hydra-configuration.md).
- Put new parameters in schema/config groups, not a growing argparse surface.
- Confirm unknown keys fail fast for formal runs.

Launching a formal run?

- Read [hydra-configuration.md](./hydra-configuration.md), [python-command.md](./python-command.md), [provenance.md](./provenance.md), [logging.md](./logging.md), and [../project-structure/outputs-organization.md](../project-structure/outputs-organization.md).
- Use `provenance.tracked_run(cfg)` so the run is registered, snapshotted, and captured automatically.
- Confirm the output path includes `<task-slot>`, date, and run name.

Locating, comparing, or changing the status of past runs?

- Read [run-registry.md](./run-registry.md).
- Use `runs.py latest|list|show|compare`; never walk date directories or write one-off aggregation scripts.
- Promote/invalidate via `runs.py promote|invalidate`; validity lives only in the registry.

Before heavy compute?

- Read [smoke-dry-run.md](./smoke-dry-run.md) and [../agent-collaboration/pre-heavy-run-review.md](../agent-collaboration/pre-heavy-run-review.md).
- Run smoke first and preserve the evidence.
- Do not launch expensive jobs before provenance and review are complete.

Running remotely or concurrently?

- Read [remote-concurrency.md](./remote-concurrency.md), [logging.md](./logging.md), and [provenance.md](./provenance.md).
- Redirect logs to files before parallel execution.
- Record concurrency manifest and machine/resource assumptions.

Debugging config or data paths?

- Read [smoke-dry-run.md](./smoke-dry-run.md).
- Use dry run for config/path validation and smoke run for a tiny real execution.

## Core Rules Summary

- **配置真源是第一优先级** - 阅读 [config-source-of-truth.md](./config-source-of-truth.md) 了解真源系统
- 正式运行必须使用 Hydra
- **必须**：每次实验前对比 `configs/truth/config.yaml` 验证配置
- 每次正式运行自动注册进 `outputs/<task-slot>/runs.jsonl` 并获得 git snapshot；有效性只通过 `runs.py promote|invalidate` 变更
- Python 命令必须使用验证过的项目解释器；agent 不能静默替换 `python` 和 `python3`
- 每次正式运行必须保存配置、提交、snapshot、命令、环境、日志、状态和指标
- 重计算需要 smoke-run 证据、`runs.py check` 通过和重计算前审查
- 异常可以在写入失败状态后崩溃；不要吞掉错误让运行看起来成功
