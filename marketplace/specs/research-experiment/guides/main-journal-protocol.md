# Main Journal Protocol

`docs/main/main.md` 是实验叙事链的主文件。
它回答的是："我们为什么走这条路，发现了什么，科学逻辑引向哪里。"
它不是任务清单，不是执行摘要，不是 T1/T2/T3 细目表。

## 角色分工

| 角色 | 职责 |
|---|---|
| Human | 提供昨日叙事草稿（可以不精确） |
| AI | 核实文件 → 纠正误记 → 输出正式版 |
| Human | 确认正式版 → AI 写入 `docs/main/main.md` |

**关键约束**：AI 不得在核实之前直接接受人类叙事。

## 触发 Prompt（每日使用）

```text
昨天我们做了 [X]，判断了 [Y]。
请先核实相关文件，然后输出今日 main.md 条目。
```

## AI 核实步骤（必须按序执行）

1. 读 `docs/research-log/source-of-truth.md`——昨日叙事中的事实是否有记录？
2. 读 `docs/research-log/invalidated-results.md`——有无相关结果已失效但人类未提及？
3. 跑 `python scripts/common/runs.py list <task-slot> --since <昨日>` 和 `runs.py latest <task-slot>`——产出状态与人类描述是否一致？canonical 是否空缺？
4. 读 `tests/<task-slot>/index.md`——测试结果是否支持人类的判断？
5. 如有差异，明确列出：**"你说的 X，文件显示的是 Y"**，不得沉默接受。

## 正式版条目格式

```markdown
## YYYY-MM-DD — <一句话主题>

### 实验叙事

<连贯段落。描述昨天做了什么、为什么这样做、
发现了什么问题或结论、科学逻辑如何推进到下一步。
不是 bullet list，是可以被未来自己读懂的故事。>

### 问题与解决（如有）

| 问题 | 解法 | 结果 | 影响范围 |
|---|---|---|---|
| ... | ... | ... | ... |

### 下一步的科学逻辑

<因为上面的结论，下一步应该 ...
不是任务清单，是"因此"的推导。>

### 链接
- source-of-truth related entry: `docs/research-log/source-of-truth.md`
- invalidated-results check: `docs/research-log/invalidated-results.md`
- related runs: registry ids, e.g. `ppo-handwritten#0007`（`runs.py show` 可溯源）
- related tests: `tests/<task-slot>/index.md`
```

## 核实差异的输出格式

当 AI 发现人类叙事与文件不一致时，必须在正式版前输出：

```markdown
### 核实差异（写入前请确认）

| 人类说 | 文件显示 | 来源 |
|---|---|---|
| baseline 已稳定 | `runs.py latest ppo-handwritten` 显示 canonical VACANT | run registry |
| 昨天测试全过 | tests/ppo-handwritten/ 有 2 个 FAIL | test index |
```

差异确认后再写入正式版。

## `docs/main/main.md` 维护规则

- 最新条目在最前（倒序）。
- 每日一个 `## YYYY-MM-DD` 条目，不拆分多个文件。
- 每个条目必须至少有一个文件链接，不允许裸断言。
- 不记录 T1 执行细节（那是 task-slot 日志的职责）。
- 如当日无新实验进展，仍需写一行状态，例如：

```markdown
## YYYY-MM-DD — 无新进展

等待 [X] 结果 / 今日专注文献 / 环境调试未完成。
下一步逻辑不变：[上一条目链接]。
```

## Forbidden

- AI 在未核实文件前直接把人类草稿当作事实写入。
- 把 `main.md` 变成脚本执行日志或 T1 任务列表。
- 在叙事里使用"实验成功"、"进展顺利"等无证据的情绪性表述。
- 跳过 `invalidated-results.md` 检查而引用旧结论。
- 同一天写多个独立条目（应合并）。
