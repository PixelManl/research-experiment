# Examples Index

**参考示例，不是编码合同。** 安装后路径在 `.trellis/spec/examples/`。  
照抄前先对照 organize / intent / linkage 正文；示例只演示形状。

## Guidelines Index

| 示例 | 说明 | 何时看 |
|------|------|--------|
| [indexes/scripts-index.md](./indexes/scripts-index.md) | scripts 下 index 样例 | 建 slot 脚本目录时 |
| [indexes/runs-index.md](./indexes/runs-index.md) | runs 当前/废弃 样例（防 7-01） | 重算、作图引用前 |
| [indexes/data-index.md](./indexes/data-index.md) | data 软链 run、下游废弃 | 提取数据、清脏链路时 |
| [plan/slot-plan.md](./plan/slot-plan.md) | plan + paper 抽取表骨架 | 写 docs/plan 时 |
| [linkage/COMPONENTS.md](./linkage/COMPONENTS.md) | 组件组表样例 | 改 clip/entropy 等时 |

## Pre-Development Checklist

- [ ] 确认示例路径不会被写进 `implement.jsonl` 当正式规范。
- [ ] 复制到项目时改成真实 slot/包名。

## Quality Check

- [ ] 项目里的 index **实际文件**已按示例精神维护，而不是只留在 examples/。
- [ ] 未把 example 里的假路径当真实 runs/data。
