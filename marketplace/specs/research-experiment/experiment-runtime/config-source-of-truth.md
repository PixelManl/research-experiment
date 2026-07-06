# Configuration Source of Truth Contract

配置漂移是无声的研究杀手。当 agent 使用与 paper/作者不同的参数时，所有结果都不可信。

## 核心原则

**YAML 就是 truth 的表征，直接读取 yaml 就可以验证配置。**

## The Problem

```text
CRITICAL FAILURE MODE:
- Paper says: "only actor enabled"
- Original code: "critic + actor enabled"
- Agent runs: "critic + actor enabled" (copying code, not paper)
- Result: WRONG baseline comparison
- Impact: ALL downstream results INVALIDATED
```

## 配置结构

```text
configs/
├── config.yaml              # 主配置文件（头顶必须说明真源位置）
├── schema.py
├── task/
├── experiment/
├── debug/
├── hydra/
└── truth/
    ├── config.yaml          # 默认配置副本（真源，一般不修改）
    └── config_truth.md      # 配置内容说明文档（用于协商核对参数）
```

## configs/truth/config.yaml（真源）

这是默认配置的副本，是配置的真源。**一般不修改**。

头顶必须说明真源在哪里：

```yaml
# ============================================================
# CONFIG TRUTH - 配置真源
# ============================================================
# 这是默认配置的副本，是配置的真源。
# 一般不修改，除非真的确定要修改原作者的参数。
#
# 真源位置：
# - 作者原始代码配置：[链接到原作者代码/文档]
# - Paper 声称的实验配置：[链接到 paper]
#
# 验证规则：
# 1. 必须参数必须和 Paper 一致
# 2. 可选参数默认关闭
# 3. 修改原作者参数必须有明确理由
# ============================================================

# 必须参数（必须和 Paper 一致）
algorithm:
  actor: true
  critic: false  # Paper 说只开 actor
  entropy_bonus: true
  value_loss: false  # Paper 说只开 actor
  # 可选扩展（默认关闭）
  extra_module: false
  advanced_feature: false

training:
  batch_size: 256  # 必须和 paper 一致
  learning_rate: 3e-4  # 必须和 paper 一致
  gamma: 0.99  # 必须和 paper 一致
  gae_lambda: 0.95  # 必须和 paper 一致
  clip_epsilon: 0.2  # 必须和 paper 一致
  entropy_coef: 0.01  # 必须和 paper 一致
  value_coef: 0.0  # Paper 说只开 actor
  max_grad_norm: 0.5  # 必须和 paper 一致
  # 可选扩展（默认关闭）
  advanced_lr: false
  gradient_accumulation: false

environment:
  num_envs: 8  # 必须和 paper 一致
  num_steps: 128  # 必须和 paper 一致
  num_mini_batch: 4  # 必须和 paper 一致

# 验证参数
validation:
  # 是否真的修改了原作者的参数
  # 默认 false，必须真的确定要修改原作者的参数才可以 validate 通过
  modified_original: false

  # 修改理由（如果 modified_original 为 true，必须填写）
  modification_reason: ""

  # 修改日期
  modification_date: ""
```

## configs/truth/config_truth.md（配置内容说明文档）

这个文档用于和用户协商核对具体参数，并连接真源：

```markdown
# Config Truth - 配置真源

## 真源说明

本项目的配置真源是：
- 作者原始代码配置：[链接到原作者代码/文档]
- Paper 声称的实验配置：[链接到 paper]

## 参数核对表

### 必须和 Paper 一致的参数

| 参数 | Paper 值 | 当前值 | 是否一致 |
|---|---|---|---|
| algorithm.actor | true | true | ✅ |
| algorithm.critic | false | false | ✅ |
| training.batch_size | 256 | 256 | ✅ |
| ... | ... | ... | ... |

### 可选参数（默认关闭）

| 参数 | 说明 | 默认值 | 是否开启 |
|---|---|---|---|
| algorithm.extra_module | 额外模块 | false | ❌ |
| training.advanced_lr | 高级学习率调度 | false | ❌ |
| ... | ... | ... | ... |

## 验证规则

1. 必须参数必须和 Paper 一致
2. 可选参数默认关闭
3. 修改原作者参数必须有明确理由
```

## configs/config.yaml（主配置文件）

头顶必须说明真源在哪里：

