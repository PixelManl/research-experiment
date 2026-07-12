# Tests 按 task-slot

## 一句话

**测试与 scripts/runs/data 同 slot；控制数量；mock 可以，烟雾靠 smoke 真跑。**

## 布局

```text
tests/<task-slot>/
  index.md              # 重要测试 + 命令
  test_*.py
tests/common/           # 真共用才放
```

## 规则

- slot 名与研究工作流一致，**不要**把所有测试堆成一百多个无归属文件。  
- 预算建议（可按项目改）：每 slot **约 3～8** 个单测 + 需要时 1 个稍重的集成；整体避免无限制膨胀。  
- **Unit test 可以 mock** 依赖与 IO。  
- **Smoke 不是 test**：`debug=smoke` 走真实 Hydra 入口与配置（见 [config-entry.md](./config-entry.md)）。  
- 禁止把完整长时间训练当作 unit test。  
- 改 algorithm 核心（loss/clip/…）→ 同 slot 补/跑相关测试；数值边界优先进 utils 测。

## index 示例

```markdown
# tests / ppo-baseline

| 测试 | 命令 | 备注 |
|------|------|------|
| test_clip.py | pytest tests/ppo-baseline/test_clip.py | |
| 全 slot | pytest tests/ppo-baseline -q | 提交前 |
```

## Agent 禁令

- 禁止只在仓库根丢 `test_misc.py`。  
- 禁止用 mock 单测冒充「已 smoke」。
