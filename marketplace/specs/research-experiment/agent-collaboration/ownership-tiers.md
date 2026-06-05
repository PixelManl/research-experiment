# Ownership Tiers Contract

The research lead must remain the scientific owner. AI is a collaborator, implementer, reviewer, and organizer.

## When to Read

Read this before:

- starting or finishing any task;
- deciding whether AI may execute, draft, or must defer;
- changing baselines, metrics, outputs, figures, or claims;
- recording human approvals or pending T2/T3 decisions.

## T1 — AI may execute after normal review

AI can directly implement or modify:

- task-scoped tests;
- task-scoped scripts;
- plotting scripts from approved data;
- logging/provenance helpers;
- Hydra configs following existing schema;
- metric code with explicit formula;
- cleanup of dead code;
- smoke/dry run plumbing;
- verify main.md narrative against file evidence.

Required: tests or smoke command must pass, and indexes must be updated.

## T2 — AI may draft; human must approve before heavy use

AI can draft but not finalize:

- new algorithm variants;
- paper formula translation;
- baseline definitions;
- new evaluation metrics;
- invalidating prior results;
- figure/table intended for a paper;
- changing output validity states.

Required: human approval line in ledger or task report.

## T3 — Human-owned decisions

AI must not decide alone:

- final scientific claim;
- whether a baseline is “correct enough”;
- whether to spend major compute;
- whether to stop/reframe the project;
- paper narrative;
- mathematical proof or core derivation acceptance.

AI must provide evidence and objections, then ask for human decision or record that the decision is pending.

## Anti-hallucination trigger

If human or AI says “I think the baseline is correct” without file evidence, AI must respond with:

```text
Please point to the baseline ledger entry, config, implementation path, and validation run. If they do not exist, this is not a source-backed baseline yet.
```

## Required task summary

Every task finish must include:

```markdown
Ownership summary:
- T1 changes completed:
- T2 drafts needing human approval:
- T3 decisions not made by AI:
```