```yaml
# ============================================================
# MAIN CONFIG - 主配置文件
# ============================================================
# 这是主配置文件，默认配置 = 原作者配置。
# 真源在 configs/truth/config.yaml
#
# 真源位置：
# - 作者原始代码配置：[链接到原作者代码/文档]
# - Paper 声称的实验配置：[链接到 paper]
#
# 验证规则：
# 1. 必须参数必须和 Paper 一致
# 2. 可选参数默认关闭
# 3. 修改原作者参数必须有明确理由
# ============================================================

# 必须参数（必须和 Paper 一致）
algorithm:
  actor: true
  critic: false  # Paper 说只开 actor
  entropy_bonus: true
  value_loss: false  # Paper 说只开 actor
  # 可选扩展（默认关闭）
  extra_module: false
  advanced_feature: false

training:
  batch_size: 256  # 必须和 paper 一致
  learning_rate: 3e-4  # 必须和 paper 一致
  gamma: 0.99  # 必须和 paper 一致
  gae_lambda: 0.95  # 必须和 paper 一致
  clip_epsilon: 0.2  # 必须和 paper 一致
  entropy_coef: 0.01  # 必须和 paper 一致
  value_coef: 0.0  # Paper 说只开 actor
  max_grad_norm: 0.5  # 必须和 paper 一致
  # 可选扩展（默认关闭）
  advanced_lr: false
  gradient_accumulation: false

environment:
  num_envs: 8  # 必须和 paper 一致
  num_steps: 128  # 必须和 paper 一致
  num_mini_batch: 4  # 必须和 paper 一致

# 验证参数
validation:
  # 是否真的修改了原作者的参数
  # 默认 false，必须真的确定要修改原作者的参数才可以 validate 通过
  modified_original: false

  # 修改理由（如果 modified_original 为 true，必须填写）
  modification_reason: ""

  # 修改日期
  modification_date: ""
```

## 验证逻辑

**不需要写复杂脚本**，直接读取 yaml 文件进行对比：

```python
import yaml

def validate_config(config_path):
    with open(config_path) as f:
        config = yaml.safe_load(f)

    # 检查验证参数
    validation = config.get('validation', {})
    modified_original = validation.get('modified_original', False)
    modification_reason = validation.get('modification_reason', '')

    if modified_original and not modification_reason:
        print("ERROR: 修改了原作者参数但没有填写理由")
        return False

    # 对比必须参数和 Paper 一致
    # ... 对比逻辑

    return True
```

## 默认关闭的正确理解

- **默认配置 = 原作者配置** - 这是基础
- **自己添加的更多配置，默认关闭** - 这是关键
- 需要开启时，必须有明确理由

## AGENT BEHAVIOR RULES

### What Agent MUST Do

1. **ALWAYS** 读取 configs/truth/config.yaml 了解真源
2. **ALWAYS** 使用项目正式入口的 `configs/config.yaml`，并在正式实验前核对 `configs/truth/config.yaml`
3. **ALWAYS** 记录任何配置偏差
4. **ALWAYS** 在修改关键参数前询问人类
5. **NEVER** 假设配置正确而不验证

### What Agent MUST NOT Do

1. **NEVER** 使用未验证的配置运行实验
2. **NEVER** 未经人类批准修改 configs/truth/config.yaml
3. **NEVER** 假设"这只是小改动" - 所有改动都需要验证
4. **NEVER** 跳过验证进行"快速测试" - 所有测试都需要验证

## EMERGENCY PROCEDURES

### If Config Drift Detected

If you discover config drift (wrong parameters used):

1. **STOP** all running experiments immediately
2. **INVALIDATE** all results from wrong config
3. **LOG** the drift in `docs/research-log/invalidated-results.md`
4. **FIX** the config to match truth
5. **RE-RUN** all affected experiments
6. **UPDATE** the truth files if paper was wrong

## SUMMARY

**THE GOLDEN RULE**:

```text
IF config doesn't match configs/truth/config.yaml
AND human hasn't explicitly approved the change
THEN DON'T RUN THE EXPERIMENT
```

This is not a suggestion. This is a **MANDATORY REQUIREMENT**.

Violations of this contract will result in:
- All results from wrong config becoming INVALID
- Wasted compute time
- Untrustworthy research conclusions
- Potential paper retraction

**VALIDATE BEFORE YOU CALCULATE.**
