# 组件级语义联动

## 问题

Agent 常 **单点优化**一个函数，不联想多步：

- 改了 **hard-clip** 的语义，却仍调用旧的 `dist.entropy()` 假设；
- 改了 reward 缩放，指标与 advantage 仍按旧尺度；
- 关了 value loss，日志与 checkpoint 字段仍当 value 有效。

这是 **组件组织** 问题：若干符号/文件在语义上是一组，必须一起变更或一起宣布废弃。

## 抽象：组件组（Component Bundle）

把「改 A 必须想到 B、C」写成显式组，而不是靠临场聪明。

示例：

```text
Bundle: policy-surrogate
  - hard_clip / ratio clip
  - dist.entropy() / entropy bonus
  - approx_kl 记录
  - 相关 unit test

Bundle: reward-scale
  - reward transform
  - advantage / return
  - metrics 里的 return_mean
```

### 建议落盘位置（简单即可）

在 plan 或模块目录维护短表 `COMPONENTS.md`：

```markdown
## policy-surrogate
| 成员 | 路径 | 备注 |
|------|------|------|
| clip | src/.../clip.py | |
| entropy | src/.../entropy.py | 与 clip 共用 mask |
| tests | tests/<slot>/test_surrogate.py | |
```

改组内任一点 → 打开该表走一遍。

## 改前最小动作

1. 点名本次改动落入哪个 **bundle**（或新建一行）。
2. 列出同组文件/函数。
3. 逐项：同改 / 确认不受影响（写一句为什么）/ 暂时不做（写风险）。
4. 跑同组相关测试；没有测试则补一条最小断言或手动数值检查。

## 有没有「动态索引」工具？

**没有强制绑定的魔法索引器**；用现有手段即可，有更好工具就挂上：

| 手段 | 作用 | 说明 |
|------|------|------|
| 仓库内搜索（Grep/IDE） | 找 `entropy`、`clip`、调用点 | 默认必备 |
| 测试与类型 | 改坏立刻红 | 组件组应有至少一条测试 |
| MCP / 代码图 / 引用分析 | 辅助列「谁调用了谁」 | **可选**；有则在 before-work 用，无则手列 bundle 表 |
| 自定义小脚本 | 扫注册表「组件成员列表」 | 可选增强，非本模板核心 |

原则：**工具是加速找依赖的；source of truth 仍是 COMPONENTS/plan 里的组件表 + 代码本身。**  
不要等「完美动态索引」才写联动表——一张 markdown 表就胜过聊天记忆。

## 与 runs/data

语义变了 → 旧语义下的 **当前 run** 应标废弃 → 依赖它的 **data** 删或标废弃（见 organize）。  
联动不只改代码，也切断错误结果链。
