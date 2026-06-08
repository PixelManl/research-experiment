# External Heavy-Model Review

This contract defines how to prepare a **heavy-package** for an external heavy model such as GPT-5.5 Pro, Claude Opus, Gemini Deep Research, or another high-cost reviewer. A heavy-package is not a raw zip dump and not a chat transcript. It is a sanitized, runnable, evidence-grounded review packet with a two-part prompt: directed review of the current problem and creative exploration of future directions.

## When to Use

Use this protocol only when the user explicitly asks for it or approves it after an agent recommendation.

Appropriate triggers include:

- high-risk semantic changes, especially changes to action transforms, log-probability, entropy, reward, loss, objective, baseline, metric, figure, or claim logic;
- expensive compute, large sweeps, remote GPU jobs, or formal multi-seed runs;
- paper-facing claims, table generation, figure interpretation, or final report conclusions;
- complex bugs that may invalidate prior outputs;
- architectural uncertainty where process, metrics, diagnostics, runtime, and scripts boundaries may be confused;
- repeated reviewer objections that need deeper independent reasoning.

Do not use heavy-package review for routine T1 cleanup, typo fixes, simple read-only inspection, or small local edits that do not affect scientific meaning.

## Invocation Policy

Heavy-package review is **explicit-invocation only**.

Agents may recommend it when high-risk research conditions appear, but they must not create, export, upload, or send a heavy-package unless the user requests or approves it.

Valid user requests include phrases such as:

- `prepare a heavy-package`;
- `package this for GPT-5.5 Pro`;
- `make an external heavy-model review packet`;
- `run the AI handoff packager`;
- `prepare a logic-chain review package`.

If a skill is installed, the skill may inject this protocol and provide helper commands. The skill still must preserve explicit invocation: recommendation is allowed; silent packaging is not.

## Definition

A heavy-package is an explicitly invoked external heavy-model review packet. It packages sanitized project context together with a designed prompt.

A valid heavy-package should be:

- **self-contained**: the reviewer can understand the objective, repository context, task-slot, and evidence boundaries without hidden chat history;
- **runnable when possible**: install, test, smoke, and minimal reproduction commands are included or explicitly marked unavailable;
- **scoped**: files are selected by review profile and task concern, not by dumping the whole repository;
- **sanitized**: secrets, credentials, private data, large outputs, checkpoints, and generated caches are excluded by default;
- **evidence-grounded**: findings must be tied back to paths, diffs, tests, run ids, output indexes, specs, and ledgers;
- **read-only**: external model output is advice until a main agent maps it back to files, tests, specs, ledgers, and human-owned decisions.

## Prompt Philosophy

A heavy-package prompt must contain two parts.

### Part A: Current Problem / Directed Review

This section is narrow, grounded, and falsifiable. It protects the user's immediate intent.

Use fixed questions to force the model to answer the known risk directly:

- What exact mechanism, assumption, or semantic contract is under review?
- Is the current implementation consistent with that contract?
- Which downstream logic should have changed with it?
- Are tests, metrics, diagnostics, baselines, outputs, reports, and claims synchronized?
- What blockers must be fixed before trusting this work?
- What warnings should be recorded?
- What tests, smoke commands, or cheaper checks should be run next?

Expected output from this part is structured and decision-oriented: `pass`, `warn`, or `block`, with cited evidence.

### Part B: Future Direction / Creative Review

This section is open-ended and insight-seeking. It buys additional reasoning value from the heavy model.

Ask the model to look beyond the immediate bug or patch:

- What hidden assumptions are most likely to fail later?
- What cheaper falsification tests could save expensive compute?
- What alternative design would make the project harder for agents to misuse?
- What future research direction looks promising or risky?
- What new spec rule, pitfall, doctor check, or regression test should be added?
- What human-owned decisions must be clarified before continuing?
- If the reviewer had only one follow-up question, what should it ask?

Creative suggestions must still be labeled. If a suggestion goes beyond the package evidence, the reviewer must mark it as speculation.

Core principle:

