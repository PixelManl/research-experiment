# Research Pitfalls Index

Recurring failure modes that are locally easy to miss but globally expensive.
Treat each pitfall as a source of review gates, regression tests, and spec updates.

## Guidelines Index

| Guide | Description | When to Read |
|-------|-------------|--------------|
| [coupled-logic-drift.md](./coupled-logic-drift.md) | Downstream logic fails to follow a core semantic change | Core mechanism changes; dependent logic may be stale |
| [route-value-drift.md](./route-value-drift.md) | Locally correct stages no longer support the original value question | Correct artifacts/exactness/infra do not prove route value |

## Pre-Development Checklist

- [ ] Core mechanism change → read [coupled-logic-drift.md](./coupled-logic-drift.md);
      trace dependent objectives, entropy terms, metrics, diagnostics, baselines, reports.
- [ ] Continuing after correct-but-value-weak results → read
      [route-value-drift.md](./route-value-drift.md); restate the original value question
      before adding stages or infrastructure.
- [ ] Define the minimum discriminating test against the strongest simple baseline before
      building more exactness, protocol, benchmark, or control-plane machinery.
- [ ] Update or invalidate anything whose meaning changed even if the local module test
      still passes.
- [ ] Map the pitfall to a preventive check: test, validation, checklist, or CI gate.

## Quality Check

- [ ] Dependent logic was updated or explicitly marked invalid after semantic changes.
- [ ] Route still answers the original value question, not only local correctness.
- [ ] Passing tests / exact references / no-claim flags are not treated as substitutes
      for route-value evidence.
- [ ] New recurring failure modes were added as pitfall pages or linked gates, not left
      only in chat.
