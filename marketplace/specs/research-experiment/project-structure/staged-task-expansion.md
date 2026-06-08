# Staged Task Expansion Protocol

This protocol defines how to keep one Trellis task as the control plane for a continuous research/implementation thread. It replaces PRD-centered ceremony with stage-centered task evolution: the PRD stays useful because it records the evolving stage map, locked decisions, claim boundaries, blockers, and acceptance criteria.

## When to Read

Read this when:

- a research task keeps growing around the same scientific object;
- a failed or No-Go stage becomes the input to a redesign;
- an agent wants to create a new Trellis task for a follow-up that may belong in the current task;
- stage labels such as `A/B/C`, `A1/A2/A3`, `F.1/F.2`, or `G0/G2/G1` are being appended to one task;
- the team needs to decide whether a follow-up is a new task, a new stage, or a substage.

## Core Definition

Staged task expansion means using one Trellis task as the long-lived control plane for a continuous research thread.

When a research or implementation task continues around the same scientific object, code path, and claim boundary, do not create a fragmented new task for every new idea. Append a new Stage to the current Trellis task PRD, and give each Stage its own preregistration or contract, results, review response, and acceptance criteria when needed.

Simple rule:

```text
Do not open a new task for every new idea.
Keep expanding the same task when the scientific object and claim boundary remain continuous.
```

The PRD is not a product-management ceremony. In this template, the PRD is the task control plane: it records the current stage map, locked user decisions, forbidden work, acceptance criteria, and open blockers.

## Trellis Task vs Task-Slot

A Trellis task and a `<task-slot>` serve different purposes.

```text
Trellis task / PRD
└── evolving control plane for stages, decisions, blockers, and acceptance

<task-slot>
├── tests/<task-slot>/
├── scripts/<task-slot>/
├── outputs/<task-slot>/
└── docs/research-log/tasks/<task-slot>.md
```

- The Trellis task controls how the current research thread evolves.
- The `<task-slot>` gives durable filesystem identity to tests, scripts, outputs, and ledgers.
- A single Trellis task usually maps to one active `<task-slot>`, but the task may contain many stages.
- Stable scientific conclusions must eventually be promoted from task-local research notes into the project ledger or output index.

## When to Expand the Current Task

Expand the current Trellis task when most of these are true:

- the scientific object is the same;
- the claim boundary is the same or has been narrowed by earlier evidence;
- the code path, test path, benchmark, or output family is continuous;
- the new stage depends on prior stage results;
- a No-Go, review finding, or failed result becomes the input to the next stage;
- the follow-up is a natural continuation: preregistration, contract, implementation, review, hardening, route policy, schema, protocol, or test contract;
- the work does not need independent parallel management.

Example expansion:

```text
Stage D No-Go
  -> Stage E redesign
  -> Stage F exact reference implementation
  -> Stage F.1 hardening
  -> Stage G0 route policy
  -> Stage G2 packet schema / identity contract
  -> Stage G1 fixed-lag sync/window test contract
```

Although these stages may become numerous, they belong in one task when they keep refining the same object and boundary.

## When to Create a New Trellis Task

Create a new Trellis task when any of these are true:

- the scientific object changes;
- the claim target changes;
- a new output family, benchmark family, or evaluation family is introduced;
- the code path is mostly independent;
- the new task can be completed without the current task control plane;
- the current task is complete and archived;
- the work changes risk level enough to need separate governance;
- the work moves from a synthetic sandbox to a calibrated simulator, economic environment, deployment setting, or real data environment;
- the task changes from an exactness route into a service objective, selector benchmark, performance claim, or another different claim family.

Do not create a new task only because:

- the previous stage failed;
- a reviewer found blockers;
- stage labels are becoming long;
- the next stage is not a code implementation;
- the execution order is nonlinear.

## Stage Identity

Stage IDs are local to one Trellis task. They are not global milestones and do not need a universal meaning across projects.

Allowed examples:

```text
A
A1
A2
A3
B
C
D
E
F
F.1
F.2
G0
G1
G2
```

