# Reviewer Objections Ledger Contract

Agents tend to over-claim. The objection ledger forces them to preserve counterarguments.

## Required file

```text
docs/research-log/reviewer-objections.md
```

## Format

```markdown
| ID | Task slot | Objection | Evidence needed | Status | Resolution |
|---|---|---|---|---|---|
| OBJ-001 | cvar-sam | second-order term may be negligible | compare first/second-order magnitudes | open | |
```

## When to add an objection

Add or update an objection when:

- a formula assumption is uncertain;
- a baseline may be wrong;
- a metric may not measure the claim;
- a result could be random seed noise;
- a derivation depends on a small term;
- a reviewer would likely challenge the story.

## Rule for changing tone

If the human challenges a claim and AI changes its answer, the AI must update the ledger:

```markdown
## Tone/claim correction

Previous claim:
Challenge:
Revised claim:
Evidence needed:
```

## Example: second-order concern

```markdown
| OBJ-003 | cvar-sam | If first-order gradient is already tiny, Taylor second-order correction may have negligible practical effect | compute first/second-order norm ratio on toy and real batches before parameter sweep | open | |
```

## Forbidden

- Removing objections because they are inconvenient.
- Closing objections without a run/test/report link.
- Continuing a sweep when the highest-risk objection has a cheaper diagnostic.
