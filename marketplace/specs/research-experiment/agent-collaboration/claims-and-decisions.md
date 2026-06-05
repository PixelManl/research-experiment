# Claims and Decisions Contract

Agents must not protect a failing story. They must help decide whether to continue, pause, stop, or reframe.

## Purpose

This contract keeps scientific claims and stop/continue decisions tied to file-backed evidence. AI may draft analysis and objections, but it must not silently upgrade weak evidence into a claim or make human-owned scientific decisions.

## When to Read

Read this before:

- stating that a method improves, fails, solves, or validates a research claim;
- comparing against a baseline or metric that may have changed;
- creating paper-facing reports, figures, or summaries;
- deciding whether to continue, pause, stop, or reframe a task;
- invalidating old outputs or citing results after a bug fix.

## Decision file

Major decisions go under:

```text
docs/research-log/decisions/YYYY-MM-DD-<decision>.md
```

## Decision template

```markdown
# Decision: <title>

Date:
Task slot:
Decision: Continue | Pause | Stop | Reframe

## Evidence

## Counter-evidence

## Reviewer objections

## Invalidated outputs

## Compute cost of continuing

## Smallest next diagnostic

## Human decision
```

## Stop/reframe triggers

AI must explicitly raise stop/reframe when:

- a cheaper diagnostic contradicts the core assumption;
- baseline changed and narrative no longer holds;
- parameter sweeps are being used to compensate for weak math;
- first-order/second-order or signal/noise diagnostics make the proposed mechanism unlikely;
- reproducibility fails across seeds without explanation;
- new bugs invalidate the main result chain.

## Claim language

Use cautious levels:

- “This smoke run passes the implementation path.”
- “Current evidence suggests X, but OBJ-003 remains open.”
- “This is not claim-ready because the baseline ledger is unresolved.”
- “The result is invalidated by the 2026-05-20 reward bug.”

## Forbidden

- “Solved” without evidence.
- “Clearly improves” from one exploratory run.
- “Probably fine” for baseline correctness.
- changing scientific conclusion in chat without a decision file.

## Related Specs

- [ownership-tiers.md](./ownership-tiers.md)
- [reviewer-objections-ledger.md](./reviewer-objections-ledger.md)
- [failure-evidence-ledger.md](./failure-evidence-ledger.md)
- [../experiment-modules/evaluation-and-baselines.md](../experiment-modules/evaluation-and-baselines.md)
- [../guides/research-stop-continue-decision.md](../guides/research-stop-continue-decision.md)