Use simple letters for the main sequence. Split any stage into local substages when the subproblem needs clearer preregistration, contract, results, review, or acceptance criteria. This is not limited to later stages: `A` may become `A1/A2/A3`, `F` may become `F.1/F.2`, and `G` may become `G0/G1/G2`.

Important rule:

```text
Any stage may be decomposed into local substages when the substage boundary is useful.
Substage labels are local control-plane labels, not global chronological order.
```

For example, `G0 -> G2 -> G1` is valid if:

- `G0` selects a route or policy;
- `G2` defines a packet, schema, identity, or availability layer needed first;
- `G1` depends on `G2` and defines a fixed-lag, sync-window, or algorithm test contract.

When execution order is nonlinear, or when a main stage is split into local substages such as `A1/A2/A3`, the PRD must record dependency order explicitly.

## PRD Requirements

When a Trellis task uses staged expansion, the PRD must stay current. It should not be rewritten from scratch each time. Append stages and update the control sections.

Minimum PRD sections:

```markdown
## Status

Current stage:
Completed stages:
Next blocked stage:

## User Decisions Locked

- ...

## Stage Map

| Stage | Type | Status | Claim Boundary | Primary Artifact |
|---|---|---|---|---|

## Acceptance Criteria by Stage

### Stage <id> Acceptance Criteria

- [ ] ...

## Open Blockers Before Next Stage

- ...

## Forbidden Work

- ...
```

The PRD should preserve locked decisions such as:

```text
Stage G0 selects the G1/G2 deployable exactness path.
Stage G2 defines atom-packet identity and availability.
Stage G1 depends on G2 and expands sync-anchor/window tests.
```

The PRD must also preserve forbidden work. This prevents later stages from silently drifting into claims or implementation routes that were explicitly blocked.

## Acceptance Criteria by Stage

Use separate acceptance criteria for each stage. Do not collapse all stages into one large checklist.

Example:

```markdown
## Stage G0 Acceptance Criteria

- [x] Route selected.
- [x] Packet identity policy recorded.
- [x] Sync/window assumptions recorded.

## Stage G2 Acceptance Criteria

- [x] Packet schema implemented.
- [x] `received_t` excluded from factor identity.
- [x] Online/offline packet availability tests pass.

## Stage G1 Acceptance Criteria

- [x] Sync-anchor schema specified.
- [x] Late atom policy specified.
- [x] Deterministic fixture list specified.
```

Each stage must be reviewable on its own even when the whole Trellis task remains in progress.

## Research File Naming

Store stage-local research files under the Trellis task's `research/` directory when available.

Use this naming pattern:

```text
research/stage-<id>-<short-topic>-<doc-type>.md
```

Recommended `<doc-type>` values:

```text
prereg-plan
contract
test-contract
results
review-response
external-review-response
hardening-results
route-plan
packet-policy
```

Examples:

```text
research/stage-d-dynamic-private-history-results.md
research/stage-e-factor-graph-contract.md
research/stage-f-factor-graph-reference-results.md
research/stage-f1-external-review-hardening-results.md
research/stage-g0-route-acceptance-and-packet-policy.md
research/stage-g2-atom-packet-contract-results.md
research/stage-g1-fixed-lag-sync-window-test-contract.md
```

Task-local `research/` files are working evidence. Stable conclusions must be promoted into durable project records such as:

```text
docs/research-log/tasks/<task-slot>.md
outputs/<task-slot>/index.md
docs/research-log/source-of-truth.md
docs/research-log/invalidated-results.md
```

## Required Stage Artifacts

Not every stage needs every artifact. Choose the minimum artifacts needed for the stage type and risk level.

Use:

- preregistration or intent before risky implementation;
- contract before code when semantics matter;
- test contract before implementation when acceptance must be fixed;
- results after implementation, derivation, or experiment;
- review response after internal or external audit;
- hardening note after fixes or adversarial tests;
- updated acceptance criteria in the PRD.

A No-Go stage must still produce an artifact. It becomes input to the next stage's contract.

## Stage Types

