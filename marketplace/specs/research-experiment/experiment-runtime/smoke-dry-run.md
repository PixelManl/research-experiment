# Smoke / Dry Run Contract

Smoke tests prevent wasting 10 hours on a bug that would appear in 30 seconds.

## When to Read

Read this before:

- adding or changing a run script;
- modifying the main process, data path, config path, or output path;
- launching any run that may consume substantial GPU/CPU time;
- deciding whether a planned run has enough cheap evidence to proceed.

## Required smoke mode

Every task-slot must provide:

```bash
python scripts/<task-slot>/run.py debug=smoke
```

Use the verified project interpreter from
[python-command.md](./python-command.md). On Windows, do not replace this with
`python3` unless `python3` has been checked and is the active project
interpreter.

The smoke run must:

- finish in seconds or a few minutes;
- use tiny tensor sizes, tiny data, or toy environment;
- execute the real code path, not a fake mock path;
- write a normal output directory;
- produce `metrics.json`, `status.json`, and `run.log`;
- run at least one diagnostic if available.

## Dry run

Dry run validates setup without training:

```bash
python scripts/<task-slot>/run.py debug=dry_run
```

It should validate:

- config schema;
- paths;
- device availability;
- random seed setup;
- dataset manifest;
- output write permission;
- git provenance capture.

## Required before full run

Before any run expected to consume substantial GPU/CPU time:

```bash
pytest tests/<task-slot> -q
python scripts/<task-slot>/run.py debug=smoke
```

Then update `docs/research-log/tasks/<task-slot>.md` with:

```markdown
## Pre-heavy-run check YYYY-MM-DD HH:MM

- Test command:
- Smoke output:
- Config:
- Known objections:
- Human decision:
```

## Forbidden

- Starting full sweeps before a smoke run.
- Treating a mocked-only path as proof that the full path works.
- Using an output directory from a failed smoke run as evidence for a scientific claim.
