# Research Pitfalls Index

This layer captures recurring failure modes that are locally easy to miss but globally expensive. Treat each pitfall as a source of review gates, regression tests, and spec updates.

## Documentation Files

| File | Purpose | When to Read | Priority |
|---|---|---|---|
| [coupled-logic-drift.md](./coupled-logic-drift.md) | Downstream logic fails to follow a core semantic change | When a core mechanism changes and dependent logic may be stale | Must Read |
| [route-value-drift.md](./route-value-drift.md) | Locally correct stages no longer support the original value question | When correct artifacts, exactness, protocols, or infrastructure do not prove route value | Must Read |

## Quick Navigation by Task

Changing a core mechanism that may affect downstream logic?

- Read [coupled-logic-drift.md](./coupled-logic-drift.md).
- Trace all dependent objectives, entropy terms, metrics, diagnostics, baselines, and reports.
- Update or invalidate anything whose meaning changed, even if the local module test passes.

Continuing a route after correct but value-insufficient results?

- Read [route-value-drift.md](./route-value-drift.md).
- Restate the original value question and value-bearing judgment before adding the next stage.
- Define the minimum discriminating test against the strongest simple baseline before building more infrastructure.

## Core Rules Summary

- A pitfall page should describe a recurring failure mode, not a one-off bug report.
- Each pitfall must map to preventive checks, recovery actions, and the spec or CI gate that should catch it next time.
- Passing tests, exact references, and no-claim flags are not substitutes for route value evidence.
- Pitfalls should be concise enough to act on during review or before heavy compute.
