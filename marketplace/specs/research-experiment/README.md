# Research-Experiment Spec Template

本模板用于科研实验项目，尤其适合 RL/ML/数值实验/论文复现/算法验证场景。它是 Trellis `.trellis/spec/` 规范模板，不是可运行的科研代码项目，也不是默认脚手架生成器。它的目标不是让 AI “多写代码”，而是让 AI 在每次动手前都被约束在可追溯、可验证、可清理的人机协作流程里。

## 核心原则

1. **文件系统是真源**：conversation 会消失，文件不会。重要结论、失败、失效数据、baseline 变更、reviewer objection 必须写入文件。
2. **task-slot 贯穿全链路**：同一研究任务的 tests/scripts/outputs/ledger 必须共享同一个 `<task-slot>`。
3. **Hydra 是配置入口**：正式实验不得靠大量 argparse 参数拼接；新增参数必须进入 schema 与配置组。
4. **重计算前先审查**：任何重型实验必须先通过 smoke run、任务级测试、配置快照、diff patch、独立 review。
5. **数学和实现逐行对齐**：公式、张量形状、数据 schema、数值稳定函数必须可被人类快速检查。
6. **失败是机制证据**：失败 run 不应该隐藏，而应记录为“为什么不能继续这个叙事”的证据。

## 推荐项目形状

```text
.
├── src/<package>/
│   ├── policy/
│   ├── runner/
│   ├── process.py
│   ├── metrics.py
│   ├── diagnostics.py
│   ├── numerics.py
│   ├── schema.py
│   ├── validate.py
│   ├── plotting.py
│   └── provenance.py
├── configs/
│   ├── config.yaml
│   ├── schema.py
│   ├── task/
│   ├── experiment/
│   ├── debug/
│   └── hydra/
├── scripts/
│   ├── index.md
│   ├── common/
│   ├── remote/
│   └── <task-slot>/
├── tests/
│   ├── index.md
│   ├── common/
│   └── <task-slot>/
├── outputs/
│   ├── index.md
│   └── <task-slot>/
│       └── <YYYY-MM-DD>/
├── data/
│   └── processed/
├── docs/
│   ├── main/
│   │   └── main.md
│   └── research-log/
│       ├── index.md
│       ├── baselines.md
│       ├── source-of-truth.md
│       ├── invalidated-results.md
│       ├── reviewer-objections.md
│       ├── decisions/
│       ├── tasks/
│       ├── reports/
│       └── equation-maps/
└── .trellis/spec/
```

## Spec layers

- `project-structure/`：目录、task-slot、tests/scripts/outputs、死代码清理。
- `experiment-runtime/`：Hydra、运行溯源、smoke/dry run、日志、远程并发。
- `research-code/`：代码风格、数学映射、张量形状、validate/assert、numerics、schema、随机性。
- `experiment-modules/`：process/metrics/diagnostics 拆分、评估、绘图、报告。
- `research-pitfalls/`：高频失配、失效模式、反复踩坑点，以及对应的 CI 触发规则。
- `agent-collaboration/`：T1/T2/T3 ownership、reviewer objections、失败证据、重计算前检查。
- `guides/`：实际任务开始前、重计算前、bug 复盘、停止/继续决策、spec 更新的操作清单。

## Quick Navigation by Research Task

Starting or adapting a project?

- Read [project-structure/index.md](./project-structure/index.md).
- Read [guides/before-dev-checklist.md](./guides/before-dev-checklist.md).
- Read [agent-collaboration/ownership-tiers.md](./agent-collaboration/ownership-tiers.md).

Starting a new task-slot?

- Read [project-structure/task-slots.md](./project-structure/task-slots.md).
- Read [project-structure/tests-organization.md](./project-structure/tests-organization.md).
- Read [project-structure/scripts-organization.md](./project-structure/scripts-organization.md).
- Read [project-structure/outputs-organization.md](./project-structure/outputs-organization.md).
- Create or update `docs/research-log/tasks/<task-slot>.md`.

Extending the same Trellis task with Stage A/B/C or A1/A2/A3?

- Read [project-structure/staged-task-expansion.md](./project-structure/staged-task-expansion.md).
- Expand the current PRD when the same scientific object, code path, and claim boundary keep evolving.
- Split any stage into local substages such as A1/A2/A3 when the substage boundary is useful.

Changing math, loss, reward, or objective code?

- Read [research-code/math-formula-mapping.md](./research-code/math-formula-mapping.md).
- Read [research-code/tensor-shapes-typing.md](./research-code/tensor-shapes-typing.md).
- Read [research-code/validation-assertions.md](./research-code/validation-assertions.md).
- Read [research-code/numerics.md](./research-code/numerics.md).
- Record unresolved concerns in [agent-collaboration/reviewer-objections-ledger.md](./agent-collaboration/reviewer-objections-ledger.md).

Launching a formal run?

