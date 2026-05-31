# Project Structure Index

本层只规定科研项目的文件组织。详细规则放在链接文件中；不要把细则堆在本 index。

| Topic | File | Status |
|---|---|---|
| Repository layout | `directory-layout.md` | Template |
| Task-slot contract | `task-slots.md` | Template |
| Unit test organization | `tests-organization.md` | Template |
| Script organization | `scripts-organization.md` | Template |
| Output organization | `outputs-organization.md` | Template |
| Dead-code cleanup | `cleanup-dead-code.md` | Template |

## Non-negotiable

- `tests/`、`scripts/`、`outputs/` 必须按 `<task-slot>` 对齐。
- 每个 root index 和 task-slot index 都必须简洁：只放目录、命令、状态、链接，不放长日志。
- 废弃实现用 git/ledger 追溯，不用 `old.py`、`v2.py`、大段注释留尸体。