```text
Use fixed questions to protect intent. Use open questions to buy insight.
```

## Recommended Response Budget

Set the response budget by review profile:

| Profile | Directed Current Problem | Creative Future Direction |
|---|---:|---:|
| `logic-chain-review` | 70% | 30% |
| `heavy-run-review` | 60% | 40% |
| `bug-review` | 70% | 30% |
| `paper-claim-review` | 70% | 30% |
| `architecture-review` | 50% | 50% |

Do not allow the model to skip future-direction analysis just because it found current blockers. Current blockers make future-risk discovery more valuable, not less.

## Required Packet Contents

A heavy-package should generate a review directory such as:

```text
handoff-packages/
  <timestamp>-<profile>/
    handoff.md
    manifest.json
    file-list.txt
    git-status.txt
    repo-diff.patch
    tree.txt
    package.zip
```

### `handoff.md`

The main English prompt for the heavy model. It contains objective, repository context, how to run, relevant files, known constraints, directed questions, creative questions, and required output format.

### `manifest.json`

Machine-readable record of what was packaged:

- schema version;
- profile;
- creation time;
- root path;
- branch, commit, and dirty state;
- task-slot when known;
- included files with size and hash;
- generated support files;
- excluded files and reasons;
- size limits.

### `file-list.txt`

Human-readable list of included files.

### `git-status.txt`

Captured `git status --short --branch` output.

### `repo-diff.patch`

Current diff when available. If the worktree is clean, record that explicitly.

### `tree.txt`

A compact tree of relevant project paths.

### `package.zip`

The sanitized code and document package to upload or pass to the heavy model.

## Default Exclusions

Exclude these by default:

```text
.git/
.env
.env.*
*.key
*.pem
*.pt
*.pth
*.ckpt
*.onnx
*.npy
*.npz
*.parquet
*.csv
data/
outputs/
wandb/
mlruns/
node_modules/
.venv/
__pycache__/
```

Including `data/`, `outputs/`, checkpoints, or large generated files requires explicit user approval and a size limit. Never package secrets.

## Review Profiles

### `logic-chain-review`

Use when a local change may shift downstream scientific meaning.

Include relevant:

- git diff and changed files;
- source files implementing the mechanism;
- tests and configs for the task-slot;
- task ledger and output index when relevant;
- [../research-pitfalls/coupled-logic-drift.md](../research-pitfalls/coupled-logic-drift.md);
- [../research-code/math-formula-mapping.md](../research-code/math-formula-mapping.md);
- [../research-code/numerics.md](../research-code/numerics.md);
- [../research-code/validation-assertions.md](../research-code/validation-assertions.md);
- [../experiment-modules/evaluation-and-baselines.md](../experiment-modules/evaluation-and-baselines.md);
- [claims-and-decisions.md](./claims-and-decisions.md).

Directed questions must ask whether log-probability, entropy, action transforms, losses, rewards, metrics, diagnostics, baselines, outputs, reports, and claims remain synchronized.

### `heavy-run-review`

Use before expensive compute.

Include relevant:

- run script;
- Hydra config;
- smoke result;
- test result;
- provenance plan;
- output path plan;
- task ledger;
- baseline ledger;
- reviewer objections;
- [pre-heavy-run-review.md](./pre-heavy-run-review.md);
- [../guides/before-heavy-run-checklist.md](../guides/before-heavy-run-checklist.md).

Directed questions must ask whether evidence is sufficient before launch and what cheaper falsification test should run first.

### `bug-review`

Use for complex bugs, failed tests, or potential historical invalidation.

Include relevant:

- traceback or failing output;
- failing test;
- related source and configs;
- git diff;
- invalidated-results ledger;
- bug retrospective when available.

Directed questions must ask root cause, invalidated outputs, regression tests, and spec updates.

### `paper-claim-review`

Use before paper-facing claims, tables, figures, or report conclusions.

Include relevant:

- report or claim draft;
- figures and tables index;
- source-of-truth notes;
- baseline ledger;
- invalidated-results ledger;
- outputs index;
- run ids;
- [claims-and-decisions.md](./claims-and-decisions.md).

