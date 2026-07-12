# 开干前

1. **Slot**  
   - 确定 `<task-slot>`；跨天不换 slot。  
   - 确认 `scripts|runs|data/<slot>/` 与 `index.md` 存在或将创建。

2. **意图**  
   - 读 `docs/main/`：目标仍是这个吗？  
   - 写/更新 `docs/plan/<slot>.md`。  
   - 涉及论文：模块旁或 plan 下已有 **PAPER 原文 .md**；抽取表与实现清单已写。

3. **禁止**  
   - 未写 plan 就按 ori 开超参。  
   - 在仓库根丢脚本。

4. **若改核心逻辑**  
   - 打开 [../linkage/coupled-changes.md](../linkage/coupled-changes.md)，标组件组。  
   - 有 Grep/MCP 则搜调用点，补进清单。  
   - 分层：algorithm 只动算法；指标/诊断/安全算子见 [../code/algorithm-split.md](../code/algorithm-split.md)。

5. **若会重算**  
   - 想好旧 run 如何标废弃；data 是否依赖旧 run。
