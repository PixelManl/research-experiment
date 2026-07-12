# Examples Index

This directory is a **reference asset layer**, not a coding-contract layer.

Trellis scans every subdirectory under `.trellis/spec/` (except `guides`) as a
spec layer and lists `index.md` for each. This file exists so that discovery
does not point at a missing path. Do **not** treat examples as project rules.

## What belongs here

- Optional bootstrap scripts that illustrate a possible initial layout.
- Snippets that show how task-scoped `tests/` / `scripts/` / `outputs/` indexes
  might look after adaptation.
- Reference run-registry helpers that demonstrate provenance + `runs.py` shape.

## What does not belong here

- Project-owned coding conventions (those live in other layers).
- Secrets, private URLs, active task state, or platform prompt files.
- Paths that must appear in every task's `implement.jsonl` / `check.jsonl`.

## Guidelines Index

| Guide / asset | Description | When to Read |
|---------------|-------------|--------------|
| [bootstrap/bootstrap.py](./bootstrap/bootstrap.py) | Optional scaffold illustration for a research layout | Only when bootstrapping a new repo and the user asks for a scaffold reference |
| [repo-files/tests-index.md](./repo-files/tests-index.md) | Example `tests/` index shape | Adapting task-scoped test indexes |
| [repo-files/scripts-index.md](./repo-files/scripts-index.md) | Example `scripts/` index shape | Adapting task-scoped script indexes |
| [repo-files/outputs-index.md](./repo-files/outputs-index.md) | Example `outputs/` index shape | Adapting output indexes (prefer generated views when using `runs.py`) |
| [repo-files/gitignore-snippet.md](./repo-files/gitignore-snippet.md) | Suggested ignore patterns for research outputs | Setting up `.gitignore` |
| [run-registry/runs.py](./run-registry/runs.py) | Reference CLI for run registry operations | Implementing or adapting `scripts/common/runs.py` |
| [run-registry/provenance.py](./run-registry/provenance.py) | Reference provenance helper shape | Implementing run capture / registration |

## Pre-Development Checklist

Examples are optional. Before copying anything from this layer:

- [ ] Confirm the target project does not already have an equivalent path.
- [ ] Prefer project-owned files under `tests/`, `scripts/`, `outputs/`, and
      `src/<package>/` over keeping long-lived logic inside `examples/`.
- [ ] Read the real contract layers first:
      - [../project-structure/index.md](../project-structure/index.md)
      - [../experiment-runtime/run-registry.md](../experiment-runtime/run-registry.md)
      - [../experiment-runtime/provenance.md](../experiment-runtime/provenance.md)
- [ ] Do **not** add `examples/**` paths to `implement.jsonl` / `check.jsonl`
      unless the task is explicitly about adapting these reference files.
- [ ] Treat bootstrap scripts as starting points to rewrite, not as required
      Trellis entrypoints.

## Quality Check

- [ ] No secrets, private hosts, or project-only credentials in example files.
- [ ] Examples still match the contracts described in the coding layers, or are
      clearly marked outdated.
- [ ] Copied examples were adapted to real package names and paths (no leftover
      `<package>` / placeholder-only trees that the project never uses).
- [ ] Heavy helpers were moved out of `examples/` into project-owned
      `scripts/common/` or `src/` when they became production dependencies.
