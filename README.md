# Research-Experiment Trellis Spec Template v1.24

这是一个面向科研实验项目的 Trellis `.trellis/spec/` 模板。它不是可运行的科研代码项目，也不是默认脚手架生成器，而是一组让 AI 和人类共同遵守的研究工程规范。

## 安装前必读（避免装错）

本仓库的 **Git 根目录**就是本 README 所在目录，且必须满足：

```text
<repo-root>/
├── README.md
├── marketplace/
│   ├── index.json
│   ├── specs/research-experiment/   # 安装进 .trellis/spec/ 的内容
│   ├── skills/                      # 可选，registry 不会安装
│   └── agents/                      # 可选，registry 不会安装
```

| 字段 | 规则 |
|------|------|
| Registry source | 必须指向 **含 `index.json` 的目录**，即 `.../marketplace` |
| `index.json` 的 `path` | 相对 **Git 仓库根**，本模板为 `marketplace/specs/research-experiment` |
| `type` | 必须是 `"spec"`；skill/agent 不进 registry |
| 安装结果 | 模板目录内容直接落在 `.trellis/spec/`，不应出现 `.trellis/spec/spec/` |

### 正确命令

本仓库已发布为 `PixelManl/research-experiment` 时：

```bash
# Marketplace 模式：安装指定 template id
trellis init --registry gh:PixelManl/research-experiment/marketplace --template research-experiment

# 已有项目：只补缺失的 spec 文件
trellis init --registry gh:PixelManl/research-experiment/marketplace --template research-experiment --append

# 固定版本（推荐生产/论文复现）
trellis init --registry gh:PixelManl/research-experiment/marketplace#v1.24 --template research-experiment
```

若 fork 到自己的 org/repo，把上面的 `PixelManl/research-experiment` 换成你的 `org/repo` 即可。

### 错误用法（会导致“索引不到 / 装错内容”）

| 错误 | 会发生什么 |
|------|------------|
| `trellis init --registry gh:org/repo`（少了 `/marketplace`） | 根下没有 `index.json` → 走 **direct mode**，可能把整个仓库目录当 spec 拷进去 |
| `path` 写成 `specs/research-experiment`（相对 index 而不是仓库根） | marketplace 模式下载路径 404 / 模板 not found |
| 把 workspace 外层目录（例如嵌套的 `research-experiment-template-v0.1/` 包一层）当 Git 根发布 | `marketplace/index.json` 不在预期位置，registry 读不到 |
| 期望 `trellis init --registry` 安装 skill/agent | 当前只安装 `type: "spec"`；skill/agent 需手动复制 |
| 把 `examples/` 当可执行科研脚手架默认入口 | `examples/` 只是参考资产；见该层 `index.md` |

### 安装后自检

```bash
# 1) 层发现：应列出 coding layers + examples；guides 单独列出
python .trellis/scripts/get_context.py --mode packages

# 2) 每个被列出的 layer 都应有可读 index
#    特别确认：.trellis/spec/examples/index.md 存在
#    正式规则层：project-structure, experiment-runtime, research-code,
#    experiment-modules, research-pitfalls, agent-collaboration

# 3) 模板内容应在 .trellis/spec/ 下，而不是 .trellis/spec/spec/
```

期望的单仓层列表（CLI 扫描 `.trellis/spec/*/`，`guides` 除外但会单独引用）：

```text
agent-collaboration, examples, experiment-modules, experiment-runtime,
project-structure, research-code, research-pitfalls
+ shared guides: .trellis/spec/guides/index.md
```

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
└── examples/          # 参考资产；有 index.md，但不是 coding contract
```

## 安装方式 B：作为 Trellis 自定义 registry

见上文「正确命令」。要点再强调一次：

1. `--registry` 指向 `gh:<org>/<repo>/marketplace`（含 `index.json` 的 source path）
2. `index.json` 内 `path` 为仓库根相对路径 `marketplace/specs/research-experiment`
3. 用 `--template research-experiment` 匹配 `id`，不是文件夹名或 `name`

Trellis 0.6 会把 registry spec source 和 template id 写入 `.trellis/config.yaml`，后续可用 `trellis update` 走 hash / conflict / modified-by-you 流程刷新 `.trellis/spec/`。更新后仍要人工审查本项目对模板的本地改写，不要把源模板当成实时远程 wiki。

## 使用方式 C：可选脚手架参考

模板内的 `examples/bootstrap/bootstrap.py` 只是可选参考，用于说明如何按本 spec 生成一个初始科研项目目录。它不属于 Trellis spec 的核心规则；未来如果需要自动化脚手架，应作为独立 skill 设计，而不是混入 spec template 本体。

读 `examples/index.md` 了解参考文件清单；**不要**把 examples 路径写进正式任务的 `implement.jsonl` / `check.jsonl` 当作 coding contract。

## Spec index 约定（与 Trellis 技能对齐）

Trellis **运行时不会解析** `index.md` 章节标题（CLI 只扫层目录并列出 `.../index.md` 路径）。  
但官方 `before-dev` / `check` / `workflow.md` 会用**固定章节名**指示 Agent 去读：

| 章节 | 谁依赖 | 作用 |
|------|--------|------|
| **Guidelines Index** | 人类 + brainstorm | 文件表：path + 一句话 reason |
| **Pre-Development Checklist** | `before-dev` skill | 动手前该读哪些细则、完成哪些门禁 |
| **Quality Check** | `check` skill | 写完/改完后对照的验收项 |

本模板各层 `index.md` 按上述形态编写。细则正文在同目录其它 `.md` 中；index 只做发现面，不堆长规则。

`examples/` 是参考层：有 `index.md` 避免“层被扫到但文件不存在”，但不承担 Pre-Dev / Quality 编码门禁。

## Marketplace contents

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

## v1.24 更新重点

- README 明确正确/错误 registry 安装方式与安装后自检。
- 补全 `examples/index.md`，避免 CLI 层扫描指向不存在的 index。
- 各正式层 `index.md` 对齐作者约定：`Guidelines Index` + `Pre-Development Checklist` + `Quality Check`。
- 说明：章节名是 skill/prompt 软约束，不是 CLI 硬解析；为可靠触发仍采用官方标题。

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
