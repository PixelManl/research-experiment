# Reports and Claim Summaries Contract

Reports convert outputs into decisions. They must distinguish observation, hypothesis, evidence, and claim.

## When to Read

Read this before:

- writing task reports, milestone summaries, or paper-facing evidence;
- turning outputs into observations, hypotheses, decisions, or claims;
- deciding which runs are usable or excluded;
- recording human approval for claim-ready results.

## Required report location

Use:

```text
docs/research-log/tasks/<task-slot>.md
```

or for larger milestones:

```text
docs/research-log/reports/YYYY-MM-DD-<short-name>.md
```

## Claim levels

Use these labels:

- `Observation`: what a run showed.
- `Hypothesis`: possible explanation, not proven.
- `Evidence-backed`: supported by tests/runs, still internal.
- `Claim-ready`: human approved for paper/report.
- `Invalidated`: no longer usable.

## Report template

```markdown
# Report: <task-slot> / <short title>

## Question

## Runs used

| Run | Status | Why usable |
|---|---|---|

## Observations

## Hypotheses

## Reviewer objections

## Invalidated or excluded outputs

## Decision

Continue | Pause | Stop | Reframe

## Human approval

Name/date:
```

## Forbidden

- collapsing “the model learned” and “the reward increased once” into one claim;
- omitting failed runs that affect interpretation;
- using invalidated outputs;
- letting agent change narrative after pushback without updating objections and evidence.
