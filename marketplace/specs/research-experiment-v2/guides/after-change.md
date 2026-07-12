# 改完 / 修 bug 后

## 1. 对照 plan 实现清单

- 清单项是否 1:1 勾完？有无未写入的「顺手改」？  
- （不必重读整篇 plan 叙述，勾清单即可。）

## 2. 联动

- 组件组是否半更新？相关 tests 是否过？

## 3. 结果链 + 证据

- 新 run 在 `runs/<slot>/<日期>/...`，**证据齐全**（git、配置、command、seed）。  
- `index.md`：旧 → **废弃 + 原因**；新 → **当前**（仅证据齐时）。  
- data 下游按废弃链清理。  
- **图与结论只引当前**；禁止「见某日期文件夹」。

## 4. 声明语言（短）

| 级别 | 含义 |
|------|------|
| observation | 看见了什么 |
| hypothesis | 猜测 |
| evidence | 有当前 run 证据支撑 |
| claim | 对外/论文叙事；人确认 |

证据与叙事冲突、cheap 诊断已杀假设、只会扫参掩盖弱设定 → **应喊停/reframe**，勿硬编故事。

## 5. 防复发

修完问：怎样让同类不再发生？

→ 补 `tests/<slot>` / plan 一条 / linkage 组件 / utils 安全算子 / baseline 表。

## 6. index 仍短

scripts / runs / data / tests 的 index 是否仍一屏内？

## 7. main

仅目标变了才改 main；过程留 plan 与 runs index。
