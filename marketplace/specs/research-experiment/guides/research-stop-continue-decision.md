# Research Stop / Continue Decision Guide

Use when a project may be failing, looping, or becoming narrative-driven.

## When to Use

Use this guide when:

- evidence is weak, contradictory, or invalidated;
- compute cost is rising without stronger diagnostic evidence;
- baseline, metric, formula, or data changes threaten the current story;
- deciding whether to continue, pause, stop, or reframe a task.

## Decision question

```text
Given current evidence, should we continue, pause, stop, or reframe?
```

## Evidence checklist

- What exact claim are we trying to support?
- Which runs are valid?
- Which runs are invalidated?
- Which baseline is active?
- Which objections remain open?
- What is the smallest next diagnostic?
- What compute cost would continuing require?
- What would make us stop?

## Agent behavior

AI should be supportive but objective. It must not continue polishing a story if evidence points against it.

## Decision output

Create:

```text
docs/research-log/decisions/YYYY-MM-DD-<continue-pause-stop-reframe>.md
```

Use the template from `agent-collaboration/claims-and-decisions.md`.
