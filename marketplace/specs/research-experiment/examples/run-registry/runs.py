#!/usr/bin/env python
"""Run registry CLI and library. Reference implementation for run-registry.md.

Copy to scripts/common/runs.py (CLI) or src/<package>/registry.py (library).
Stdlib-only. PyYAML is used opportunistically for key-level config diffs.

Truth model:
    outputs/<task-slot>/runs.jsonl   append-only event log (the truth)
    outputs/<task-slot>/index.md     generated view (never hand-edited)
    refs/runs/<task-slot>/<seq>      git snapshot of the exact tree per run

Commands: latest list show compare promote invalidate note render check backfill wrap
"""

from __future__ import annotations

import argparse
import json
import os
import platform
import re
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

try:  # optional, for key-level config diff only
    import yaml  # type: ignore
except ImportError:  # pragma: no cover
    yaml = None

RUN_ID_RE = re.compile(r"^(?P<slot>[a-z0-9][a-z0-9-]*)#(?P<seq>\d{4,})$")
EXEC_STATES = {"running", "success", "failed"}
VALIDITY_STATES = {"exploratory", "valid", "claim-ready", "invalidated", "superseded"}
ROLES = {"canonical", "replicate", "ablation"}

# ---------------------------------------------------------------- repo layout


_REPO_ROOT: Path | None = None


def repo_root() -> Path:
    global _REPO_ROOT
    if _REPO_ROOT is None:
        out = _git(["rev-parse", "--show-toplevel"], check=False)
        _REPO_ROOT = Path(out.strip()) if out else Path.cwd()
    return _REPO_ROOT


def outputs_dir() -> Path:
    return repo_root() / "outputs"


def registry_path(slot: str) -> Path:
    return outputs_dir() / slot / "runs.jsonl"


def all_slots() -> list[str]:
    if not outputs_dir().is_dir():
        return []
    return sorted(p.parent.name for p in outputs_dir().glob("*/runs.jsonl"))


# ---------------------------------------------------------------- git helpers


def _git(args: list[str], check: bool = True, env: dict | None = None) -> str | None:
    proc = subprocess.run(
        ["git", *args],
        capture_output=True,
        text=True,
        cwd=repo_root() if args[:1] != ["rev-parse"] else None,
        env={**os.environ, **(env or {})},
    )
    if proc.returncode != 0:
        if check:
            raise RuntimeError(f"git {' '.join(args)} failed: {proc.stderr.strip()}")
        return None
    return proc.stdout


def git_head() -> tuple[str | None, bool]:
    """Return (commit, dirty). commit is None in a repo with no commits."""
    commit = _git(["rev-parse", "HEAD"], check=False)
    commit = commit.strip() if commit else None
    dirty = bool((_git(["status", "--porcelain"], check=True) or "").strip())
    return commit, dirty


def snapshot_ref(slot: str, seq: int) -> str:
    return f"refs/runs/{slot}/{seq:04d}"


def git_snapshot(slot: str, seq: int) -> str | None:
    """Commit the exact working tree (incl. untracked) to refs/runs/<slot>/<seq>.

    Does not touch the working tree, the real index, or branch history.
    Returns the snapshot commit sha, or None when not in a git repo.
    """
    if _git(["rev-parse", "--git-dir"], check=False) is None:
        return None
    fd, tmp_index = tempfile.mkstemp(prefix="runs-index-")
    os.close(fd)
    os.unlink(tmp_index)  # git wants to create it itself
    env = {"GIT_INDEX_FILE": tmp_index}
    try:
        _git(["add", "-A"], env=env)  # empty temp index + add -A == working tree
        tree = (_git(["write-tree"], env=env) or "").strip()
        head, _ = git_head()
        commit_args = ["commit-tree", tree, "-m", f"snapshot: {slot}#{seq:04d}"]
        if head:
            commit_args[2:2] = ["-p", head]
        snap = (_git(commit_args) or "").strip()
        _git(["update-ref", snapshot_ref(slot, seq), snap])
        return snap
    finally:
        if os.path.exists(tmp_index):
            os.unlink(tmp_index)


