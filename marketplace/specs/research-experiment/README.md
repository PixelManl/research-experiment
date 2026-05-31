# Research-Experiment Spec Template

本模板用于科研实验项目，尤其适合 RL/ML/数值实验/论文复现/算法验证场景。它的目标不是让 AI “多写代码”，而是让 AI 在每次动手前都被约束在可追溯、可验证、可清理的人机协作流程里。

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
- `agent-collaboration/`：T1/T2/T3 ownership、reviewer objections、失败证据、重计算前检查。
- `guides/`：实际任务开始前、重计算前、bug 复盘、停止/继续决策、spec 更新的操作清单。

## 使用方式

复制本目录内容到 `.trellis/spec/` 后，先让 AI 执行一次项目适配：

```text
请根据当前仓库，把 .trellis/spec/ 的 Research-Experiment 模板填成项目专属规范：
1. 替换 <package>、<task-slot> 和路径占位符；
2. 删除不适用的规则；
3. 从现有代码提取 Good/Bad examples；
4. 保持每个 index.md 简洁，只链接细则；
5. 最后列出还需要我人类确认的 T2/T3 决策。
```
