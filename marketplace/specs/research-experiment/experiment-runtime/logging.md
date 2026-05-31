# Logging Contract

Logging must be configurable, file-backed, and low-overhead by default.

## Required

Use Python `logging` or a project logger wrapper. Do not use `print` for experiment progress except in interactive REPL/notebooks.

Default behavior:

- `INFO` to `run.log`;
- minimal console output;
- `DEBUG` only when `cfg.debug.mode != off`;
- structured metrics to `metrics.json`, not only logs;
- progress bars disabled or redirected in remote/non-interactive runs.

## Config fields

```yaml
logging:
  level: INFO
  console: true
  file: true
  log_interval_steps: 100
  capture_stdout_stderr: true
```

## stdout/stderr

Formal runs must redirect stdout/stderr to files or logging handlers so concurrent jobs do not corrupt terminal output.

Required files:

```text
run.log
stdout.log        # if separate capture is used
stderr.log        # if separate capture is used
```

## What to log

At run start:

- task-slot;
- output directory;
- git commit and dirty status;
- config path;
- seed;
- device summary.

During run:

- coarse progress only;
- metrics at configured interval;
- warnings for numerical anomalies.

At finish:

- status;
- final metrics;
- artifact paths.

## Forbidden

```python
print(loss)
print("here")
print("done?")
```

Use:

```python
logger.debug("loss=%s step=%s", float(loss), step)
```

## Diagnostic mode

Expensive debug logs and tensor dumps require:

```yaml
debug:
  diagnostics: true
```

Do not dump large tensors during normal runs.
