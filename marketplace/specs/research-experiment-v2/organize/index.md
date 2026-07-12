# Organize Index

按 `<task-slot>` 组织脚本、runs、data、tests、配置；run 必须带证据包。

## Guidelines Index

| Guide | Description | When to Read |
|-------|-------------|--------------|
| [task-slots.md](./task-slots.md) | slot；scripts/runs/data；跨天；当前/废弃 | 新建任务、落盘 |
| [run-evidence.md](./run-evidence.md) | git 处理；证据最少集；Hydra 配置落盘 | **每次正式 run 前/后** |
| [config-entry.md](./config-entry.md) | Hydra；yaml>arg；slot 化 configs；smoke | 加入口、改配置结构 |
| [tests.md](./tests.md) | tests 按 slot；mock vs smoke | 加测试、改算法前 |

## Pre-Development Checklist

- [ ] 稳定 `<task-slot>`；路径在 `scripts|runs|data|tests/<slot>/`。  
- [ ] 正式跑：已读 [run-evidence.md](./run-evidence.md)，git 状态可说明。  
- [ ] 配置走 Hydra；defaults 在 yaml；见 [config-entry.md](./config-entry.md)。  
- [ ] 将跑配置相对 baseline 表无静默 ori 冲突；见 [../intent/config-baseline.md](../intent/config-baseline.md)。  
- [ ] 分清 run 证据 vs 可复用 data。

## Quality Check

- [ ] 「当前」run 证据齐全（commit/dirty+patch/配置/command/seed）。  
- [ ] 废弃条有原因；data 下游已清理。  
- [ ] 无根目录脚本/测试垃圾堆。
