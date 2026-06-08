# Before Heavy Run Checklist

Use this immediately before expensive compute.

## Purpose

This guide prevents expensive runs from amplifying preventable mistakes. Heavy compute should start only after the task path, config, provenance, tests, smoke evidence, baseline validity, objections, and human-owned decisions are checked.

## When to Use

Use this guide before:

- long training runs;
- large parameter sweeps;
- remote or multi-machine jobs;
- paper-facing experiments;
- any run whose failure would waste significant compute or delay the project.

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

## Optional external heavy-model review

If the user explicitly asks for or approves external heavy-model review, prepare a heavy-package using [../agent-collaboration/external-heavy-model-review.md](../agent-collaboration/external-heavy-model-review.md).

Do not create, export, upload, or send a heavy-package without explicit user request or approval. The package prompt must include both current-problem directed review and future-direction creative review.

## Review prompt for checker agent

```text
Please review this planned heavy run. Check config, task-slot consistency, output/provenance, tests, smoke result, baseline validity, tensor shape risks, numerical risks, and reviewer objections. Do not implement. Return blockers, warnings, and approval status.
```

## Exit Criteria

Before launching the run:

- required evidence is checked;
- blockers from reviewer objections are resolved or explicitly accepted;
- output/provenance paths are ready;
- human approval exists for T2/T3 decisions;
- the smallest cheaper diagnostic has already been considered.

## Related Specs

- [../experiment-runtime/provenance.md](../experiment-runtime/provenance.md)
- [../experiment-runtime/smoke-dry-run.md](../experiment-runtime/smoke-dry-run.md)
- [../experiment-runtime/remote-concurrency.md](../experiment-runtime/remote-concurrency.md)
- [../agent-collaboration/pre-heavy-run-review.md](../agent-collaboration/pre-heavy-run-review.md)
- [../agent-collaboration/external-heavy-model-review.md](../agent-collaboration/external-heavy-model-review.md)
- [../agent-collaboration/ownership-tiers.md](../agent-collaboration/ownership-tiers.md)