- Read [experiment-runtime/hydra-configuration.md](./experiment-runtime/hydra-configuration.md).
- Read [experiment-runtime/provenance.md](./experiment-runtime/provenance.md).
- Read [experiment-runtime/logging.md](./experiment-runtime/logging.md).
- Read [project-structure/outputs-organization.md](./project-structure/outputs-organization.md).

Before heavy compute?

- Read [experiment-runtime/smoke-dry-run.md](./experiment-runtime/smoke-dry-run.md).
- Read [guides/before-heavy-run-checklist.md](./guides/before-heavy-run-checklist.md).
- Read [agent-collaboration/pre-heavy-run-review.md](./agent-collaboration/pre-heavy-run-review.md).
- Read [agent-collaboration/external-heavy-model-review.md](./agent-collaboration/external-heavy-model-review.md) only when the user asks for or approves an external heavy-model packet.

Preparing a heavy-package for GPT-5.5 Pro or another advanced external model?

- Read [agent-collaboration/external-heavy-model-review.md](./agent-collaboration/external-heavy-model-review.md).
- Package sanitized context with a two-part English prompt: current-problem directed review plus future-direction creative review.
- Do not create, export, or upload a heavy-package without explicit user request or approval.

Changing a baseline or metric?

- Read [experiment-modules/evaluation-and-baselines.md](./experiment-modules/evaluation-and-baselines.md).
- Read [experiment-modules/process-metric-diagnose.md](./experiment-modules/process-metric-diagnose.md).
- Read [agent-collaboration/claims-and-decisions.md](./agent-collaboration/claims-and-decisions.md).

Changing a core mechanism that may affect downstream logic?

- Read [research-pitfalls/coupled-logic-drift.md](./research-pitfalls/coupled-logic-drift.md).
- Read [research-code/math-formula-mapping.md](./research-code/math-formula-mapping.md).
- Read [research-code/validation-assertions.md](./research-code/validation-assertions.md).
- Trace dependent objectives, entropy terms, metrics, diagnostics, baselines, and reports before accepting the change.

Creating figures or reports?

- Read [experiment-modules/figures.md](./experiment-modules/figures.md).
- Read [experiment-modules/reports.md](./experiment-modules/reports.md).
- Read [agent-collaboration/claims-and-decisions.md](./agent-collaboration/claims-and-decisions.md).
- Use only valid, source-backed run ids.

Handling failed or invalidated results?

- Read [agent-collaboration/failure-evidence-ledger.md](./agent-collaboration/failure-evidence-ledger.md).
- Read [agent-collaboration/claims-and-decisions.md](./agent-collaboration/claims-and-decisions.md).
- Read [guides/research-stop-continue-decision.md](./guides/research-stop-continue-decision.md).
- Update invalidated results and source-of-truth records.

After fixing a bug?

- Read [guides/bug-root-cause-retrospective.md](./guides/bug-root-cause-retrospective.md).
- Read [agent-collaboration/break-loop-ci.md](./agent-collaboration/break-loop-ci.md).
- Add a test, validation rule, checklist item, or spec update when the bug class is preventable.

Updating project conventions?

- Read [guides/spec-update-guide.md](./guides/spec-update-guide.md).
- Update the smallest relevant spec file.
- Do not rely on chat memory as the only record.

## 使用方式

复制本目录内容到 `.trellis/spec/` 后，先做项目适配。Specs are meant to be customized: 不要把本模板当成永远不变的通用规则，而应根据真实仓库删除不适用内容、替换路径占位符、加入项目自己的 Good/Bad examples。

先让 AI 执行一次项目适配：

```text
请根据当前仓库，把 .trellis/spec/ 的 Research-Experiment 模板填成项目专属规范：
1. 替换 <package>、<task-slot> 和路径占位符；
2. 删除不适用的规则；
3. 从现有代码提取 Good/Bad examples；
4. 保持每个 index.md 简洁，只链接细则；
5. 最后列出还需要我人类确认的 T2/T3 决策。
```

## Pitfall / CI layer

This layer captures recurring failure modes and turns them into review gates, regression tests, and checklist updates. Start with [research-pitfalls/index.md](./research-pitfalls/index.md) when a change is locally correct but may shift downstream meaning.

## On-demand scaffold rule

Create filesystem scaffolding only when a task needs a persistent filesystem identity. Read-only inspections, audits, and other validation-only tasks should stay read-only and should not create extra directories, ledgers, or planning files.

## 可选脚手架参考

`examples/bootstrap/bootstrap.py` 是可选参考脚本，用来说明如何按本 spec 创建初始目录。它不属于 spec 核心规则，也不应被理解为 Trellis template 必须执行的入口。

如果未来需要自动化脚手架，应该独立设计为 skill：先读取目标仓库，再根据项目真实结构创建 task-slot、tests/scripts/outputs/docs ledger。