Directed questions must ask which claims are directly supported, which overreach, and which caveats must be stated.

### `architecture-review`

Use for project structure and long-term agent-maintainability review.

Include relevant:

- README;
- compact tree;
- source layout;
- scripts layout;
- tests layout;
- configs;
- dependency files;
- selected specs.

Directed questions must ask whether reusable methods, task-specific execution, output writing, metrics, diagnostics, and provenance responsibilities are separated clearly.

## Standard `handoff.md` Template

````markdown
# External Heavy-Model Review Packet

## Role

You are an external research-engineering reviewer. Review the attached package in English. Prioritize correctness, evidence, hidden failure modes, and useful future directions over politeness.

## Review Mode

This packet has two goals:

1. Directed review of the current problem.
2. Creative exploration of future risks and directions.

Answer both parts.

## Repository Context

- Project:
- Task-slot:
- Branch:
- Commit:
- Dirty working tree:
- Review profile:

## Objective

...

## Current Problem

...

## Why This Needs Heavy Review

...

## How to Run

Install:

```bash
...
```

Tests:

```bash
...
```

Smoke:

```bash
...
```

Minimal reproduction:

```bash
...
```

If a command is unavailable, say why.

## Relevant Files

| Path | Why Included |
|---|---|
| ... | ... |

## Known Constraints

- Do not assume missing files are irrelevant.
- Do not approve claims without run evidence.
- Treat invalidated results as invalid.
- Distinguish blockers, warnings, and speculative ideas.
- Do not propose broad rewrites unless they directly reduce research risk.
- If a future-direction idea goes beyond the package, label it as speculation.

## Part A: Current Problem / Directed Review

Answer these fixed questions:

1. What is the core mechanism or scientific assumption under review?
2. Is the implementation consistent with that assumption?
3. Which downstream logic should be synchronized?
4. Are tests, metrics, diagnostics, baselines, outputs, reports, and claims consistent?
5. What are the blockers?
6. What are the warnings?
7. What commands or tests should be run before trusting this work?

## Part B: Future Direction / Creative Review

After the directed review, explore:

1. What hidden assumptions may fail later?
2. What cheaper falsification tests should be run before expensive compute?
3. What alternative design would reduce future agent mistakes?
4. What future research direction seems promising or risky?
5. What spec rule, pitfall, doctor check, or regression test should be added?
6. What human-owned decisions must be clarified?
7. What would you ask if you had one follow-up question?

## Required Output Format

Return:

1. Executive verdict: `pass | warn | block`
2. Current-problem blockers
3. Current-problem warnings
4. Required tests or commands
5. Evidence gaps
6. Future-direction risks
7. Creative future directions
8. Suggested spec, pitfall, doctor, or test updates
9. Human questions
10. Confidence limits
````

## Handling Heavy-Model Output

The external heavy model does not write project truth.

After receiving its response, the main agent must:

1. separate blockers, warnings, creative ideas, and speculation;
2. map each actionable finding to files, tests, specs, ledgers, or run ids;
3. reject or mark unsupported advice that cannot be grounded;
4. record unresolved reviewer objections when evidence is missing;
5. ask humans to decide T2/T3 scientific questions;
6. update code, tests, specs, or ledgers only after normal review rules are satisfied.

A heavy model saying `pass` is not enough to launch expensive compute. The project still needs smoke, tests, provenance, output path, valid evidence, and human gates.

## Related Specs

- [ownership-tiers.md](./ownership-tiers.md)
- [pre-heavy-run-review.md](./pre-heavy-run-review.md)
- [reviewer-objections-ledger.md](./reviewer-objections-ledger.md)
- [claims-and-decisions.md](./claims-and-decisions.md)
- [../research-pitfalls/coupled-logic-drift.md](../research-pitfalls/coupled-logic-drift.md)
- [../guides/before-heavy-run-checklist.md](../guides/before-heavy-run-checklist.md)
