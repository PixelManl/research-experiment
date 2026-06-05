# Research-Experiment Trellis Spec Template v1.1

这是一个面向科研实验项目的 Trellis `.trellis/spec/` 模板。它不是可运行的科研代码项目，也不是默认脚手架生成器，而是一组让 AI 和人类共同遵守的研究工程规范。

## 安装方式 A：直接复制

把下面目录的内容复制到目标项目的 `.trellis/spec/`：

```text
marketplace/specs/research-experiment/
```

复制后目标项目应类似：

```text
.trellis/spec/
├── README.md
├── project-structure/
├── experiment-runtime/
├── research-code/
├── experiment-modules/
├── agent-collaboration/
├── guides/
└── examples/          # optional examples, not required spec rules
```

## 安装方式 B：作为 Trellis 自定义 registry

把整个仓库发布到 GitHub/GitLab/Bitbucket 后，可用：

```bash
trellis init --registry gh:<org>/<repo>/marketplace --template research-experiment
```

## 使用方式 C：可选脚手架参考

模板内的 `examples/bootstrap/bootstrap.py` 只是可选参考，用于说明如何按本 spec 生成一个初始科研项目目录。它不属于 Trellis spec 的核心规则；未来如果需要自动化脚手架，应作为独立 skill 设计，而不是混入 spec template 本体。

## v1.1 更新重点

- Clarifies spec-only scope and moves the optional scaffold helper under `examples/bootstrap/`.
- Adds task-oriented quick navigation for research workflows.
- Upgrades layer indexes into agent-friendly navigation tables.
- Defines reusable spec page shapes for contracts, guides, and pitfall pages.
- Adds `When to Read` / `When to Use` triggers across core spec pages.
- Cleans relative Markdown links so template-local links resolve.

## 设计重点

- task-slot 贯穿 `tests/`、`scripts/`、`outputs/`、research ledger。
- Hydra 作为配置真源，禁止在正式入口堆 60 个 argparse 参数。
- 每次运行强制保存 config、git commit、git diff patch、命令、环境和日志。
- 数学公式、张量形状、数值稳定性、随机种子、数据 schema 都有可检查契约。
- Agent 不能只“继续调故事”；它必须维护失败证据、反对意见、失效结果和停止/继续决策。
- 人机协作按 T1/T2/T3 ownership 分层：AI 可执行，AI 可草拟，Human 必须决定。
