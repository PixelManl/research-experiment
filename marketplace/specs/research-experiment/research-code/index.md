# Research Code Index

本层规定科研代码本身：清晰、数学可审查、形状可追踪、数值稳定、随机性可复现。

| Topic | File | Status |
|---|---|---|
| Code style | `code-style.md` | Template |
| Math/formula mapping | `math-formula-mapping.md` | Template |
| Tensor shapes and typing | `tensor-shapes-typing.md` | Template |
| Validation/assertions | `validation-assertions.md` | Template |
| Numerical stability | `numerics.md` | Template |
| Data schema | `data-schema.md` | Template |
| Determinism | `determinism.md` | Template |
| Profiling | `profiling.md` | Template |

## Non-negotiable

- 先写直观正确的 torch 实现；性能优化要有 profile 证据。
- 公式实现必须能对应到论文/笔记中的公式编号。
- 跨模块传递数据必须用 dataclass/NamedTuple schema，不用裸 dict。
