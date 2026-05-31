import argparse
import os
from pathlib import Path

def create_scaffold(package_name: str, task_slot: str):
    root = Path.cwd()
    
    print(f"🚀 初始化科研项目脚手架...")
    print(f"📦 包名 (Package): {package_name}")
    print(f"🎯 初始任务槽 (Task-slot): {task_slot}")
    
    # 1. src-layout
    src_dir = root / "src" / package_name
    src_dir.mkdir(parents=True, exist_ok=True)
    (src_dir / "__init__.py").touch()
    
    for d in ["policy", "runner"]:
        (src_dir / d).mkdir(parents=True, exist_ok=True)
        (src_dir / d / "__init__.py").touch()
    
    for mod in ["metrics.py", "diagnostics.py", "numerics.py", "schema.py", "validate.py", "plotting.py", "provenance.py"]:
        (src_dir / mod).touch()
        
    # 2. Configs
    configs_dir = root / "configs"
    for sub in ["task", "experiment", "debug", "hydra"]:
        (configs_dir / sub).mkdir(parents=True, exist_ok=True)
    
    # 生成基础 hydra 配置占位
    (configs_dir / "config.yaml").write_text(f"defaults:\n  - task: {task_slot}\n  - experiment: default\n  - debug: off\n  - _self_\n")
    (configs_dir / "schema.py").write_text("# dataclass / structured config roots\n")
    
    # 3. Task slots directories
    for p in ["scripts", "tests", "outputs"]:
        task_dir = root / p / task_slot
        task_dir.mkdir(parents=True, exist_ok=True)
        (task_dir / "index.md").write_text(f"# {p.capitalize()} Index for {task_slot}\n")
        
    # 4. Data
    (root / "data" / "processed").mkdir(parents=True, exist_ok=True)
    
    # 5. Docs & Research Log
    main_dir = root / "docs" / "main"
    main_dir.mkdir(parents=True, exist_ok=True)
    (main_dir / "main.md").write_text("# 实验主日志 (Main Journal)\n\n## YYYY-MM-DD — 项目初始化\n\n### 实验叙事\n项目骨架建立，准备进行基线测试。\n")
    
    log_dir = root / "docs" / "research-log"
    log_dir.mkdir(parents=True, exist_ok=True)
    
    for md in ["index.md", "baselines.md", "source-of-truth.md", "invalidated-results.md", "reviewer-objections.md"]:
        (log_dir / md).touch()
        
    for sub in ["decisions", "tasks", "reports", "equation-maps"]:
        (log_dir / sub).mkdir(parents=True, exist_ok=True)
        
    (log_dir / "tasks" / f"{task_slot}.md").write_text(f"# Task Ledger: {task_slot}\n")

    print(f"✅ 脚手架生成完毕！请运行 `pip install -e .` (如果有 pyproject.toml) 来安装包。")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Bootstrap Research-Experiment Scaffold")
    parser.add_argument("--package", required=True, help="真实的 Python 包名 (如 zero_ucar)")
    parser.add_argument("--task-slot", required=True, help="初始的实验任务槽名 (如 default_env_test)")
    args = parser.parse_args()
    
    create_scaffold(args.package, args.task_slot)
