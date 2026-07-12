# Agent Collaboration Index

Human-agent collaboration: what AI may execute, what it may draft, what humans
must decide, and how to avoid continuing a failed research story.

## Guidelines Index

| Guide | Description | When to Read |
|-------|-------------|--------------|
| [ownership-tiers.md](./ownership-tiers.md) | T1/T2/T3 ownership boundaries | Starting tasks; classifying AI vs human decisions |
| [reviewer-objections-ledger.md](./reviewer-objections-ledger.md) | Objections, uncertainty, counter-evidence | Reviewing claims, formulas, baselines, paper results |
| [failure-evidence-ledger.md](./failure-evidence-ledger.md) | Failed/invalidated evidence as source-backed records | Failed runs, bugs invalidating outputs, contradictions |
| [pre-heavy-run-review.md](./pre-heavy-run-review.md) | Independent review before expensive compute | Heavy runs, large sweeps, remote jobs |
| [external-heavy-model-review.md](./external-heavy-model-review.md) | Explicit heavy-package protocol for external advanced AI | Only with explicit user request/approval |
| [break-loop-ci.md](./break-loop-ci.md) | Post-bug prevention and minimal CI gates | After bug fixes or repeated failure modes |
| [claims-and-decisions.md](./claims-and-decisions.md) | Claim strength, stop/continue, human approvals | Scientific claims, reframing, citing outputs |

## Pre-Development Checklist

- [ ] Classify T1 / T2 / T3 ownership before coding
      ([ownership-tiers.md](./ownership-tiers.md)); record pending T2/T3 decisions in files.
- [ ] Before heavy compute → [pre-heavy-run-review.md](./pre-heavy-run-review.md);
      independent review of code, math, configs, smoke evidence, output paths.
- [ ] External heavy-model packet only after explicit user request/approval
      ([external-heavy-model-review.md](./external-heavy-model-review.md)).
- [ ] Strong claims require objections + evidence records
      ([reviewer-objections-ledger.md](./reviewer-objections-ledger.md),
      [claims-and-decisions.md](./claims-and-decisions.md)).
- [ ] Failed or invalidated runs become ledger evidence, not hidden history
      ([failure-evidence-ledger.md](./failure-evidence-ledger.md)).
- [ ] After bugs → [break-loop-ci.md](./break-loop-ci.md): test, checklist, spec, or CI gate.
- [ ] Conversation is not source of truth; durable facts go to files.

## Quality Check

- [ ] T3 scientific decisions were not finalized by AI alone.
- [ ] Heavy compute had independent review (or explicit human acceptance of open objections).
- [ ] Claims distinguish observation / hypothesis / evidence / decision and cite valid runs.
- [ ] Invalidated results are marked and excluded from paper-facing claims.
- [ ] Preventable bug classes produced a durable prevention update (test/spec/checklist/CI).
- [ ] External heavy-model advice was mapped back to files/tests/specs before acting on it.