def ref_exists(ref: str) -> bool:
    return _git(["rev-parse", "--verify", "--quiet", ref], check=False) is not None


def ref_on_origin(ref_or_sha: str) -> bool | None:
    """True/False, or None when no remote is configured."""
    if not (_git(["remote"], check=False) or "").strip():
        return None
    if _git(["ls-remote", "--exit-code", "origin", ref_or_sha], check=False) is not None:
        return True
    for line in (_git(["branch", "-r", "--contains", ref_or_sha], check=False) or "").splitlines():
        if line.strip():
            return True
    return False


# ---------------------------------------------------------------- event log


def now_iso() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def read_events(slot: str) -> list[dict]:
    path = registry_path(slot)
    if not path.is_file():
        return []
    events = []
    for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise SystemExit(f"{path}:{i}: corrupt registry line: {exc}")
    return events


class _SlotLock:
    """Cross-platform lock via atomic mkdir. Held only around seq-alloc+append."""

    def __init__(self, slot: str, timeout: float = 10.0):
        self.dir = outputs_dir() / slot / ".runs.lock"
        self.timeout = timeout

    def __enter__(self):
        deadline = time.monotonic() + self.timeout
        self.dir.parent.mkdir(parents=True, exist_ok=True)
        while True:
            try:
                self.dir.mkdir()
                return self
            except FileExistsError:
                if time.monotonic() > deadline:
                    raise SystemExit(f"registry lock stuck: {self.dir} (remove if stale)")
                time.sleep(0.05)

    def __exit__(self, *exc):
        self.dir.rmdir()


def append_event(slot: str, event: dict) -> None:
    event.setdefault("at", now_iso())
    line = json.dumps(event, ensure_ascii=False, sort_keys=True)
    path = registry_path(slot)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def next_seq(slot: str) -> int:
    seqs = [0]
    for ev in read_events(slot):
        m = RUN_ID_RE.match(ev.get("id", ""))
        if m:
            seqs.append(int(m.group("seq")))
    return max(seqs) + 1


def register_run(slot: str, path_rel: str, *, name: str, cmd: str, cfg_hash: str = "",
                 seed: int | None = None, backfilled: bool = False,
                 exec_state: str = "running") -> tuple[str, str | None]:
    """Allocate id, snapshot the tree, append the run event. Returns (run_id, snap)."""
    with _SlotLock(slot):
        seq = next_seq(slot)
        run_id = f"{slot}#{seq:04d}"
        snap = None if backfilled else git_snapshot(slot, seq)
        commit, dirty = git_head()
        event = {
            "ev": "run", "id": run_id, "path": path_rel, "name": name,
            "exec": exec_state, "git": commit, "dirty": dirty, "snap": snap,
            "cfg_hash": cfg_hash, "seed": seed, "host": platform.node() or "unknown",
            "cmd": cmd,
        }
        if backfilled:
            event["backfilled"] = True
        append_event(slot, event)
    return run_id, snap


def finish_run(run_id: str, exec_state: str, metrics: dict | None = None) -> None:
    slot, _ = parse_id(run_id)
    event = {"ev": "end", "id": run_id, "exec": exec_state}
    if metrics:
        event["metrics"] = metrics
    append_event(slot, event)


# ---------------------------------------------------------------- fold


@dataclass
class RunState:
    run_id: str
    slot: str
    seq: int
    path: str = ""
    name: str = ""
    exec: str = "running"
    validity: str = "exploratory"
    role: str = ""
    group: str = ""
    git: str | None = None
    dirty: bool = False
    snap: str | None = None
    cfg_hash: str = ""
    seed: int | None = None
    host: str = ""
    cmd: str = ""
    started_at: str = ""
    ended_at: str = ""
    metrics: dict = field(default_factory=dict)
    supersedes: list[str] = field(default_factory=list)
    superseded_by: str = ""
    notes: list[str] = field(default_factory=list)
    backfilled: bool = False

    @property
    def is_canonical(self) -> bool:
        return self.role == "canonical" and self.validity in ("valid", "claim-ready")


