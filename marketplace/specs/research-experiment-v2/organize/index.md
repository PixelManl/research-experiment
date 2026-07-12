# Organize Index

按 `<task-slot>` 组织脚本、runs、data。不强制重审计；**必须组织好**。

## Guidelines Index

| Guide | Description | When to Read |
|-------|-------------|--------------|
| [task-slots.md](./task-slots.md) | slot 命名；scripts/runs/data；跨天；index 规则；runs≠data | 新建任务、加脚本、落盘数据/结果 |

## Pre-Development Checklist

- [ ] 已有稳定 `<task-slot>`（无日期当 slot 名）。
- [ ] 将使用的路径落在 `scripts|runs|data/<task-slot>/`，不是仓库根。
- [ ] 会更新对应 `index.md`（重要脚本 / 当前 run / data 来源）。
- [ ] 分清本次产物是 **run 证据** 还是 **可复用 data**（见 task-slots）。
- [ ] 多日任务：slot 不变，其下按日期分子目录，由 slot 级 index 汇总。

## Quality Check

- [ ] 无根目录一次性脚本堆。
- [ ] `runs/<slot>/index.md` 标明 **当前**（至多一个叙事主线）与 **废弃**。
- [ ] `data/<slot>/index.md` 标明 **来自哪个 run**；废弃 run 的下游 data 已删或已标废弃。
- [ ] index 保持一屏内：链接 + 一句说明，不写长文。
