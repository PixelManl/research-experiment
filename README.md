# Research-Experiment Trellis Spec Template v0.1

这是一个面向科研实验项目的 Trellis `.trellis/spec/` 模板。它不是代码脚手架，而是一组让 AI 和人类共同遵守的研究工程规范。

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
└── guides/
```

## 安装方式 B：作为 Trellis 自定义 registry

把整个仓库发布到 GitHub/GitLab/Bitbucket 后，可用：

```bash
trellis init --registry gh:<org>/<repo>/marketplace --template research-experiment
```

## 设计重点

- task-slot 贯穿 `tests/`、`scripts/`、`outputs/`、research ledger。
- Hydra 作为配置真源，禁止在正式入口堆 60 个 argparse 参数。
- 每次运行强制保存 config、git commit、git diff patch、命令、环境和日志。
- 数学公式、张量形状、数值稳定性、随机种子、数据 schema 都有可检查契约。
- Agent 不能只“继续调故事”；它必须维护失败证据、反对意见、失效结果和停止/继续决策。
- 人机协作按 T1/T2/T3 ownership 分层：AI 可执行，AI 可草拟，Human 必须决定。
