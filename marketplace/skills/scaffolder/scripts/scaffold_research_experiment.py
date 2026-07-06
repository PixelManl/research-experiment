#!/usr/bin/env python
from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path


TASK_SLOT_RE = re.compile(r"^[a-z0-9][a-z0-9-]*[a-z0-9]$|^[a-z0-9]$")
PACKAGE_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
SHARED_TEST_DIRS = {"common", "contracts", "smoke", "__pycache__"}


@dataclass(frozen=True)
class PlannedFile:
    path: Path
    content: str


def rel(path: Path) -> str:
    return str(path).replace("\\", "/")


def validate_task_slot(task_slot: str) -> None:
    if not TASK_SLOT_RE.match(task_slot):
        raise SystemExit(
            f"Invalid task-slot {task_slot!r}. Use lowercase letters, digits, and hyphens; do not include dates."
        )


def validate_package(package: str) -> None:
    if not PACKAGE_RE.match(package):
        raise SystemExit(f"Invalid package name {package!r}. Use a valid Python identifier.")


def read_pyproject_name(root: Path) -> str | None:
    pyproject = root / "pyproject.toml"
    if not pyproject.exists():
        return None
    for line in pyproject.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = line.strip()
        if line.startswith("name") and "=" in line:
            value = line.split("=", 1)[1].strip().strip('"').strip("'")
            candidate = value.replace("-", "_")
            if PACKAGE_RE.match(candidate):
                return candidate
    return None


def infer_package(root: Path) -> str | None:
    from_pyproject = read_pyproject_name(root)
    if from_pyproject:
        return from_pyproject
    src = root / "src"
    if src.exists():
        packages = [p.name for p in src.iterdir() if p.is_dir() and (p / "__init__.py").exists()]
        if len(packages) == 1:
            return packages[0]
    return None


def list_dirs(root: Path, name: str) -> set[str]:
    directory = root / name
    if not directory.exists():
        return set()
    return {p.name for p in directory.iterdir() if p.is_dir()}


def list_task_files(root: Path) -> set[str]:
    directory = root / "docs" / "research-log" / "tasks"
    if not directory.exists():
        return set()
    return {p.stem for p in directory.glob("*.md")}


def list_task_config_files(root: Path) -> set[str]:
    directory = root / "configs" / "task"
    if not directory.exists():
        return set()
    return {p.stem for p in directory.glob("*.yaml")}


def list_output_task_dirs(root: Path) -> tuple[set[str], set[str]]:
    directory = root / "outputs"
    if not directory.exists():
        return set(), set()
    task_dirs = set()
    output_only = set()
    for p in directory.iterdir():
        if not p.is_dir():
            continue
        if (p / "runs.jsonl").exists() or (p / "index.md").exists():
            task_dirs.add(p.name)
        else:
            output_only.add(p.name)
    return task_dirs, output_only


def audit(root: Path) -> dict:
    package = infer_package(root)
    tests = list_dirs(root, "tests")
    scripts = list_dirs(root, "scripts")
    outputs, output_only_areas = list_output_task_dirs(root)
    config_tasks = list_task_config_files(root)
    ledgers = list_task_files(root)
    candidates = sorted((tests | scripts | outputs | config_tasks | ledgers) - SHARED_TEST_DIRS)
    task_slots = []
    for slot in candidates:
        task_slots.append(
            {
                "task_slot": slot,
                "configs_task": slot in config_tasks,
                "tests": slot in tests,
                "scripts": slot in scripts,
                "outputs": slot in outputs,
                "task_ledger": slot in ledgers,
            }
        )
    warnings = []
    if not (root / ".trellis" / "spec" / "README.md").exists():
        warnings.append("No .trellis/spec/README.md found.")
    if not package:
        warnings.append("Package name could not be inferred.")
    for item in task_slots:
        missing = [k for k, v in item.items() if k not in {"task_slot", "outputs"} and not v]
        if missing:
            warnings.append(f"Task-slot {item['task_slot']} is not fully aligned: missing {', '.join(missing)}.")
    has_config_truth = (root / "configs" / "truth" / "config.yaml").exists() and (
        root / "configs" / "truth" / "config_truth.md"
    ).exists()
    if (root / "configs" / "config.yaml").exists() and not has_config_truth:
        warnings.append("Hydra config exists but configs/truth/config.yaml and config_truth.md are not both present.")
    return {
        "root": str(root),
        "package": package,
        "has_trellis_spec": (root / ".trellis" / "spec" / "README.md").exists(),
        "has_hydra_config": (root / "configs" / "config.yaml").exists(),
        "has_config_truth": has_config_truth,
        "shared_test_dirs": sorted(tests & SHARED_TEST_DIRS),
        "task_slots": task_slots,
        "output_only_areas": sorted(output_only_areas),
        "warnings": warnings,
    }


