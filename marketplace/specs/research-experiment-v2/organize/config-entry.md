# 配置入口：必须 Hydra + yaml > arg

## 一句话

**正式实验必须用 Hydra 管理配置；CLI 覆盖不得靠「错误的 argparse 默认值」偷跑；yaml 为底，arg 只做显式覆盖。**

## 强制 Hydra

- 正式训练/评估入口：`@hydra.main` 或项目统一的 Hydra 启动封装。  
- **禁止**用越来越长的 `argparse` 拼正式实验。  
- Hydra 输出目录应落在 `runs/<task-slot>/...`（或与之等价并在 run 证据中可找到 `.hydra/`）。

推荐形状：

```text
configs/
  config.yaml              # 主入口 defaults
  schema.py                # 可选 structured config
  task/
    <task-slot>.yaml       # 按 slot 拆分（推荐，configs 也会大量改）
  experiment/
  debug/
    smoke.yaml
    dry_run.yaml
    off.yaml
  hydra/
    default.yaml           # run.dir → runs/${task.slot}/...
```

### configs 与 task-slot

configs **会频繁改**，推荐与 slot 对齐，避免所有任务挤一个巨大 yaml：

| 做法 | 说明 |
|------|------|
| `configs/task/<slot>.yaml` | 推荐；defaults 里 `- task: <slot>` |
| `configs/experiment/<name>.yaml` | 消融/设定变体 |
| 共用段 | `configs/model/`、`configs/train/` 等，被 task 引用 |

**不要**为每个日期复制一份 slot 配置；变体用 experiment 组或 run 时显式 override。

## yaml > arg（铁律）

1. **真实默认值写在 yaml**，不写在 Python 函数签名里当「第二套默认」。  
2. CLI / `argparse` **仅用于**：  
   - 显式覆盖（用户知道自己在改）；或  
   - 与 Hydra 组合时由 Hydra 解析的 override（`key=value`）。  
3. 若仍保留独立 arg 定义文件：  

```text
src/<package>/config/args.py   # 或 configs/cli_schema — 独立抽取
# 禁止把一大坨 parser 埋在 algorithm/ 或 run 训练主循环里
```

4. **arg 的 default 必须与对应 yaml 一致**；不一致视为 bug。优先：**default 从 yaml/OmegaConf 读出**，而不是手写两遍。  
5. 合并优先级（概念上）：

```text
yaml 底稿  <  显式 Hydra override / 显式 CLI
禁止：静默的「代码 default 盖过 yaml」
```

6. 未知键：正式模式 **失败**（struct / schema），不要吞掉。

## debug 组

| 组 | 用途 |
|----|------|
| `debug=smoke` | **真路径**极小步数/batch，写出正常 run 目录；**不是** unit test mock |
| `debug=dry_run` | 只验配置/路径/seed/入口，可不跑满训练 |
| `debug=off` | 正式 |

test 可以 mock；**smoke 必须走真实入口与真实配置链路**。

## 与证据包

- Hydra 写入 run 目录的 `.hydra/config.yaml` = 本次配置证据（见 [run-evidence.md](./run-evidence.md)）。  
- `command.txt` 记录完整启动行（含 overrides）。

## Agent 禁令

- 禁止在 algorithm 内堆 argparse 默认超参。  
- 禁止 yaml 一套、函数 default 另一套。  
- 禁止用 mock 测试代替 smoke。
