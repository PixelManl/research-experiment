# Math and Formula Mapping Contract

Mathematical modeling is a human-review surface. The implementation must make formula alignment obvious.

## Purpose

This contract makes paper-derived or note-derived math auditable by humans. A reviewer should be able to map each nontrivial formula to an implementation path, tensor shape assumptions, and tests without relying on chat history.

## When to Read

Read this before:

- translating a paper, note, or derivation into code;
- changing loss, reward, objective, estimator, update rule, or metric math;
- claiming that an implementation matches an equation;
- documenting unresolved mathematical risk or reviewer objections.

## Required for paper-derived code

Create or update:

```text
docs/research-log/equation-maps/<task-slot>.md
```

Format:

```markdown
| Paper / note | Equation | Meaning | Implementation | Test |
|---|---|---|---|---|
| PPO paper | Eq. 7 | clipped surrogate objective | `src/<package>/algorithms/ppo.py:compute_loss` | `tests/ppo-handwritten/test_ppo_loss.py` |
```

## Code comment format

(For shape annotation format, see `tensor-shapes-typing.md`.)

Near the implementation:

```python
# Eq. (GAE):
#   A_t = delta_t + gamma * lambda * (1 - done_t) * A_{t+1}
# Implementation mapping:
#   rewards[t] -> r_t           shape [T, B]
#   values[t]  -> V(s_t)        shape [T + 1, B]
#   dones[t]   -> done_t        shape [T, B]
# Output:
#   advantages                 shape [T, B]
```

## Required when derivation is uncertain

If the math is not fully settled, do not present it as solved. Add an uncertainty block:

```markdown
## Open math risk

Claim under test:
Evidence currently available:
Counterargument:
Smallest diagnostic experiment:
Human decision needed:
```

## Reviewer objection hook

Every nontrivial formula must have at least one possible objection in:

```text
docs/research-log/reviewer-objections.md
```

Example:

```markdown
| ID | Objection | Evidence needed | Status |
|---|---|---|---|
| OBJ-003 | Second-order Taylor term may be negligible if first-order gradient is already small | compare first/second-order magnitude on toy and real batches | open |
```

## Forbidden

- “Paper says this” without equation number or note reference.
- Implementing a derived formula without shape comments.
- Changing a formula and only mentioning it in chat.
- Upgrading a hypothesis to a claim without tests/evidence.

## Related Specs

- [tensor-shapes-typing.md](./tensor-shapes-typing.md)
- [validation-assertions.md](./validation-assertions.md)
- [numerics.md](./numerics.md)
- [../agent-collaboration/reviewer-objections-ledger.md](../agent-collaboration/reviewer-objections-ledger.md)
- [../agent-collaboration/claims-and-decisions.md](../agent-collaboration/claims-and-decisions.md)
