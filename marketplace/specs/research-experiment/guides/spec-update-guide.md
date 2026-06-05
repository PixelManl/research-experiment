# Spec Update Guide

Specs should evolve when bugs, repeated friction, or stable human preferences reveal a durable rule.

## Purpose

This guide keeps `.trellis/spec/` useful as a project source of truth. Update specs when a lesson should guide future agents, not when a note only belongs to one run, one chat, or one output directory.

## When to Use

Use this guide when:

- the same bug class appears twice;
- a human states a durable preference;
- a new project convention becomes stable;
- a pre-heavy-run review finds a preventable issue;
- a baseline/result invalidation required manual cleanup;
- agents repeatedly misplace files or skip the same check.

## How to Update

1. Put durable rules in the relevant layer.
2. Keep `index.md` concise and navigation-only.
3. Include exact paths.
4. Include good/bad examples when they reduce ambiguity.
5. Add tests, validation commands, or ledger updates when possible.
6. Remove placeholders or rules that no longer apply.

## Spec Page Shapes

Use one of these page shapes when adding or substantially revising a spec page.

### Contract Page

Use for durable rules such as runtime, provenance, numerics, data schema, ownership, and output organization.

```markdown
# <Topic> Contract

## Purpose

What this contract protects.

## When to Read

Read this before:
- ...

## Required Rules

Rules that must be followed.

## Forbidden

Patterns that must not appear.

## Required Checks

Tests, commands, ledger updates, or evidence required before finishing.

## Good / Bad Examples

Short examples only when they reduce ambiguity.

## Related Specs

- `...`
```

### Guide Page

Use for operational checklists that agents can run during a task.

```markdown
# <Task> Guide

## Purpose

What this guide helps prevent.

## When to Use

Use this guide when:
- ...

## Checklist

- [ ] ...

## Evidence to Record

Files, commands, run ids, decisions, or ledger entries that must be recorded.

## Exit Criteria

What must be true before moving on.

## Related Specs

- `...`
```

### Pitfall Page

Use for repeated failure patterns or high-risk research mistakes.

```markdown
# <Failure Pattern>

## Problem

What goes wrong.

## Symptoms

How it appears during research.

## Failure Chain

Step-by-step path from root cause to invalid result.

## Root Cause

The structural reason this bug happens.

## Required Fix

What must be changed now.

## Detection Checklist

- [ ] ...

## Prevention

Test, validation, spec update, or CI guard that prevents recurrence.

## Related Specs

- `...`
```

## Do Not Update Specs For

- one-off personal notes;
- large logs;
- unsettled hypotheses;
- private runtime state;
- outputs that belong in `outputs/`;
- research evidence that belongs in `docs/research-log/`.

## Related Specs

- [../agent-collaboration/break-loop-ci.md](../agent-collaboration/break-loop-ci.md)
- [../agent-collaboration/failure-evidence-ledger.md](../agent-collaboration/failure-evidence-ledger.md)
- [main-journal-protocol.md](./main-journal-protocol.md)
