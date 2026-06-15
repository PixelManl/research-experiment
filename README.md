# Research-Experiment Trellis Spec Template v1.23

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
├── research-pitfalls/
├── agent-collaboration/
├── guides/
└── examples/          # optional examples, not required spec rules
```

## 安装方式 B：作为 Trellis 自定义 registry

把整个仓库发布到 GitHub/GitLab/Bitbucket 后，可用：

```bash
trellis init --registry gh:<org>/<repo>/marketplace --template research-experiment
```

本仓库的 `marketplace/index.json` 位于仓库根目录下的 `marketplace/` 子目录中。Trellis template `path` 按 Git 仓库根目录解析，因此 registry 条目使用 `marketplace/specs/research-experiment`，而不是 `specs/research-experiment`。

Trellis 自定义 registry 当前是 spec template marketplace：`trellis init --registry` 只安装 `type: "spec"` 的模板。仓库里的 optional skill / agent 是参考资产，不注册到 `marketplace/index.json`，需要按目标平台的 skill/agent 目录手动复制或另行打包。

Trellis 0.6 会把 registry spec source 和 template id 写入 `.trellis/config.yaml`，后续可用 `trellis update` 走 hash / conflict / modified-by-you 流程刷新 `.trellis/spec/`。更新后仍要人工审查本项目对模板的本地改写，不要把源模板当成实时远程 wiki。

## 使用方式 C：可选脚手架参考

模板内的 `examples/bootstrap/bootstrap.py` 只是可选参考，用于说明如何按本 spec 生成一个初始科研项目目录。它不属于 Trellis spec 的核心规则；未来如果需要自动化脚手架，应作为独立 skill 设计，而不是混入 spec template 本体。

## Marketplace contents

本仓库的 `marketplace/` 目录包含一个可由 Trellis registry 安装的 spec template，以及两个可选参考资产：

```text
marketplace/
├── index.json  # spec registry index; only lists type: "spec"
├── specs/      # Trellis spec templates copied into .trellis/spec/
├── skills/     # Optional Agent Skill source; not installed by trellis init --registry
└── agents/     # Optional focused sub-agent source; not installed by trellis init --registry
```

当前包含：

- `marketplace/specs/research-experiment`：Research-Experiment Trellis spec template，由 `trellis init --registry` 安装。
- `marketplace/skills/scaffolder`：可选 Agent Skill 源文件，只负责 audit / dry-run / apply 一个保守的项目文件骨架或 task-slot 文件骨架；需要按目标平台 skill 目录手动安装或另行打包。
- `marketplace/agents/logic-chain-checker.md`：只读 agent 源文件，专门检查核心逻辑变化后的下游逻辑耦合失配；需要按目标平台 agent 格式安装。

## v1.23 更新重点

- Aligns `marketplace/index.json` with Trellis custom registry semantics: only `type: "spec"` entries are registered.
- Clarifies that optional skill/agent files are source assets, not installed by `trellis init --registry`.
- Adds Trellis 0.6-aware mapping for `prd.md`, `design.md`, `implement.md`, `implement.jsonl`, and `check.jsonl` without turning PRD into old ceremony.
- Treats `prd.md` as the stage/value control plane, `design.md` as technical contracts and data flow, and `implement.md` as executable checklist plus validation gates.
- Adds Route Value Drift as a core research pitfall: correct artifacts do not automatically prove route value.
- Keeps `trellis channel` deferred as an optional 0.6 coordination primitive, not a default spec requirement.
- Preserves spec-only registry scope: optional scaffolder skill and logic-chain checker agent remain separate source assets, not `trellis init --registry` entries.

## 设计重点

- task-slot 贯穿 `tests/`、`scripts/`、`outputs/`、research ledger。
- Trellis 0.6 task artifacts 分层使用：`prd.md` 管 stage/value，`design.md` 管技术合同，`implement.md` 管执行与验证。
- Hydra 作为配置真源，禁止在正式入口堆 60 个 argparse 参数。
- 每次运行强制保存 config、git commit、git diff patch、命令、环境和日志。
- 数学公式、张量形状、数值稳定性、随机种子、数据 schema 都有可检查契约。
- Agent 不能只“继续调故事”；它必须维护失败证据、反对意见、失效结果和停止/继续决策。
- 人机协作按 T1/T2/T3 ownership 分层：AI 可执行，AI 可草拟，Human 必须决定。
