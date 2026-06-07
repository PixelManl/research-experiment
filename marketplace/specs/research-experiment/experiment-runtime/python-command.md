# Python Command Contract

Python commands must be copied exactly for the current platform. Do not replace
`python` with `python3`, or the reverse, unless the target environment has been
checked.

## When to Read

Read this before:

- running Trellis helper scripts;
- writing canonical task commands;
- creating smoke, dry-run, or remote launch commands;
- asking an agent to execute commands across Windows, Linux, or macOS.

## Required

Use the active project interpreter as the command source:

```bash
python -c "import sys; print(sys.executable)"
```

Template examples use:

```bash
python
```

because it works with common Windows Conda/venv setups. On Unix systems where
`python` is not installed but `python3` is the project interpreter, record
`python3` in the project command index and use it consistently.

## Forbidden

- Do not silently rewrite a documented `python` command to `python3`.
- Do not use POSIX inline environment assignment in canonical commands:

```bash
PYTHONPATH=src python -m package.main
```

This fails on PowerShell. Prefer an installed package entrypoint, a project
launcher script, or platform-specific notes in `scripts/<task-slot>/index.md`.

## Windows check

On Windows, verify interpreter resolution before running helper scripts:

```powershell
where.exe python
where.exe python3
python -c "import sys; print(sys.executable)"
```

If `python3` resolves to `WindowsApps`, use `python` or `py -3` instead.

## Recording

Every formal run must record:

- exact command string;
- `sys.executable`;
- Python version;
- package or editable-install status when the command depends on `src/`.
