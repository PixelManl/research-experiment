# Paper 原文 → Plan → 1:1 实现

## 硬要求

**凡按某论文（或论文中某模块）设计的代码，该模块旁（或 plan 约定目录）必须有一份 `.md` 格式的 paper 原文（全文、章节或可定位摘录），设计与实现必须按该原文，而不是按记忆或 ori 源码默认。**

```text
模块目录或 plan 子树
  PAPER.md          # 原文（或原文摘录 + 出处页码/节号）
  （实现代码在 src/... 对照 PAPER + plan 清单）
```

## 推荐流程（实现方式保持简单）

本模板**不绑定**特定工具；流程用文件约定即可（后续可加脚本/MCP，非必须）。

1. **选定**：main 写明采用论文 A / 某节。
2. **落盘原文**：把相关原文整理为 `.md`（可从 PDF 粘贴/转换；保持可检索）。
3. **写 plan**：在 `docs/plan/<slot>.md` 中：
   - 链接到各模块 `PAPER.md`；
   - **抽取表**（超参、公式、模块行为、不采用的 ori 差异）；
   - **实现清单**（要改/要写的文件与函数）。
4. **1:1 实现**：代码只落实清单；清单外的「顺手改」先回 plan。
5. **对照**：实现后用清单勾选；公式/开关与 PAPER 不一致则停。

### 抽取表模板（可直接贴进 plan）

```markdown
## Paper 抽取 — <模块名>

原文：`docs/plan/modules/<module>/PAPER.md`（§x.x）

| key | paper | ori | we use | why |
|-----|-------|-----|--------|-----|
| clip.eps | 0.2 | 0.1 | 0.2 | 跟 paper；写入 yaml |
| entropy | on | off | on | 与 clip 同组件组 |

> 超参权威表只维护一处（本 plan 表 **或** `configs/baseline.md`，见 [config-baseline.md](./config-baseline.md)），禁止两处各写一套 we use。

## 公式 ↔ 代码（数学相关时）

| Eq/节 | 代码 path:fn | 测试 |
|-------|--------------|------|
| §3.2 clip | src/.../clip.py:ratio_clip | tests/<slot>/test_clip.py |

不确定 → 写「开放风险」，禁止当已解决。

## 实现清单

- [ ] `src/.../clip.py` — 与 PAPER §x 一致
- [ ] `src/.../entropy.py` — 同组联动
```

超参门禁与跑前轻量核对见 [config-baseline.md](./config-baseline.md)（**不必**每次开跑重读整本 plan）。

## 做不到「自动从 PDF 完美抽取」时

- 人工粘贴关键段落进 `PAPER.md` **足够**；不要求完美 OCR 流水线。
- Agent 允许帮助整理 md 与表格，但 **不得在没有原文文件时假装已对齐 paper**。
- 暂无自动化脚本：以本文件流程为准；有脚本后只是加速步骤 2–3，不改变「原文落盘 + 1:1」原则。

## 失败模式

| 错误 | 后果 |
|------|------|
| 只读 ori 默认超参 | 论文根本不用的开关被打开 → 整线作废 |
| 只有聊天里「我记得 paper 是…」 | 无法复核 |
| 有 PAPER.md 但实现不对照清单 | main/plan 与代码再次分叉 |
