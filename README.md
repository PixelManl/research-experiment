# Research-Experiment Trellis Spec Template v2

面向科研实验的 Trellis `.trellis/spec/` 模板。  
**v2 只保留四条职责**（旧 v1 多层 runtime/T1T2T3 等已弃用，见 git 历史）。

## 四条职责

1. **组织** — `<task-slot>` 对齐 `scripts` / `runs` / `data`，短 `index.md`；跨天用日期子目录。  
2. **意图** — `docs/main` 要什么；`docs/plan` 怎么做；模块旁 **paper 原文 .md** → 抽取 → **1:1 实现**。  
3. **链路** — 组件组联动（如 hard-clip + entropy）；Grep/MCP 可选。  
4. **真源表** — 查 main / plan / 三级 index；**runs ≠ data**，data 软链 run，错误链路从坏点下游清理。

## 安装（务必带 `/marketplace`）

```bash
trellis init --registry gh:PixelManl/research-experiment/marketplace --template research-experiment-v2
```

| 正确 | 错误 |
|------|------|
| `.../marketplace` + `--template research-experiment-v2` | 省略 `/marketplace`（易进 direct mode） |
| `path` 相对仓库根：`marketplace/specs/research-experiment-v2` | 把 path 写成相对 index.json 的 `specs/...` |

安装后自检：

```bash
python .trellis/scripts/get_context.py --mode packages
# 应看到层：organize, intent, linkage, examples（guides 单独）
```

### 直接复制

把 `marketplace/specs/research-experiment-v2/` 内容拷到目标项目 `.trellis/spec/`。

## 仓库里还有什么

```text
marketplace/
├── index.json
├── specs/research-experiment-v2/   # 本模板
├── skills/                         # 可选；registry 不安装
└── agents/                         # 可选；registry 不安装
```

## 与 v1

- 旧 id `research-experiment` 已移除；请用 **`research-experiment-v2`**。  
- 旧 outputs/Hydra/registry 双轴等长文不再作为核心；需要可从 git 历史找回参考。  
- 设计哲学压成 README 四句 + 四职责，避免概念串不起来。
