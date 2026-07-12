# 脚手架布局参考（v2）

> **参考非合同。** 初始化空仓库或新 slot 时对照此树创建目录与空壳；算法逻辑自己写。  
> 包名用 `<package>`，任务槽用 `<task-slot>`，复制后替换。

## 整仓树

```text
<repo>/
├── src/<package>/
│   ├── __init__.py
│   ├── algorithm/              # 主算法（干净）
│   ├── metric/                 # mc.xx
│   ├── diag/                   # diag.xx
│   ├── utils/                  # safe_* 等
│   └── config/
│       └── cli.py              # 可选：显式覆盖；default 从 yaml 读
│
├── configs/                    # 正式入口必须 Hydra
│   ├── config.yaml
│   ├── task/
│   │   └── <task-slot>.yaml
│   ├── experiment/
│   │   └── default.yaml
│   ├── debug/
│   │   ├── off.yaml
│   │   ├── smoke.yaml          # 真路径小跑，非 mock
│   │   └── dry_run.yaml
│   └── hydra/
│       └── default.yaml        # run.dir → runs/...
│   # 可选：baseline.md         # 超参权威表（与 plan 表二选一）
│
├── scripts/
│   ├── index.md                # 可选总览
│   └── <task-slot>/
│       ├── index.md
│       └── run.py              # Hydra 入口（文件名可自定）
│
├── runs/
│   └── <task-slot>/
│       ├── index.md            # 当前/废弃（原因）；至多一个「当前」
│       └── <YYYY-MM-DD>/<HHMMSS>-<name>/
│           # 证据最少集：见 ../runs/run-dir-layout.md
│
├── data/
│   └── <task-slot>/
│       ├── index.md            # 来自哪个 run；可多条在用
│       └── …
│
├── tests/
│   ├── common/
│   └── <task-slot>/
│       ├── index.md
│       └── test_*.py           # 可 mock
│
├── docs/
│   ├── main/
│   │   └── main.md
│   └── plan/
│       ├── <task-slot>.md      # 可放唯一超参权威表 + 实现清单
│       └── modules/            # 可选
│           └── <module>/
│               └── PAPER.md
│
└── .trellis/spec/              # trellis init 安装的规范（含本 examples）
```

## 同一 slot 必须对齐

```text
scripts/<task-slot>/
runs/<task-slot>/
data/<task-slot>/
tests/<task-slot>/
configs/task/<task-slot>.yaml    # 推荐
docs/plan/<task-slot>.md         # 推荐
```

跨天：**不换 slot 名**；在 `runs/`（及可选 `scripts/`）下加 `YYYY-MM-DD/`。

## 初始化顺序（建议）

```text
1. trellis init … --template research-experiment-v2
2. 建 src/configs/scripts/runs/data/tests/docs 空树（本页）
3. 抄 index / plan 形状：
     examples/indexes/*
     examples/plan/slot-plan.md
4. 抄 Hydra 片段：examples/configs/snippets.md
5. 正式跑：证据形状 examples/runs/run-dir-layout.md
```

## 明确不要默认建的（v1 旧形）

- `outputs/` 当主产物树（v2 用 `runs/`）  
- 默认塞满 `docs/research-log/` 七件套（用 main + plan）  
- 默认 `configs/truth/` 双份巨型 yaml 仪式  
- 默认强制 `policy/runner`（需要 RL 时再加，非通用骨架）  
- 手写假「GENERATED」outputs index  

## 相关示例

| 要抄什么 | 路径 |
|----------|------|
| scripts index | [../indexes/scripts-index.md](../indexes/scripts-index.md) |
| runs 当前/废弃 | [../indexes/runs-index.md](../indexes/runs-index.md) |
| data 软链 | [../indexes/data-index.md](../indexes/data-index.md) |
| 单次 run 证据 | [../runs/run-dir-layout.md](../runs/run-dir-layout.md) |
| plan 表头 | [../plan/slot-plan.md](../plan/slot-plan.md) |
| Hydra 片段 | [../configs/snippets.md](../configs/snippets.md) |
| 代码分层调用 | [../code/call-shape.md](../code/call-shape.md) |
| 组件组 | [../linkage/COMPONENTS.md](../linkage/COMPONENTS.md) |
