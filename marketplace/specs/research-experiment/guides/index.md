# Guides Index

Guides are operational checklists, not deep code contracts. Keep them short, executable, and easy to copy into a task or review note.

## Documentation Files

| File | Purpose | When to Read | Priority |
|---|---|---|---|
| [before-dev-checklist.md](./before-dev-checklist.md) | Pre-development task setup | Before implementing a new task-slot or substantial change | Must Read |
| [before-heavy-run-checklist.md](./before-heavy-run-checklist.md) | Evidence required before expensive compute | Before heavy runs, sweeps, remote jobs, or long training | Must Read |
| [bug-root-cause-retrospective.md](./bug-root-cause-retrospective.md) | Bug classification and prevention follow-up | After fixing a bug or invalidating a result | Must Read |
| [research-stop-continue-decision.md](./research-stop-continue-decision.md) | Stop, continue, or reframe decisions | When evidence is weak, contradictory, costly, or invalidated | Must Read |
| [spec-update-guide.md](./spec-update-guide.md) | Updating project specs from lessons learned | When a repeated bug, new convention, or project-specific rule appears | Conditional |
| [main-journal-protocol.md](./main-journal-protocol.md) | Daily research journal protocol | At the end of a research session or before handoff | Conditional |

## Quick Navigation by Task

Before starting development?

- Read [before-dev-checklist.md](./before-dev-checklist.md).
- Confirm task-slot, ownership tier, scientific contract, minimum tests, commands, and stale-source risks.

Before launching heavy compute?

- Read [before-heavy-run-checklist.md](./before-heavy-run-checklist.md), [../experiment-runtime/provenance.md](../experiment-runtime/provenance.md), and [../agent-collaboration/pre-heavy-run-review.md](../agent-collaboration/pre-heavy-run-review.md).
- Confirm smoke evidence, config/provenance, review, expected cost, and stop criteria.

After fixing a bug?

- Read [bug-root-cause-retrospective.md](./bug-root-cause-retrospective.md).
- Classify the bug and add prevention where it belongs: test, validation, spec, checklist, or CI.

When evidence is weak or contradictory?

- Read [research-stop-continue-decision.md](./research-stop-continue-decision.md).
- Compare evidence, counter-evidence, compute cost, and the smallest next diagnostic.
- Leave T3 stop/continue decisions to the human owner.

When project conventions change?

- Read [spec-update-guide.md](./spec-update-guide.md).
- Update the smallest relevant spec file instead of relying on chat memory.

At the end of a research day?

- Read [main-journal-protocol.md](./main-journal-protocol.md).
- Record what changed, what failed, what is invalid, and what decision is pending.

## Core Rules Summary

- A guide should be short enough to use during real work.
- Guides should point to source files and evidence, not summarize chat history.
- When a lesson repeats, update the spec or checklist so the next agent can inherit it.