def parse_id(run_id: str) -> tuple[str, int]:
    m = RUN_ID_RE.match(run_id)
    if not m:
        raise SystemExit(f"bad run id: {run_id!r} (expected <slot>#<seq>)")
    return m.group("slot"), int(m.group("seq"))


def fold(slot: str) -> dict[str, RunState]:
    runs: dict[str, RunState] = {}
    for ev in read_events(slot):
        rid = ev.get("id", "")
        kind = ev.get("ev")
        if kind == "run":
            _, seq = parse_id(rid)
            runs[rid] = RunState(
                run_id=rid, slot=slot, seq=seq, path=ev.get("path", ""),
                name=ev.get("name", ""), exec=ev.get("exec", "running"),
                git=ev.get("git"), dirty=bool(ev.get("dirty")), snap=ev.get("snap"),
                cfg_hash=ev.get("cfg_hash", ""), seed=ev.get("seed"),
                host=ev.get("host", ""), cmd=ev.get("cmd", ""),
                started_at=ev.get("at", ""), backfilled=bool(ev.get("backfilled")),
            )
        elif rid not in runs:
            continue  # event for unknown run; `check` reports this
        elif kind == "end":
            runs[rid].exec = ev.get("exec", runs[rid].exec)
            runs[rid].ended_at = ev.get("at", "")
            runs[rid].metrics.update(ev.get("metrics") or {})
        elif kind == "promote":
            runs[rid].validity = ev.get("to", runs[rid].validity)
            runs[rid].role = ev.get("role", runs[rid].role or "canonical")
            runs[rid].group = ev.get("group", runs[rid].group)
            for old in ev.get("supersedes") or []:
                runs[rid].supersedes.append(old)
                if old in runs:
                    runs[old].validity = "superseded"
                    runs[old].superseded_by = rid
        elif kind == "invalidate":
            runs[rid].validity = "invalidated"
            runs[rid].notes.append(f"invalidated: {ev.get('reason', '')}")
        elif kind == "note":
            runs[rid].notes.append(ev.get("note") or ev.get("text", ""))
    return runs


def canonical_of(slot: str) -> RunState | None:
    hits = [r for r in fold(slot).values() if r.is_canonical]
    return hits[-1] if hits else None


def get_run(run_id: str) -> RunState:
    slot, _ = parse_id(run_id)
    runs = fold(slot)
    if run_id not in runs:
        raise SystemExit(f"unknown run: {run_id}")
    return runs[run_id]


def run_dir(state: RunState) -> Path:
    return outputs_dir() / state.slot / state.path


# ---------------------------------------------------------------- views


