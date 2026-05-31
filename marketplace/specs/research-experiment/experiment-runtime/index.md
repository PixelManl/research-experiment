# Experiment Runtime Index

本层规定一次实验如何启动、配置、记录、复现和并发运行。

| Topic | File | Status |
|---|---|---|
| Hydra configuration | `hydra-configuration.md` | Template |
| Provenance | `provenance.md` | Template |
| Smoke / dry run | `smoke-dry-run.md` | Template |
| Logging | `logging.md` | Template |
| Remote concurrency | `remote-concurrency.md` | Template |

## Non-negotiable

- 正式 run 必须由 Hydra 配置驱动。
- 每次正式 run 必须保存 config、commit、diff patch、命令、日志和环境。
- 重型计算前必须先完成 smoke run 和 pre-heavy-run review。
