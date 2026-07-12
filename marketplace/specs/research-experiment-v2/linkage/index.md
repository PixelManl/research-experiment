# Linkage Index

语义级联动：组件成组修改，避免只改 clip 忘了 entropy。

## Guidelines Index

| Guide | Description | When to Read |
|-------|-------------|--------------|
| [coupled-changes.md](./coupled-changes.md) | 组件组织；改前依赖；工具可选 | 改 loss/reward/clip/mask/分布/指标等核心逻辑时 |

## Pre-Development Checklist

- [ ] 识别本次改动所属 **组件组**（见 coupled-changes 例子）。
- [ ] 列出同组必须同改或显式声明不改的符号/文件。
- [ ] plan 中有联动说明（或本轮任务笔记中有清单）。
- [ ] 若有代码搜索/MCP：已用其辅助找调用点（非必须，但推荐）。

## Quality Check

- [ ] 同组依赖无「半更新」（一处新语义、另一处仍旧假设）。
- [ ] 相关 metrics/diagnostics 仍与新语义一致，或已标废弃。
- [ ] 若旧 run/data 依赖旧语义：已按 organize 规则废弃。
