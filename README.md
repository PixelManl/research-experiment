# Research-Experiment Trellis Spec Template v2

科研实验用 `.trellis/spec/` 模板。v2 保持瘦身，并补齐 **Hydra 配置、run 证据、tests/slot、route-value** 等硬规则。

## 核心

1. **Slot 组织** — scripts / runs / data / tests 同名；configs 推荐 `task/<slot>.yaml`。  
2. **main / plan / paper** — 1:1 实现；跑前只核 **短 baseline 表**，不重读整本 plan。  
3. **Hydra** — 正式入口必须；**yaml > arg**；default 只来自 yaml（代码勿手写第二套）。  
4. **Run 证据** — 最少集齐才可标 **runs 当前**（data 可多条在用）；废弃写原因；dirty 必有 patch。  
5. **algorithm / mc / diag / utils** — 干净算法 + fail-closed。  
6. **test 可 mock；smoke 真路径**。  
7. **Route-value** — 做完 ≠ 有价值。

## 安装

```bash
trellis init --registry gh:PixelManl/research-experiment/marketplace --template research-experiment-v2
```

务必带 `/marketplace`。装后：`python .trellis/scripts/get_context.py --mode packages`。

## 层

`organize` · `intent` · `linkage` · `code` · `guides` · `examples`（非合同）

可选 `marketplace/skills`、`agents` 不由 registry 安装；agent 已指向 v2 路径。
