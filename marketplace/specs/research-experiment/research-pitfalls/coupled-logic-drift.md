# Pitfall: Coupled Logic Drift

## When to Read

Read this when a core mechanism changes but the downstream logic may still assume the old semantics.

## Why it matters

In research code, a local improvement can change the meaning of everything that depends on it. A module may be correct in isolation, yet the system can still fail if coupled logic is not updated together. This creates a semantic mismatch: the implementation is locally valid, but globally inconsistent.

This is especially dangerous in RL and ML systems, where action parameterization, entropy terms, reward shaping, diagnostics, baseline comparison, and evaluation logic are tightly coupled. A change to one component can invalidate assumptions elsewhere without breaking a local test.

## Typical symptoms

- A core mechanism is improved, but a downstream term still uses the old semantic.
- Unit tests pass because they only cover the updated module in isolation.
- Training continues, but optimization exploits a stale auxiliary objective.
- Metrics or diagnostics look normal while the actual behavior is corrupted.
- A change in action distribution, reward definition, or loss structure silently breaks another part of the system.

## Example

A PPO policy changes from hard action clipping to tanh-squashed actions with Jacobian correction. The policy update is correct, but the entropy term still uses `dist.entropy()` from the unsquashed distribution. The entropy bonus no longer matches the real action semantics, so the agent can exploit the mismatch and maximize reward through entropy hacking. The bug is not local to the new policy logic; it comes from failing to update the coupled downstream logic.

## Common causes

- Updating a core mechanism without tracing its dependents.
- Treating a refactor as a local change instead of a semantic change.
- Missing a dependency review for derived losses, metrics, or diagnostics.
- Assuming passable tests imply global consistency.
- Not recording the contract change in the research log or spec.

## Prevention

- Treat semantic changes as contract changes.
- For every change to a core mechanism, identify all dependent logic:
  - objectives
  - entropy or regularization terms
  - reward shaping
  - metrics
  - diagnostics
  - baselines
  - reports
  - figures
- Require a dependency impact review before accepting the change.
- Update the relevant spec pages and ledgers when the meaning of a variable or term changes.
- Add regression tests that cover the coupled behavior, not just the isolated module.

## Required reads

- [math-formula-mapping.md](../research-code/math-formula-mapping.md)
- [numerics.md](../research-code/numerics.md)
- [validation-assertions.md](../research-code/validation-assertions.md)
- [evaluation-and-baselines.md](../experiment-modules/evaluation-and-baselines.md)
- [claims-and-decisions.md](../agent-collaboration/claims-and-decisions.md)

## Related ledgers

- `docs/research-log/baselines.md`
- `docs/research-log/invalidated-results.md`
- `docs/research-log/reviewer-objections.md`
- `docs/research-log/decisions/`

## CI / review gate

Warn or block when:

- a core logic changes but no dependency review is recorded;
- a derived loss, metric, or diagnostic still references the old semantic;
- a policy parameterization changes but entropy or objective logic is unchanged;
- a report or baseline uses a quantity whose meaning no longer matches the current contract.

## Recovery action

If coupled logic drift is detected:

1. classify the semantic change;
2. enumerate all dependent logic;
3. update the downstream code and spec together;
4. invalidate any affected outputs;
5. rerun the relevant experiments;
6. add a regression test to prevent recurrence.