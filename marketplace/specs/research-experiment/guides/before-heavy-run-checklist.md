# Before Heavy Run Checklist

Use this immediately before expensive compute.

## Required evidence

- [ ] `pytest tests/<task-slot> -q` passes.
- [ ] `python scripts/<task-slot>/run.py debug=smoke` passes.
- [ ] Hydra config is composed and saved.
- [ ] Output directory is unique.
- [ ] `git.diff.patch` will be saved.
- [ ] `run.log` will capture stdout/stderr.
- [ ] Baseline ledger checked.
- [ ] Invalidated-results ledger checked.
- [ ] Reviewer objections checked.
- [ ] Human approved T2/T3 decisions.

## Cheapest diagnostic question

Before sweep, answer:

```text
Is there a cheaper diagnostic that could falsify the reason for this run?
```

If yes, run that first.

## Review prompt for checker agent

```text
Please review this planned heavy run. Check config, task-slot consistency, output/provenance, tests, smoke result, baseline validity, tensor shape risks, numerical risks, and reviewer objections. Do not implement. Return blockers, warnings, and approval status.
```