def default_config_content(task_slot: str, *, truth: bool = False) -> str:
    if truth:
        header = "# CONFIG TRUTH\n# Baseline default config. Edit only with explicit human approval."
    else:
        header = "# MAIN CONFIG\n# Truth baseline: configs/truth/config.yaml\n# Validate this file against the truth baseline before formal runs."
    return f"""{header}
defaults:
  - task: {task_slot}
  - experiment: default
  - debug: off
  - _self_

run:
  name: default
  seed: 0

validation:
  modified_original: false
  modification_reason: ""
  modification_date: ""
"""


def config_truth_doc_content(task_slot: str) -> str:
    return f"""# Config Truth

Task slot: `{task_slot}`

## Source References

| Source | Link / Path | Notes |
|---|---|---|
| Original code config | TBD | Fill before formal experiments |
| Paper / report config | TBD | Fill before formal experiments |

## Required Parameter Check

| Parameter | Source value | Current value | Status |
|---|---|---|---|
| `task.slot` | `{task_slot}` | `{task_slot}` | pending source confirmation |
| `run.seed` | `0` | `0` | pending source confirmation |

## Optional Extensions

Optional project-added features must default off until explicitly approved.
"""


def base_project_files(package: str, task_slot: str) -> list[PlannedFile]:
    return [
        PlannedFile(Path(f"src/{package}/__init__.py"), ""),
        PlannedFile(Path(f"src/{package}/config/__init__.py"), ""),
        PlannedFile(
            Path(f"src/{package}/config/schema.py"),
            "from __future__ import annotations\n\n# Packaged structured config schema.\n",
        ),
        PlannedFile(Path(f"src/{package}/runner/__init__.py"), ""),
        PlannedFile(Path(f"src/{package}/policy/__init__.py"), ""),
        PlannedFile(Path("configs/config.yaml"), default_config_content(task_slot)),
        PlannedFile(Path("configs/truth/config.yaml"), default_config_content(task_slot, truth=True)),
        PlannedFile(Path("configs/truth/config_truth.md"), config_truth_doc_content(task_slot)),
        PlannedFile(
            Path("configs/schema.py"),
            "from __future__ import annotations\n\n# Compatibility import or structured Hydra config roots.\n",
        ),
        PlannedFile(Path("configs/experiment/default.yaml"), "experiment:\n  name: default\n"),
        PlannedFile(Path("configs/debug/off.yaml"), "debug:\n  enabled: false\n  mode: off\n"),
        PlannedFile(
            Path("configs/debug/smoke.yaml"),
            "debug:\n  enabled: true\n  mode: smoke\n  max_steps: 2\nrun:\n  name: smoke\n",
        ),
        PlannedFile(Path("configs/debug/dry_run.yaml"), "debug:\n  enabled: true\n  mode: dry_run\nrun:\n  name: dry-run\n"),
        PlannedFile(
            Path("configs/hydra/default.yaml"),
            "hydra:\n  run:\n    dir: outputs/${task.slot}/${now:%Y-%m-%d}/${now:%H%M%S}-${run.name}\n  job:\n    chdir: false\n",
        ),
        PlannedFile(
            Path("tests/index.md"),
            "# Tests Index\n\n| Area / Task slot | Required command | Scope | Status |\n|---|---|---|---|\n",
        ),
        PlannedFile(Path("scripts/index.md"), "# Scripts Index\n\n| Area / Task slot | Entry | Purpose | Status |\n|---|---|---|---|\n"),
        PlannedFile(
            Path("outputs/index.md"),
            "# Outputs\n\n<!-- GENERATED by scripts/common/runs.py render - DO NOT EDIT BY HAND -->\n\n| Task slot | Canonical | Validity | Runs | Last activity |\n|---|---|---|---|---|\n",
        ),
        PlannedFile(
            Path("docs/main/main.md"),
            "# Main Journal\n\n## YYYY-MM-DD - Project initialized\n\n### Research narrative\n\nScaffold created.\n",
        ),
        PlannedFile(
            Path("docs/research-log/index.md"),
            "# Research Log\n\n| File | Purpose |\n|---|---|\n| `source-of-truth.md` | durable facts |\n| `invalidated-results.md` | invalidated outputs |\n",
        ),
        PlannedFile(Path("docs/research-log/baselines.md"), "# Baselines\n\n| Baseline | Source | Status | Notes |\n|---|---|---|---|\n"),
        PlannedFile(Path("docs/research-log/source-of-truth.md"), "# Source of Truth\n\n"),
        PlannedFile(Path("docs/research-log/invalidated-results.md"), "# Invalidated Results\n\n"),
        PlannedFile(Path("docs/research-log/reviewer-objections.md"), "# Reviewer Objections\n\n"),
    ]


