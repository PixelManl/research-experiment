# Bug Root Cause Retrospective

Use after every meaningful bug fix.

## When to Use

Use this guide when:

- a bug was fixed and the root cause is not yet classified;
- a failed or invalidated run may reveal a preventable bug class;
- deciding whether the fix needs a test, validation rule, spec update, or CI gate;
- the same bug pattern appears more than once.

```markdown
## Bug retrospective YYYY-MM-DD

Task slot:

### Symptom

### Root cause

### Why it escaped

### Affected outputs

### Fix

### Prevent-repeat mechanism

- Test added/updated:
- Spec added/updated:
- Validation added/updated:
- Ledger updated:

### Remaining risk
```

## Required actions

- Mark invalidated outputs if needed.
- Add a focused regression test.
- Update the relevant spec if this bug class was not covered.
- Keep the bug narrative objective; do not hide it as “cleanup”.
