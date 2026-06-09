# Pitfall: Route Value Drift

## When to Read

Read this when a research route keeps expanding through correct implementations, exact references, protocols, benchmark controls, or infrastructure, but the result still does not support the original value question.

## Why it matters

Route Value Drift happens when a research route continues through locally correct stages while the original value question is no longer being tested. The route may produce passing tests, exact references, clean artifacts, controlled benchmarks, or careful no-claim flags, but those outputs still may not show that the route changes a value-bearing judgment.

In short:

```text
Correct artifact != valuable route.
No-claim guard != value evidence.
Completed stage != continuation warrant.
```

This pitfall is not specific to RL. RL is a common example because policy value depends on action and reward, not on posterior exactness or model elegance. The same failure appears in forecasting, online learning, data recovery, simulation, benchmark design, uncertainty estimation, theorem-guided modeling, and protocol engineering.

## Value-bearing judgment

A value-bearing judgment is the downstream choice or conclusion that would change if the route succeeds.

Examples:

- choosing an action, policy, allocation, intervention, or design;
- selecting a model, architecture, dataset, simulator, or protocol;
- deciding whether to continue, stop, deploy, publish, or run heavy compute;
- supporting, weakening, or narrowing a scientific claim;
- improving a metric that matters to the research objective, not only an intermediate diagnostic;
- reducing cost, risk, uncertainty, compute, communication, failure rate, or invalid claim risk.

If the route cannot name a value-bearing judgment, the next stage is not justified.

## Typical failure pattern

A common pattern is:

```text
1. Start with a value hypothesis.
2. Find that a simple implementation or early fixture is insufficient.
3. Repair the route with a more exact model, protocol, reference, or learner.
4. Make the repair deployable, online, benchmarkable, or auditable.
5. Add control-plane infrastructure to protect future claims.
6. Realize that the original value question was never re-tested.
```

The route did not fail because every step was wrong. It failed because each step was locally justified while the global value warrant became weaker, untested, or irrelevant.

## Typical symptoms

- A stage result is implementation-correct but still insufficient to support the intended claim.
- A more exact method improves an intermediate quantity but does not show downstream value.
- A model, dataset, simulator, or environment substrate may not support the assumed intervention.
- A simple, conservative, or stale baseline may already be decision-sufficient.
- The next stage mainly exists because the previous stage completed.
- The task shifts from "is this useful?" to "how do we make this technically correct?"
- Online protocols, benchmark control planes, or expensive infrastructure appear before route value is shown.
- The research claim depends on a long causal chain with unstable intermediate links.
- Passing tests are used as evidence that the route is valuable, rather than only evidence that the artifact works as designed.

## Route Value Audit triggers

Trigger a Route Value Audit before continuing when any of these happen:

- a No-Go or failed result becomes input to a more complex repair route;
- an exact reference, stronger model, or better diagnostic succeeds, but its decision or claim value is unshown;
- a new stage would increase mathematical exactness, protocol complexity, benchmark scope, compute cost, or control-plane infrastructure;
- the current result is correct but the planned paper, report, deployment, or scientific claim remains unsupported;
- a strong simple baseline could already be sufficient;
- a dataset, model, simulator, or environment property undermines the original value chain;
- an agent proposes the next stage because it is the natural continuation, not because it has a value warrant.

## Route Value Audit checklist

Before continuing the route, answer:

1. What was the original value question?
2. What claim, decision, judgment, or outcome is this route supposed to improve?
3. What intermediate quantity improved, and why should that matter?
4. What is the shortest causal chain from this result to value?
5. Which link in that chain is currently unsupported?
6. What strong simple baseline might already be sufficient?
7. What is the minimum discriminating test?
8. What result would kill, narrow, or downgrade this route?
9. What infrastructure must not be built until value is shown?
10. Is the next stage proving value, repairing correctness, or expanding infrastructure?

If the next stage is mainly repairing correctness or expanding infrastructure, it must state why that work is still necessary for the value-bearing judgment.

## Minimum discriminating test

A Route Value Audit should define the smallest test that can distinguish:

```text
route has value
```

from:

```text
route is technically correct but unnecessary
```

The test should compare against the strongest simple baseline available. It should avoid building new infrastructure unless that infrastructure is required to answer the value question.

Good minimum tests often use controlled fixtures, oracle inputs, fixed predictors, synthetic ablations, or upper-bound references to isolate the value chain before building the full system.

## Forbidden agent behavior

Agents must not:

- treat a completed stage as automatic justification for the next stage;
- convert every No-Go into a more complex repair route;
- build benchmark or control-plane infrastructure before route value is shown;
- use passing tests as evidence that the research route is valuable;
- hide weak value evidence behind no-claim flags;
- optimize intermediate exactness, elegance, prediction quality, or protocol consistency without a value warrant;
- create a new Trellis task or append a new stage to avoid asking whether the route should continue.

## Recovery action

If Route Value Drift is detected:

1. stop adding implementation or infrastructure stages;
2. restate the original value question in one paragraph;
3. list the current artifacts that are correct but value-insufficient;
4. identify the strongest simple baseline;
5. design the minimum discriminating test;
6. mark infrastructure-only work as blocked until value evidence exists;
7. decide whether the route should continue, narrow, downgrade, split, or stop;
8. preserve No-Go and value-insufficient results as research assets.

## Relationship to staged task expansion

Staged task expansion prevents task fragmentation. It must not become a mechanism for indefinite route continuation.

Important rule:

```text
Same task identity does not justify the next stage.
```

A continuous task still needs a continuation warrant. Before appending a stage that increases exactness, model complexity, protocol complexity, benchmark scope, or control-plane infrastructure, the PRD must record the value-bearing judgment and the reason this stage still tests or protects it.

## Abstract examples

### Exactness route

A route starts with the hypothesis that a more accurate latent-state estimate will improve downstream decisions. Early fixtures support the idea. Later tests show that a marginal approximation is not exact, so the route shifts into exact references, online compression, and protocol design.

The repair work may be correct, but the route has drifted if it never tests whether exactness changes the downstream decision, outcome, or claim compared with a simple conservative baseline.

### Online learning route

A route starts with the hypothesis that an intervention can preserve high-uncertainty data sources, making online learning or recovery more useful. The route drifts if the dataset substrate, predictor stability, or intervention-outcome link is not validated before building a joint online-learning/control system.

The key question is not whether the online learner can be implemented. The key question is whether the intervention changes the value-bearing outcome compared with a simple baseline under data conditions that actually support the claim.

## Required reads

- [staged-task-expansion.md](../project-structure/staged-task-expansion.md)
- [evaluation-and-baselines.md](../experiment-modules/evaluation-and-baselines.md)
- [claims-and-decisions.md](../agent-collaboration/claims-and-decisions.md)
- [research-stop-continue-decision.md](../guides/research-stop-continue-decision.md)
- [failure-evidence-ledger.md](../agent-collaboration/failure-evidence-ledger.md)

## CI / review gate

Warn or block when:

- a new stage expands route complexity without a value-bearing judgment;
- a No-Go is followed by a more complex repair without a Route Value Audit;
- benchmark or infrastructure work starts before the minimum discriminating test is defined;
- a report uses implementation correctness, exactness, or no-claim flags as a substitute for value evidence;
- a simple baseline is missing from the stop/continue decision.
