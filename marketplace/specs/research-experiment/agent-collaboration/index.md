# Agent Collaboration Index

This layer defines human-agent collaboration: what AI may execute, what it may draft, what humans must decide, and how to avoid continuing a failed research story.

## Documentation Files

| File | Purpose | When to Read | Priority |
|---|---|---|---|
| [ownership-tiers.md](./ownership-tiers.md) | T1/T2/T3 ownership boundaries | Starting tasks, classifying AI vs human decisions, finishing work | Must Read |
| [reviewer-objections-ledger.md](./reviewer-objections-ledger.md) | Objections, uncertainty, and counter-evidence tracking | Reviewing claims, formulas, baselines, or paper-facing results | Must Read |
| [failure-evidence-ledger.md](./failure-evidence-ledger.md) | Failed runs and invalidated evidence as source-backed records | A run fails, a bug invalidates outputs, or evidence contradicts the story | Must Read |
| [pre-heavy-run-review.md](./pre-heavy-run-review.md) | Independent review before expensive compute | Before heavy runs, large sweeps, or remote jobs | Must Read |
| [external-heavy-model-review.md](./external-heavy-model-review.md) | Explicit heavy-package protocol for external advanced AI review | Packaging high-risk changes, heavy runs, bugs, or claims for a heavy model | Conditional |
| [break-loop-ci.md](./break-loop-ci.md) | Post-bug prevention and minimal CI gates | After fixing bugs or discovering repeated failure modes | Must Read |
| [claims-and-decisions.md](./claims-and-decisions.md) | Claim strength, stop/continue decisions, and human approvals | Making scientific claims, stopping/reframing, or citing outputs | Must Read |

## Quick Navigation by Task

Classifying AI vs human responsibility?

- Read [ownership-tiers.md](./ownership-tiers.md).
- Identify T1 changes AI may execute, T2 drafts requiring human approval, and T3 decisions humans own.
- Record pending T2/T3 decisions in the task ledger or decision file.

Before heavy compute?

- Read [pre-heavy-run-review.md](./pre-heavy-run-review.md).
- Ask an independent reviewer to inspect code, math, configs, smoke evidence, and output paths.
- Do not launch the heavy run until review objections are resolved or explicitly accepted.

Preparing a heavy-package for GPT-5.5 Pro or another external heavy model?

- Read [external-heavy-model-review.md](./external-heavy-model-review.md).
- Package only after explicit user request or approval.
- Use a two-part English prompt: current-problem directed review plus future-direction creative review.
- Treat the heavy model's response as read-only advice until findings are mapped back to files, tests, specs, ledgers, and human-owned decisions.

When a result fails or becomes invalid?

- Read [failure-evidence-ledger.md](./failure-evidence-ledger.md) and [claims-and-decisions.md](./claims-and-decisions.md).
- Preserve failed outputs and update invalidation records.
- State which runs must not support claims.

When AI or human makes a strong claim?

- Read [reviewer-objections-ledger.md](./reviewer-objections-ledger.md) and [claims-and-decisions.md](./claims-and-decisions.md).
- Require source-backed evidence, counter-evidence, and unresolved objections.
- Do not let chat memory substitute for files.

After fixing a bug?

- Read [break-loop-ci.md](./break-loop-ci.md).
- Ask what would prevent this bug class from returning.
- Add a test, checklist item, spec update, or CI gate when appropriate.

## Core Rules Summary

- Conversation is not source of truth; files are.
- AI must surface uncertainty, objections, and stop/reframe signals instead of preserving a hopeful story.
- Heavy compute requires independent review before launch.
- AI may draft T2 scientific content but must not finalize T3 scientific decisions.
- Failed or invalidated results must become evidence, not hidden history.