def task_slot_files(task_slot: str, package: str | None, entrypoint: str | None, test_command: str | None) -> list[PlannedFile]:
    validate_task_slot(task_slot)
    entry = entrypoint or (f"python -m {package}.main debug=smoke" if package else "TBD")
    tests = test_command or f"python -m pytest tests/{task_slot} -q"
    return [
        PlannedFile(Path(f"configs/task/{task_slot}.yaml"), f"task:\n  slot: {task_slot}\n"),
        PlannedFile(
            Path(f"tests/{task_slot}/index.md"),
            f"# {task_slot} Tests\n\nCanonical command:\n\n```bash\n{tests}\n```\n\n| File | Invariant checked | Delete/promote rule |\n|---|---|---|\n",
        ),
        PlannedFile(
            Path(f"scripts/{task_slot}/index.md"),
            f"# {task_slot} Scripts\n\nCanonical entrypoint:\n\n```bash\n{entry}\n```\n\n| Script / command | Purpose | Status |\n|---|---|---|\n",
        ),
        PlannedFile(
            Path(f"docs/research-log/tasks/{task_slot}.md"),
            f"# {task_slot}\n\nPurpose: TBD.\n\nCanonical test command:\n\n```bash\n{tests}\n```\n\nCanonical run command:\n\n```bash\n{entry}\n```\n\nRun registry: created by first registered run under `outputs/{task_slot}/runs.jsonl`.\n\n## Status\n\nactive scaffold\n\n## Human review needed\n\n- Confirm purpose.\n- Confirm metric, baseline, formula, and heavy-run decisions before real experiments.\n",
        ),
    ]


def required_dirs(files: list[PlannedFile]) -> list[Path]:
    dirs = {f.path.parent for f in files if str(f.path.parent) != "."}
    return sorted(dirs, key=lambda p: rel(p))


def build_plan(root: Path, files: list[PlannedFile], force: bool) -> dict[str, list[str]]:
    plan = {"create_dirs": [], "create_files": [], "overwrite_files": [], "skip_files": []}
    for directory in required_dirs(files):
        if not (root / directory).exists():
            plan["create_dirs"].append(rel(directory))
    for item in files:
        target = root / item.path
        name = rel(item.path)
        if target.exists():
            if force:
                plan["overwrite_files"].append(name)
            else:
                plan["skip_files"].append(name)
        else:
            plan["create_files"].append(name)
    return plan


def apply_files(root: Path, files: list[PlannedFile], force: bool) -> None:
    for item in files:
        target = root / item.path
        if target.exists() and not force:
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(item.content, encoding="utf-8", newline="\n")


def emit_and_maybe_apply(root: Path, command: str, files: list[PlannedFile], apply: bool, force: bool, extra: dict | None = None) -> None:
    plan = build_plan(root, files, force)
    result = {"root": str(root), "command": command, "mode": "apply" if apply else "dry-run", "plan": plan}
    if extra:
        result.update(extra)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    if apply:
        apply_files(root, files, force)


def resolve_root(value: str) -> Path:
    root = Path(value).resolve()
    if not root.exists():
        raise SystemExit(f"Root does not exist: {root}")
    return root


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit and scaffold Research-Experiment project skeletons.")
    sub = parser.add_subparsers(dest="command", required=True)

    audit_cmd = sub.add_parser("audit", help="Inspect project structure without writing files.")
    audit_cmd.add_argument("--root", default=".")

    init_cmd = sub.add_parser("init-project", help="Create a conservative base project skeleton.")
    init_cmd.add_argument("--root", default=".")
    init_cmd.add_argument("--package", required=True)
    init_cmd.add_argument("--task-slot", required=True)
    init_cmd.add_argument("--entrypoint")
    init_cmd.add_argument("--test-command")
    init_cmd.add_argument("--apply", action="store_true")
    init_cmd.add_argument("--force", action="store_true")

    task_cmd = sub.add_parser("add-task", help="Add task-slot aligned config/tests/scripts/outputs/ledger files.")
    task_cmd.add_argument("--root", default=".")
    task_cmd.add_argument("--task-slot", required=True)
    task_cmd.add_argument("--package")
    task_cmd.add_argument("--entrypoint")
    task_cmd.add_argument("--test-command")
    task_cmd.add_argument("--apply", action="store_true")
    task_cmd.add_argument("--force", action="store_true")

    args = parser.parse_args()
    root = resolve_root(args.root)

    if args.command == "audit":
        print(json.dumps(audit(root), indent=2, ensure_ascii=False))
        return

    if args.command == "init-project":
        validate_package(args.package)
        validate_task_slot(args.task_slot)
        files = base_project_files(args.package, args.task_slot) + task_slot_files(
            args.task_slot, args.package, args.entrypoint, args.test_command
        )
        emit_and_maybe_apply(root, args.command, files, args.apply, args.force, {"package": args.package, "task_slot": args.task_slot})
        return

    if args.command == "add-task":
        package = args.package or infer_package(root)
        files = task_slot_files(args.task_slot, package, args.entrypoint, args.test_command)
        emit_and_maybe_apply(root, args.command, files, args.apply, args.force, {"package": package, "task_slot": args.task_slot})
        return


if __name__ == "__main__":
    main()
