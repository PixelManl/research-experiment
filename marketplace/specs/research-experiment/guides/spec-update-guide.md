# Spec Update Guide

Specs should evolve when bugs or repeated friction reveal a new rule.

## When to update spec

Update `.trellis/spec/` when:

- the same bug class appears twice;
- a human states a durable preference;
- a new project convention becomes stable;
- a pre-heavy-run review finds a preventable issue;
- a baseline/result invalidation required manual cleanup;
- agent repeatedly misplaces files.

## How to update

1. Put durable rules in the relevant layer.
2. Keep `index.md` concise.
3. Include exact paths.
4. Include good/bad examples.
5. Add tests or validation commands when possible.
6. Remove placeholders or rules that no longer apply.

## Do not update spec for

- one-off personal notes;
- large logs;
- unsettled hypotheses;
- private runtime state;
- outputs that belong in `outputs/`;
- research evidence that belongs in `docs/research-log/`.
