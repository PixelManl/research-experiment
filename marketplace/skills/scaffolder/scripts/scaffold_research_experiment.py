#!/usr/bin/env python3
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
        if (p / "index.md").exists():
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
        missing = [k for k, v in item.items() if k != "task_slot" and not v]
        if missing:
            warnings.append(f"Task-slot {item['task_slot']} is not fully aligned: missing {', '.join(missing)}.")
    return {
        "root": str(root),
        "package": package,
        "has_trellis_spec": (root / ".trellis" / "spec" / "README.md").exists(),
        "has_hydra_config": (root / "configs" / "config.yaml").exists(),
        "shared_test_dirs": sorted(tests & SHARED_TEST_DIRS),
        "task_slots": task_slots,
        "output_only_areas": sorted(output_only_areas),
        "warnings": warnings,
    }


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
        PlannedFile(
            Path("configs/config.yaml"),
            f"defaults:\n  - task: {task_slot}\n  - experiment: default\n  - debug: off\n  - _self_\n\nseed: 0\n",
        ),
        PlannedFile(
            Path("configs/schema.py"),
            "from __future__ import annotations\n\n# Compatibility import or structured Hydra config roots.\n",
        ),
        PlannedFile(Path("configs/experiment/default.yaml"), "name: default\n"),
        PlannedFile(Path("configs/debug/off.yaml"), "enabled: false\nmode: off\n"),
        PlannedFile(Path("configs/debug/smoke.yaml"), "enabled: true\nmode: smoke\nmax_steps: 2\n"),
        PlannedFile(Path("configs/debug/dry_run.yaml"), "enabled: true\nmode: dry_run\n"),
        PlannedFile(
            Path("tests/index.md"),
            "# Tests Index\n\n| Area / Task slot | Required command | Scope | Status |\n|---|---|---|---|\n",
        ),
        PlannedFile(Path("scripts/index.md"), "# Scripts Index\n\n| Area / Task slot | Entry | Purpose | Status |\n|---|---|---|---|\n"),
        PlannedFile(Path("outputs/index.md"), "# Outputs Index\n\n| Task slot | Latest valid run | Status | Notes |\n|---|---|---|---|\n"),
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
    entry = entrypoint or (f"PYTHONPATH=src python -m {package}.main debug=smoke" if package else "TBD")
    tests = test_command or f"python -m pytest tests/{task_slot} -q"
    return [
        PlannedFile(Path(f"configs/task/{task_slot}.yaml"), f"slot: {task_slot}\n"),
        PlannedFile(
            Path(f"tests/{task_slot}/index.md"),
            f"# {task_slot} Tests\n\nCanonical command:\n\n```bash\n{tests}\n```\n\n| File | Invariant checked | Delete/promote rule |\n|---|---|---|\n",
        ),
        PlannedFile(
            Path(f"scripts/{task_slot}/index.md"),
            f"# {task_slot} Scripts\n\nCanonical entrypoint:\n\n```bash\n{entry}\n```\n\n| Script / command | Purpose | Status |\n|---|---|---|\n",
        ),
        PlannedFile(
            Path(f"outputs/{task_slot}/index.md"),
            f"# {task_slot} Outputs\n\n| Date/run | Status | Config | Metrics | Claim usage |\n|---|---|---|---|---|\n\nExpected formal run layout:\n\n```text\noutputs/{task_slot}/<YYYY-MM-DD>/<HHMMSS>-<run-name>/\n```\n",
        ),
        PlannedFile(
            Path(f"docs/research-log/tasks/{task_slot}.md"),
            f"# {task_slot}\n\nPurpose: TBD.\n\nCanonical test command:\n\n```bash\n{tests}\n```\n\nCanonical run command:\n\n```bash\n{entry}\n```\n\n## Status\n\nactive scaffold\n\n## Human review needed\n\n- Confirm purpose.\n- Confirm metric, baseline, formula, and heavy-run decisions before real experiments.\n",
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
