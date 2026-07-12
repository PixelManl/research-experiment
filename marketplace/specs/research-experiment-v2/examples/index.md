# Examples Index

**参考示例，不是编码合同。** 安装后在 `.trellis/spec/examples/`。  
初始化仓库 → 先看 **scaffold**；细则对照 organize / intent 正文。

## Guidelines Index

| 示例 | 说明 | 何时看 |
|------|------|--------|
| [scaffold/LAYOUT.md](./scaffold/LAYOUT.md) | **整仓脚手架树** + 初始化顺序 | 空仓库 / 新项目落地 |
| [configs/snippets.md](./configs/snippets.md) | Hydra / task / smoke / run.dir 片段 | 配 configs 时 |
| [indexes/scripts-index.md](./indexes/scripts-index.md) | scripts index 样例 | 建 slot 脚本时 |
| [indexes/runs-index.md](./indexes/runs-index.md) | runs 当前/废弃 | 重算、引用结果 |
| [indexes/data-index.md](./indexes/data-index.md) | data 软链 run | 提取数据、清链路 |
| [runs/run-dir-layout.md](./runs/run-dir-layout.md) | 单次 run 证据最少集 / dirty | 正式跑落盘 |
| [plan/slot-plan.md](./plan/slot-plan.md) | plan + 超参表 + 公式行 | 写 docs/plan |
| [linkage/COMPONENTS.md](./linkage/COMPONENTS.md) | 组件组 | 改 clip/entropy 等 |
| [code/call-shape.md](./code/call-shape.md) | algorithm→mc/diag/utils | 写包内分层 |

## Pre-Development Checklist

- [ ] 不把 examples 路径写进 `implement.jsonl` 当正式规范。  
- [ ] 复制时替换 `<package>` / `<task-slot>`。  
- [ ] 脚手架以 [scaffold/LAYOUT.md](./scaffold/LAYOUT.md) 为准，不要抄 v1 的 `outputs/` / `truth/` 形。

## Quality Check

- [ ] 仓库真实目录与 LAYOUT 对齐（或有意删减并写明）。  
- [ ] index / plan / 证据形状来自 examples，内容已改成项目事实。
