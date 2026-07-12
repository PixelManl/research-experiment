# 开干前

## 1. Slot 与组织

- 确定 `<task-slot>`；跨天不换 slot。  
- `scripts|runs|data|tests/<slot>/` 与 index 就绪或将建。

## 2. 意图（设计时，非整本每次开跑）

- `docs/main/`：目标仍是这个吗？  
- 写/更新 `docs/plan/<slot>.md`；论文模块有 PAPER.md。  
- **实现时**对照 plan 清单；**开跑时不要**把整本 plan 再通读一遍。

## 3. 配置（开跑轻量门禁）

- Hydra 入口；yaml > arg；见 [../organize/config-entry.md](../organize/config-entry.md)。  
- 打开 **baseline / 超参抽取表**（短表），对照本次 task/experiment 关键键。  
- 禁静默 ori 默认；见 [../intent/config-baseline.md](../intent/config-baseline.md)。

## 4. 正式 run 前 git

- [../organize/run-evidence.md](../organize/run-evidence.md)：status → commit 或 dirty+patch。  
- 准备 seed；command 可复述。

## 5. 改核心逻辑时

- [../linkage/coupled-changes.md](../linkage/coupled-changes.md) 组件组。  
- [../code/algorithm-split.md](../code/algorithm-split.md)：algorithm / mc / diag / utils。

## 6. 测试 vs Smoke

- `pytest tests/<slot>`（可 mock）。  
- **重活/重算前**再 `debug=smoke`：**真路径**小跑，写出 run 目录（非 mock）。

## 7. 重算 / 标结果

- 想好旧 run 废弃原因；data 下游。  
- 仅证据齐全可标当前。

## 8. 开下一研究阶段时

- 读 [route-value.md](./route-value.md)：做完 ≠ 有价值。

## 9. Ownership 短表

| 级 | 谁 | 例 |
|----|-----|-----|
| T1 | AI 可执行 | index、测例、按 plan 实现、格式 |
| T2 | AI 起草人知悉 | baseline 变更、跟 ori 不跟 paper、指标重定义 |
| T3 | 人定 | 放弃路线、大算力、改论文故事 |

## 禁止

- 未写 plan 就按 ori 开超参。  
- 仓库根堆脚本。  
- 无 smoke 直接 heavy 扫参。  
- 无证据标当前。
