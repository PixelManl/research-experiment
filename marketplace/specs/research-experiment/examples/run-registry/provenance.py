"""Provenance capture with automatic run registration. Reference implementation.

Copy to src/<package>/provenance.py. Pairs with the registry library/CLI
(examples/run-registry/runs.py -> scripts/common/runs.py).

The single integration point for a run entrypoint:

    @hydra.main(version_base=None, config_path="../../configs", config_name="config")
    def main(cfg: DictConfig) -> None:
        with provenance.tracked_run(cfg) as run:
            result = train(cfg, run.out_dir)
            run.metrics(return_mean=result.return_mean)

On enter: allocate run id, snapshot the git tree to refs/runs/<slot>/<seq>,
write provenance.json / command.txt / environment.txt / git.diff.patch /
status.json, append the `run` event to outputs/<slot>/runs.jsonl.
On exit: write final status.json, append the `end` event (with metrics),
regenerate index views. Exceptions propagate after the failure is recorded —
never swallow errors.

No new command-line arguments. Validity (valid / claim-ready / invalidated)
is NOT decided here; that is a post-hoc explicit act via `runs.py promote`.
"""

from __future__ import annotations

import hashlib
import json
import os
import platform
import subprocess
import sys
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import Iterator

from omegaconf import DictConfig, OmegaConf

# Registry primitives. Installed projects import from scripts/common (kept
# importable via a conftest/path hook) or move the registry core into
# src/<package>/registry.py — pick one and delete the other import.
from runs import (  # type: ignore
    finish_run,
    now_iso,
    register_run,
    repo_root,
    write_views,
)


class TrackedRun:
    def __init__(self, run_id: str, out_dir: Path, slot: str):
        self.run_id = run_id
        self.out_dir = out_dir
        self.slot = slot
        self._metrics: dict = {}

    def metrics(self, **values) -> None:
        """Record summary metrics; flushed into the `end` event and metrics.json."""
        self._metrics.update(values)


def _git(args: list[str]) -> str:
    proc = subprocess.run(["git", *args], capture_output=True, text=True,
                          cwd=repo_root())
    return proc.stdout if proc.returncode == 0 else ""


def _write_environment(out_dir: Path) -> None:
    lines = [
        f"python: {sys.version.split()[0]}",
        f"executable: {sys.executable}",
        f"platform: {platform.platform()}",
        f"host: {platform.node()}",
    ]
    try:
        import torch  # type: ignore
        lines += [
            f"torch: {torch.__version__}",
            f"cuda_available: {torch.cuda.is_available()}",
            f"cuda_version: {getattr(torch.version, 'cuda', None)}",
            f"device_count: {torch.cuda.device_count() if torch.cuda.is_available() else 0}",
        ]
    except ImportError:
        lines.append("torch: not installed")
    pip = subprocess.run([sys.executable, "-m", "pip", "freeze"],
                         capture_output=True, text=True)
    (out_dir / "environment.txt").write_text(
        "\n".join(lines) + "\n\n# pip freeze\n" + pip.stdout, encoding="utf-8")


def _write_status(out_dir: Path, slot: str, status: str,
                  started_at: str, failure: str | None = None) -> None:
    (out_dir / "status.json").write_text(json.dumps({
        # Execution axis only. Validity lives in the registry (run-registry.md).
        "status": status,
        "task_slot": slot,
        "started_at": started_at,
        "finished_at": now_iso() if status != "running" else None,
        "failure_reason": failure,
    }, indent=2, ensure_ascii=False), encoding="utf-8")


@contextmanager
def tracked_run(cfg: DictConfig) -> Iterator[TrackedRun]:
    slot = cfg.task.slot
    out_dir = Path.cwd() if cfg.get("hydra_managed_dir", True) else None
    # Under hydra.job.chdir=false, resolve the run dir from Hydra's runtime cfg:
    try:
        from hydra.core.hydra_config import HydraConfig
        out_dir = Path(HydraConfig.get().runtime.output_dir)
    except Exception:
        out_dir = out_dir or Path.cwd()
    out_dir.mkdir(parents=True, exist_ok=True)

    started_at = now_iso()
    cfg_yaml = OmegaConf.to_yaml(cfg, resolve=False)
    cfg_hash = hashlib.sha256(cfg_yaml.encode("utf-8")).hexdigest()[:12]
    command = subprocess.list2cmdline([sys.executable, *sys.argv])

    rel = out_dir.relative_to(repo_root() / "outputs" / slot).as_posix()
    run_id, snap = register_run(
        slot, rel,
        name=str(cfg.run.name),
        cmd=command,
        cfg_hash=cfg_hash,
        seed=int(cfg.run.seed) if "seed" in cfg.get("run", {}) else None,
    )

    (out_dir / "command.txt").write_text(command + "\n", encoding="utf-8")
    _write_environment(out_dir)

    # Human-browsable view of uncommitted changes; the snapshot ref is the
    # reproducibility mechanism (see run-registry.md). Mandatory even if empty.
    (out_dir / "git.diff.patch").write_text(_git(["diff", "--binary"]), encoding="utf-8")

    commit = _git(["rev-parse", "HEAD"]).strip() or None
    dirty = bool(_git(["status", "--porcelain"]).strip())
    if commit is None and not cfg.get("debug", {}).get("allow_no_git", False):
        raise RuntimeError("not a git repository; set debug.allow_no_git=true to override")

    (out_dir / "provenance.json").write_text(json.dumps({
        "run_id": run_id,
        "task_slot": slot,
        "git_commit": commit,
        "git_dirty": dirty,
        "git_snapshot": snap,
        "git_snapshot_ref": f"refs/runs/{slot}/{run_id.split('#')[1]}" if snap else None,
        "git_diff_patch": "git.diff.patch",
        "config_path": ".hydra/config.yaml",
        "config_hash": cfg_hash,
        "command": command,
        "executable": sys.executable,
        "host": platform.node(),
        "seed": OmegaConf.select(cfg, "run.seed"),
        "created_at": started_at,       # ISO 8601 with UTC offset
        "notes": "",
    }, indent=2, ensure_ascii=False), encoding="utf-8")

    _write_status(out_dir, slot, "running", started_at)
    run = TrackedRun(run_id, out_dir, slot)
    try:
        yield run
    except BaseException as exc:
        _write_status(out_dir, slot, "failed", started_at, failure=repr(exc))
        finish_run(run_id, "failed", run._metrics or None)
        write_views([slot])
        raise  # crash loudly after recording failure
    else:
        if run._metrics:
            (out_dir / "metrics.json").write_text(
                json.dumps(run._metrics, indent=2, ensure_ascii=False), encoding="utf-8")
        _write_status(out_dir, slot, "success", started_at)
        finish_run(run_id, "success", run._metrics or None)
        write_views([slot])
