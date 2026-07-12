# Guides Index

Operational checklists, not deep code contracts. Keep them short, executable,
and easy to copy into a task or review note.

> Trellis treats `guides/` as shared thinking guides (always listed separately
> from coding layers). Content style: what to consider, not full implementation
> contracts.

## Guidelines Index

| Guide | Description | When to Read |
|-------|-------------|--------------|
| [before-dev-checklist.md](./before-dev-checklist.md) | Pre-development task setup | Before a new task-slot or substantial change |
| [before-heavy-run-checklist.md](./before-heavy-run-checklist.md) | Evidence required before expensive compute | Heavy runs, sweeps, remote jobs, long training |
| [bug-root-cause-retrospective.md](./bug-root-cause-retrospective.md) | Bug classification and prevention follow-up | After fixing a bug or invalidating a result |
| [research-stop-continue-decision.md](./research-stop-continue-decision.md) | Stop, continue, or reframe decisions | Weak, contradictory, costly, or invalidated evidence |
| [spec-update-guide.md](./spec-update-guide.md) | Updating project specs from lessons learned | Repeated bugs, new conventions, project-specific rules |
| [main-journal-protocol.md](./main-journal-protocol.md) | Daily research journal protocol | End of research session or handoff |

## Pre-Development Checklist

- [ ] Before development → [before-dev-checklist.md](./before-dev-checklist.md):
      task-slot, ownership tier, scientific contract, minimum tests, commands, stale-source risks.
- [ ] Before heavy compute → [before-heavy-run-checklist.md](./before-heavy-run-checklist.md)
      plus runtime provenance and agent pre-heavy-run review.
- [ ] Locally correct but possibly globally inconsistent change → also read
      [../research-pitfalls/coupled-logic-drift.md](../research-pitfalls/coupled-logic-drift.md).
- [ ] Weak/contradictory evidence → [research-stop-continue-decision.md](./research-stop-continue-decision.md);
      leave T3 stop/continue to the human owner.
- [ ] End of research day → [main-journal-protocol.md](./main-journal-protocol.md).
- [ ] Guides stay short and point to source files/evidence; do not summarize chat only.

## Quality Check

- [ ] After a bug: retrospective done and prevention landed in the right place
      (test / validation / spec / checklist / CI) via
      [bug-root-cause-retrospective.md](./bug-root-cause-retrospective.md).
- [ ] Repeated lessons updated the smallest relevant spec file
      ([spec-update-guide.md](./spec-update-guide.md)), not only chat memory.
- [ ] Journal/handoff records what changed, failed, is invalid, and is still pending.
- [ ] Guides did not absorb long coding contracts that belong in non-guide layers.