def render_slot(slot: str) -> str:
    runs = sorted(fold(slot).values(), key=lambda r: r.seq)
    canon = canonical_of(slot)
    lines = [
        f"# {slot} runs",
        "",
        "<!-- GENERATED by scripts/common/runs.py render - DO NOT EDIT BY HAND -->",
        "",
        f"Canonical: **{canon.run_id}** (`{canon.path}`)" if canon
        else "Canonical: **VACANT** (promote a run with `runs.py promote`)",
        "",
        "| Run | Name | Exec | Validity | Role | Started | Git | Note |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for r in runs:
        git_short = (r.snap or r.git or "")[:7] + ("*" if r.dirty and not r.snap else "")
        note = r.notes[-1] if r.notes else ""
        lines.append(
            f"| `{r.run_id}` | {r.name} | {r.exec} | {r.validity} | {r.role} "
            f"| {r.started_at[:16]} | `{git_short}` | {note} |"
        )
    lines.append("")
    return "\n".join(lines)


def render_root() -> str:
    lines = [
        "# Outputs",
        "",
        "<!-- GENERATED by scripts/common/runs.py render - DO NOT EDIT BY HAND -->",
        "",
        "| Task slot | Canonical | Validity | Runs | Last activity |",
        "|---|---|---|---|---|",
    ]
    for slot in all_slots():
        runs = fold(slot)
        canon = canonical_of(slot)
        last = max((r.ended_at or r.started_at for r in runs.values()), default="")
        lines.append(
            f"| `{slot}` | {'`' + canon.run_id + '`' if canon else 'VACANT'} "
            f"| {canon.validity if canon else '-'} | {len(runs)} | {last[:16]} |"
        )
    lines.append("")
    return "\n".join(lines)


def write_views(slots: list[str] | None = None) -> None:
    for slot in slots or all_slots():
        (outputs_dir() / slot / "index.md").write_text(render_slot(slot), encoding="utf-8")
    outputs_dir().mkdir(parents=True, exist_ok=True)
    (outputs_dir() / "index.md").write_text(render_root(), encoding="utf-8")


# ---------------------------------------------------------------- commands


def cmd_latest(args) -> int:
    canon = canonical_of(args.slot)
    if canon is None:
        print(f"{args.slot}: canonical VACANT "
              f"(no run with role=canonical and validity valid/claim-ready)")
        return 3
    print(json.dumps(vars(canon) | {"is_canonical": True}, ensure_ascii=False, indent=2)
          if args.json else f"{canon.run_id}  {canon.validity}  "
          f"{outputs_dir() / canon.slot / canon.path}")
    return 0


def cmd_list(args) -> int:
    rows = sorted(fold(args.slot).values(), key=lambda r: r.seq)
    if args.validity:
        rows = [r for r in rows if r.validity == args.validity]
    if args.exec_state:
        rows = [r for r in rows if r.exec == args.exec_state]
    if args.since:
        rows = [r for r in rows if (r.started_at or "")[:10] >= args.since]
    if args.json:
        print(json.dumps([vars(r) for r in rows], ensure_ascii=False, indent=2))
    else:
        for r in rows:
            print(f"{r.run_id}  {r.exec:8}  {r.validity:12}  {r.role or '-':10}  "
                  f"{r.started_at[:16]}  {r.name}")
    return 0


def cmd_show(args) -> int:
    state = get_run(args.id)
    payload = vars(state).copy()
    prov = run_dir(state) / "provenance.json"
    if prov.is_file():
        payload["provenance"] = json.loads(prov.read_text(encoding="utf-8"))
    payload["events"] = [e for e in read_events(state.slot) if e.get("id") == args.id]
    print(json.dumps(payload, ensure_ascii=False, indent=2) if args.json else
          "\n".join(f"{k}: {v}" for k, v in payload.items()))
    return 0


def _flatten(d: dict, prefix: str = "") -> dict[str, object]:
    out: dict[str, object] = {}
    for k, v in d.items():
        key = f"{prefix}.{k}" if prefix else str(k)
        if isinstance(v, dict):
            out.update(_flatten(v, key))
        else:
            out[key] = v
    return out


def cmd_compare(args) -> int:
    a, b = get_run(args.id_a), get_run(args.id_b)
    print(f"== {a.run_id}  vs  {b.run_id}\n")

    ref_a, ref_b = a.snap or a.git, b.snap or b.git
    if ref_a and ref_b:
        print(f"-- code ({ref_a[:7]}..{ref_b[:7]})")
        diff = _git(["diff", "--stat", ref_a, ref_b, "--", ".",
                     ":(exclude)outputs"], check=False)
        print(diff if (diff or "").strip() else "(identical)\n")
    else:
        print("-- code: snapshot/commit missing on one side; cannot diff\n")

    cfg_a = run_dir(a) / ".hydra" / "config.yaml"
    cfg_b = run_dir(b) / ".hydra" / "config.yaml"
    print("-- config")
    if cfg_a.is_file() and cfg_b.is_file():
        if yaml is not None:
            fa = _flatten(yaml.safe_load(cfg_a.read_text(encoding="utf-8")) or {})
            fb = _flatten(yaml.safe_load(cfg_b.read_text(encoding="utf-8")) or {})
            changed = {k for k in fa.keys() | fb.keys() if fa.get(k) != fb.get(k)}
            for k in sorted(changed):
                print(f"  {k}: {fa.get(k, '<absent>')} -> {fb.get(k, '<absent>')}")
            if not changed:
                print("  (identical)")
        else:
            import difflib
            sys.stdout.writelines(difflib.unified_diff(
                cfg_a.read_text(encoding="utf-8").splitlines(True),
                cfg_b.read_text(encoding="utf-8").splitlines(True),
                str(cfg_a), str(cfg_b)))
    else:
        print("  (config missing on one side)")

    print("\n-- metrics")
    keys = sorted(a.metrics.keys() | b.metrics.keys())
    for k in keys:
        va, vb = a.metrics.get(k), b.metrics.get(k)
        delta = ""
        if isinstance(va, (int, float)) and isinstance(vb, (int, float)):
            delta = f"  (delta {vb - va:+.6g})"
        print(f"  {k}: {va} -> {vb}{delta}")
    if not keys:
        print("  (no metrics recorded in registry)")
    return 0


def _scan_stale_citations(bad_ids: set[str]) -> list[str]:
    hits = []
    roots = [repo_root() / "docs" / "research-log", repo_root() / "paper"]
    sidecars = list(outputs_dir().glob("*/*/*/figures/*.json"))
    for path in [p for root in roots if root.is_dir()
                 for p in root.rglob("*") if p.suffix in (".md", ".json")] + sidecars:
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for bad in bad_ids:
            if bad in text:
                hits.append(f"{path.relative_to(repo_root())}: cites {bad}")
    return hits


def cmd_promote(args) -> int:
    state = get_run(args.id)
    slot = state.slot
    role = args.role or "canonical"
    if role not in ROLES:
        raise SystemExit(f"role must be one of {sorted(ROLES)}")

    if args.to == "valid":
        if state.exec != "success":
            raise SystemExit(f"refuse: exec status is {state.exec}, not success")
        reproducible = (state.snap and ref_exists(state.snap)) or \
                       (not state.dirty and state.git and ref_exists(state.git))
        if not reproducible:
            raise SystemExit("refuse: no snapshot ref and no clean commit; "
                             "run is not reproducible (see run-registry.md gates)")
        canon = canonical_of(slot)
        if role == "canonical" and canon and canon.run_id != args.id \
                and canon.run_id not in (args.supersedes or []):
            raise SystemExit(
                f"refuse: {canon.run_id} is already canonical.\n"
                f"Either --supersedes {canon.run_id} or use --role replicate/ablation.")
    elif args.to == "claim-ready":
        if state.validity != "valid":
            raise SystemExit(f"refuse: validity is {state.validity}; promote to valid first")
        if not args.by:
            raise SystemExit("refuse: claim-ready requires --by <human>")
        pushed = ref_on_origin(state.snap or state.git or "")
        if pushed is False and not args.allow_local:
            raise SystemExit("refuse: snapshot/commit not on origin; push refs/runs/* "
                             "or the commit, or override with --allow-local")
        stale = _scan_stale_citations({r.run_id for r in fold(slot).values()
                                       if r.validity in ("invalidated", "superseded")})
        if stale and not args.allow_local:
            raise SystemExit("refuse: stale citations of dead runs found:\n  "
                             + "\n  ".join(stale))
    else:
        raise SystemExit("promote target must be valid or claim-ready")

    event = {"ev": "promote", "id": args.id, "to": args.to, "role": role}
    if args.supersedes:
        event["supersedes"] = args.supersedes
    if args.group:
        event["group"] = args.group
    if args.by:
        event["by"] = args.by
    if args.note:
        event["note"] = args.note
    if args.allow_local:
        event["allow_local"] = True
    append_event(slot, event)
    write_views([slot])
    print(f"{args.id} -> {args.to} ({role})")
    return 0


def cmd_invalidate(args) -> int:
    state = get_run(args.id)
    append_event(state.slot, {"ev": "invalidate", "id": args.id,
                              "reason": args.reason, "by": args.by})
    write_views([state.slot])
    if state.is_canonical:
        print(f"note: {state.slot} canonical is now VACANT; re-promote explicitly")
    print(f"{args.id} -> invalidated")
    return 0


def cmd_note(args) -> int:
    state = get_run(args.id)
    append_event(state.slot, {"ev": "note", "id": args.id, "note": args.text})
    write_views([state.slot])
    return 0


def cmd_render(args) -> int:
    slots = all_slots() if args.all or not args.slot else [args.slot]
    write_views(slots)
    print(f"rendered {len(slots)} slot index(es) + outputs/index.md")
    return 0


def cmd_check(args) -> int:
    problems: list[str] = []
    warns: list[str] = []
    slots = [args.slot] if args.slot else all_slots()
    for slot in slots:
        events = read_events(slot)  # parse errors already fatal
        seen_ids: set[str] = set()
        for ev in events:
            rid = ev.get("id", "")
            if ev.get("ev") == "run":
                if rid in seen_ids:
                    problems.append(f"{slot}: duplicate run id {rid}")
                seen_ids.add(rid)
            elif rid and rid not in seen_ids:
                problems.append(f"{slot}: event {ev.get('ev')} for unknown run {rid}")
        runs = fold(slot)
        canon = [r for r in runs.values() if r.is_canonical]
        if len(canon) > 1:
            problems.append(f"{slot}: {len(canon)} canonical runs: "
                            f"{[r.run_id for r in canon]}")
        for r in runs.values():
            if not r.backfilled and not run_dir(r).is_dir():
                warns.append(f"{r.run_id}: run dir missing: {r.path}")
            if r.validity in ("valid", "claim-ready"):
                ok = (r.snap and ref_exists(r.snap)) or \
                     (not r.dirty and r.git and ref_exists(r.git))
                if not ok:
                    problems.append(f"{r.run_id}: {r.validity} but snapshot/commit "
                                    f"unresolvable in git")
            if r.validity == "claim-ready":
                pushed = ref_on_origin(r.snap or r.git or "")
                if pushed is False:
                    warns.append(f"{r.run_id}: claim-ready but not on origin")
        index = outputs_dir() / slot / "index.md"
        if index.is_file() and index.read_text(encoding="utf-8") != render_slot(slot):
            problems.append(f"{slot}: index.md is stale or hand-edited; run `runs.py render`")
        stale = _scan_stale_citations({r.run_id for r in runs.values()
                                       if r.validity in ("invalidated", "superseded")})
        problems.extend(stale)
    for w in warns:
        print(f"WARN  {w}")
    for p in problems:
        print(f"ERROR {p}")
    print(f"check: {len(problems)} error(s), {len(warns)} warning(s)")
    return 1 if problems else 0


def cmd_backfill(args) -> int:
    slot = args.slot
    known_paths = {r.path for r in fold(slot).values()}
    added = 0
    for day_dir in sorted((outputs_dir() / slot).glob("*/")):
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", day_dir.name):
            continue
        for rd in sorted(day_dir.glob("*/")):
            rel = f"{day_dir.name}/{rd.name}"
            if rel in known_paths:
                continue
            prov = {}
            prov_file = rd / "provenance.json"
            if prov_file.is_file():
                prov = json.loads(prov_file.read_text(encoding="utf-8"))
            status = "success"
            status_file = rd / "status.json"
            if status_file.is_file():
                raw = json.loads(status_file.read_text(encoding="utf-8")).get("status", "")
                status = {"success": "success", "failed": "failed"}.get(raw, "success")
            run_id, _ = register_run(
                slot, rel, name=rd.name.split("-", 1)[-1],
                cmd=prov.get("command", ""), cfg_hash="",
                seed=prov.get("seed"), backfilled=True, exec_state=status)
            added += 1
            print(f"backfilled {run_id} <- {rel} (exec={status}, validity=exploratory)")
    write_views([slot])
    print(f"backfill: {added} run(s) registered")
    return 0


def cmd_wrap(args) -> int:
    if not args.command:
        raise SystemExit("wrap: missing command after --")
    slot, name = args.slot, args.name
    started = datetime.now().astimezone()
    rel = f"{started:%Y-%m-%d}/{started:%H%M%S}-{name}"
    out = outputs_dir() / slot / rel
    out.mkdir(parents=True, exist_ok=True)
    cmd_str = subprocess.list2cmdline(args.command)
    run_id, snap = register_run(slot, rel, name=name, cmd=cmd_str)
    (out / "command.txt").write_text(cmd_str + "\n", encoding="utf-8")
    print(f"registered {run_id} (snap {snap[:7] if snap else 'none'}) -> {out}")

    log = open(out / "run.log", "w", encoding="utf-8")
    try:
        proc = subprocess.Popen(args.command, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT, text=True)
        assert proc.stdout is not None
        for line in proc.stdout:
            log.write(line)
            sys.stdout.write(line)
        code = proc.wait()
    finally:
        log.close()
    finish_run(run_id, "success" if code == 0 else "failed")
    write_views([slot])
    print(f"{run_id} finished: exit {code}")
    return code


# ---------------------------------------------------------------- entrypoint


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="runs.py", description=__doc__)
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("latest", help="canonical run of a slot (exit 3 when vacant)")
    s.add_argument("slot")
    s.add_argument("--json", action="store_true")
    s.set_defaults(fn=cmd_latest)

    s = sub.add_parser("list", help="list runs of a slot")
    s.add_argument("slot")
    s.add_argument("--validity", choices=sorted(VALIDITY_STATES))
    s.add_argument("--exec", dest="exec_state", choices=sorted(EXEC_STATES))
    s.add_argument("--since", help="YYYY-MM-DD")
    s.add_argument("--json", action="store_true")
    s.set_defaults(fn=cmd_list)

    s = sub.add_parser("show", help="full state + events + provenance of one run")
    s.add_argument("id")
    s.add_argument("--json", action="store_true")
    s.set_defaults(fn=cmd_show)

    s = sub.add_parser("compare", help="code + config + metric diff of two runs")
    s.add_argument("id_a")
    s.add_argument("id_b")
    s.set_defaults(fn=cmd_compare)

    s = sub.add_parser("promote", help="raise validity (gated)")
    s.add_argument("id")
    s.add_argument("--to", required=True, choices=["valid", "claim-ready"])
    s.add_argument("--role", choices=sorted(ROLES))
    s.add_argument("--supersedes", nargs="*")
    s.add_argument("--group")
    s.add_argument("--by")
    s.add_argument("--note")
    s.add_argument("--allow-local", action="store_true")
    s.set_defaults(fn=cmd_promote)

    s = sub.add_parser("invalidate", help="mark a run untrustworthy")
    s.add_argument("id")
    s.add_argument("--reason", required=True)
    s.add_argument("--by", required=True)
    s.set_defaults(fn=cmd_invalidate)

    s = sub.add_parser("note", help="append a note event")
    s.add_argument("id")
    s.add_argument("--text", required=True)
    s.set_defaults(fn=cmd_note)

    s = sub.add_parser("render", help="regenerate index.md views")
    s.add_argument("slot", nargs="?")
    s.add_argument("--all", action="store_true")
    s.set_defaults(fn=cmd_render)

    s = sub.add_parser("check", help="registry invariants (exit 1 on violation)")
    s.add_argument("slot", nargs="?")
    s.set_defaults(fn=cmd_check)

    s = sub.add_parser("backfill", help="register pre-registry run directories")
    s.add_argument("slot")
    s.set_defaults(fn=cmd_backfill)

    s = sub.add_parser("wrap", help="run + register an unmodified command")
    s.add_argument("--slot", required=True)
    s.add_argument("--name", default="wrapped")
    s.add_argument("command", nargs=argparse.REMAINDER,
                   help="command after -- to execute")
    s.set_defaults(fn=cmd_wrap)

    args = p.parse_args(argv)
    if getattr(args, "command", None) and args.command[0] == "--":
        args.command = args.command[1:]
    return args.fn(args)


if __name__ == "__main__":
    raise SystemExit(main())
