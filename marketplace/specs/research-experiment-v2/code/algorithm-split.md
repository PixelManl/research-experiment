# Algorithm / Metric / Diag / Utils 分层

## 一句话

**algorithm 只写主算法，保持干净；统计进 metric；诊断进 diag；有数值风险的算子从 utils 拿安全实现做替换。**

## 推荐布局（包内）

名称可按项目微调，职责不要混：

```text
src/<package>/
├── algorithm/          # 或 algo/：主算法、更新规则、前向与中间量
├── metric/             # 统计指标；对外 mc.xx 或 metric.xx
├── diag/               # 诊断探针；对外 diag.xx
└── utils/              # 安全数值、通用小工具（含 safe_div 等）
```

脚本仍在 `scripts/<task-slot>/`：只编排配置、调用 algorithm、再调 metric/diag、写 runs。

## 1. algorithm — 只要主算法干净

**负责：**

- 论文/plan 中的核心计算（policy、loss、update、rollout 机制等）；
- 产出**中间产物**（tensor、dict、dataclass），供后续统计/诊断。

**不负责：**

- 复杂统计汇总、claim 用指标表；
- 健康检查、可视化探针、冗长 debug 打印逻辑；
- 到处手写 `+ 1e-8` 掩盖数值问题（应走 utils 替换）。

额外内容放哪？→ **metric**（要记的数）、**diag**（要查的健康/形状）、**utils**（可复用安全算子）、**scripts**（IO 与编排）。

## 2. metric — 统计只在这里

- algorithm **不**内嵌大段 metric 公式。
- algorithm 提供中间产物后，调用方（script 或薄封装）使用：

```text
mc.xxx(...)     # 或 metric.xxx(...)
```

- metric 模块：**输入中间产物 → 输出可记录的标量/表**；不拥有训练步进，不写算法状态机。

## 3. diag — 诊断与 metric 同构

- 诊断逻辑进 `diag/`，不要堆进 algorithm 主干。
- 调用形态与 metric 对称：

```text
diag.xxx(...)
```

- 输入具体内容（batch、logits、mask、中间产物）→ 计算诊断结果。
- 昂贵诊断由 script/config 开关，默认不污染主路径。

## 4. utils — 安全算子，替换式使用

任何 **torch 上有 0 梯度 / NaN / 除零风险** 的计算，从 utils 取安全实现，**替换** algorithm 中的裸写法，而不是让 algorithm 正文堆满防护噪音。

| 场景 | 不要 | 要 |
|------|------|-----|
| 除法 | `a / b` 随处 + 注释 | `utils.safe_div(a, b, eps=...)` |
| log-softmax | `log(softmax(x))` | `utils.safe_log_softmax` 或等价 |
| 标准差归一化 | `/ std` 无下限 | `utils.normalize_*(..., eps=...)` |

原则：

- **算法可读性优先**：主公式仍像公式；安全细节在 utils。
- **替换不是拦截**：不是包一层「禁止 algorithm 做除法」，而是统一安全原语，algorithm 直接换调用。
- 新安全原语加在 utils，并尽量有单测；algorithm 禁止再复制一份 eps 逻辑。

## 调用关系（示意）

```text
script
  → algorithm.step(...)           # 干净主算法，返回 intermediates
  → mc.summary(intermediates)     # 统计
  → diag.health(intermediates)    # 诊断（可选）
  → 写入 runs/<slot>/...
```

algorithm 内部需要除法/归一化时：

```text
algorithm  →  utils.safe_*  （替换裸算子）
algorithm  ✗ metric / diag 的大段逻辑
```

## 与 linkage

clip、entropy 等仍属 **algorithm 组件组**（见 linkage）。  
metric/diag 若依赖旧语义字段，语义变更后要同步改调用或废弃旧 runs/data。

## Agent 禁令

- 禁止在 algorithm 里越写越长的「顺便算个 mean/std/直方图」。
- 禁止 metric 反写训练状态机。
- 禁止在 algorithm 多处复制 `eps` 除法而不进 utils。