| Stage Type | Purpose |
|---|---|
| Smoke | Deterministic infrastructure validation |
| Falsification | Prove or disprove a route, claim, or exactness assumption |
| Redesign | Redesign math or architecture after No-Go |
| Reference Implementation | Implement an exact reference object or oracle |
| Hardening | Apply external review fixes, adversarial tests, or regression hardening |
| Route Contract | Select the next route and define forbidden work |
| Protocol / Schema | Define packet, identity, availability, interface, or sync contract |
| Test Contract | Define acceptance tests before implementation |
| Review Response | Map reviewer objections to fixes, blockers, rejected advice, or human decisions |
| Claim Boundary | Narrow or update allowed wording, forbidden wording, and stop rules |

A stage may be purely conceptual or contractual. Do not force every stage to contain implementation.

## Claim Boundary Rule

Every stage document must include a claim boundary when the stage can affect interpretation.

Use this format:

```markdown
## Claim Boundary

Allowed wording:
- ...

Forbidden wording:
- ...

Stop rules:
- ...
```

Example:

```markdown
Allowed wording:
- Packet-layer identity and availability contract is implemented.

Forbidden wording:
- Fixed-lag online algorithm is exact.
- Bounded-memory exactness is proven.
- Cross-covariance route is validated.
- Performance claim is supported.

Stop rules:
- Stop if offline/online parity fails.
- Stop if packet identity depends on `received_t`.
```

This rule prevents a narrow stage result from being reused as a broader scientific claim.

## No-Go as an Asset

A No-Go stage is not a failed task. It is a valid research artifact.

A No-Go must record:

- what was tested, derived, or reviewed;
- why the route failed;
- what claims are now forbidden;
- what assumptions are invalidated;
- what the next stage must preserve or avoid.

Do not delete No-Go evidence. Later stages should cite it as a root constraint.

## Nonlinear Stage Order

Stage IDs and substage IDs do not require execution in alphabetical or numerical order. Dependency order matters more than label order.

If execution is nonlinear, record:

```markdown
## Stage Dependency Order

- Stage G0 selects route policy.
- Stage G2 defines packet identity and availability.
- Stage G1 depends on G2 and defines fixed-lag sync/window tests.
```

A nonlinear order is acceptable only when the dependency explanation is explicit.

## `implement.jsonl` and `check.jsonl`

Use task context logs to keep implementation and review grounded.

### `implement.jsonl`

Record implementation and result artifacts:

```text
src/...
tests/...
research/stage-g2-atom-packet-contract-results.md
outputs/<task-slot>/...
```

Purpose:

```text
Tell the implementation pass what was actually changed or produced.
```

### `check.jsonl`

Record contracts, review inputs, claim boundaries, and external audits:

```text
research/stage-g0-route-acceptance-and-packet-policy.md
research/stage-g1-fixed-lag-sync-window-test-contract.md
research/stage-f-55pro-external-review-response.md
.trellis/spec/...
```

Purpose:

```text
Tell the checking pass what contract, review, and forbidden boundaries must be enforced.
```

## Commit Rule

Prefer one coherent commit per completed stage or substage when durable files, tests, specs, or research artifacts change.

A coherent stage commit should include:

- the PRD stage update;
- relevant research artifact;
- implementation or tests when applicable;
- result or review response when applicable;
- updated task-slot ledger or output index when the result becomes durable project evidence.

Do not commit speculative stage notes as final evidence unless they are clearly labeled as preregistration, draft, or rejected route.

## Related Specs

- [task-slots.md](./task-slots.md)
- [tests-organization.md](./tests-organization.md)
- [scripts-organization.md](./scripts-organization.md)
- [outputs-organization.md](./outputs-organization.md)
- [../agent-collaboration/ownership-tiers.md](../agent-collaboration/ownership-tiers.md)
- [../agent-collaboration/claims-and-decisions.md](../agent-collaboration/claims-and-decisions.md)
- [../agent-collaboration/external-heavy-model-review.md](../agent-collaboration/external-heavy-model-review.md)
