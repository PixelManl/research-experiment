# Pre-Heavy-Run Review Contract

One hour of review is cheaper than ten hours of bad compute.

## When to Read

Read this before:

- launching expensive, remote, sweep, or paper-facing runs;
- spending major compute after code, baseline, metric, or formula changes;
- asking another agent to review planned heavy compute;
- deciding whether objections, smoke evidence, and provenance are sufficient.

## Trigger

Run this review before any job that is expensive in time, GPU, money, or narrative commitment.

Default trigger:

- expected runtime > 30 minutes;
- uses remote/GPU batch;
- launches a sweep;
- produces data intended for paper/report;
- changes a baseline or metric.

## Required review packet

Create/update in `docs/research-log/tasks/<task-slot>.md`:

```markdown
## Pre-heavy-run review YYYY-MM-DD HH:MM

Command:
Config:
Output target:
Git commit:
Git diff patch will be saved: yes/no
Smoke run:
Tests:
Known objections:
Cheapest diagnostic not yet done:
Expected resource use:
Human decision:
```

## Independent check

Before launching, ask a separate checking pass/agent to review:

- config keys and defaults;
- output paths;
- task-slot consistency;
- provenance capture;
- tests and smoke result;
- tensor shapes and data schema;
- top reviewer objections;
- whether this run answers the actual question.

## Launch gate

All must be true:

- task tests pass;
- smoke run pass;
- provenance path verified;
- output directory unique;
- invalidated-result ledger checked;
- baseline status active;
- reviewer objections checked and resolved;
- human approved T2/T3 items.

## Forbidden

- launching full run to “see what happens” when smoke is broken;
- sweeping parameters to avoid checking a math objection;
- using AI confidence as substitute for independent check;
- launching remote jobs without log capture.
