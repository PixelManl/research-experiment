# Directory Layout Contract

## When to Read

Read this before:

- initializing or adapting a repository to this spec;
- adding new top-level directories or root-level files;
- deciding whether code belongs in `src/<package>/`, `scripts/`, `tests/`, `outputs/`, or `docs/`;
- reviewing misplaced task-specific glue or generated artifacts.

## Required shape

```text
.
├── src/<package>/
├── configs/
├── scripts/
├── tests/
├── outputs/
│   └── <task-slot>/
│       └── <YYYY-MM-DD>/
├── data/
├── docs/
│   ├── main/
│   │   └── main.md
│   └── research-log/
│       ├── index.md
│       ├── baselines.md
│       ├── source-of-truth.md
│       ├── invalidated-results.md
│       ├── reviewer-objections.md
│       ├── decisions/
│       ├── tasks/
│       ├── reports/
│       └── equation-maps/
└── .trellis/spec/
```

## Rules

### Source code

`src/<package>/` contains reusable research methods only, not one-off experiment glue.

Required shared modules when applicable:

```text
src/<package>/
├── policy/        # network architectures, actor-critic heads, trust models
├── runner/        # environment interaction, rollout loops, buffers
├── process.py       # reusable heavy processing for metrics/diagnostics; not an entrypoint
├── metrics.py       # pure or near-pure metric computation
├── diagnostics.py   # debug-only checks, plots, expensive probes
├── numerics.py      # safe numerical primitives
├── schema.py        # dataclass / NamedTuple contracts
├── validate.py      # precondition and invariant checks
├── plotting.py      # shared figure styles and subplot builders
└── provenance.py    # git/config/env capture helpers
```

### Configs

`configs/` is the only official experiment configuration surface.

```text
configs/
├── config.yaml
├── schema.py
├── task/
├── experiment/
├── debug/
└── hydra/
```

### Tests, scripts, outputs

Use the same `<task-slot>` everywhere:

```text
tests/<task-slot>/
scripts/<task-slot>/
outputs/<task-slot>/
docs/research-log/tasks/<task-slot>.md
```

## Forbidden

- Adding task-specific Python files to repository root.
- Adding one-off plotting, statistics, or analysis scripts directly under `src/<package>/`.
- Using `src/<package>/process.py` as a run entrypoint or hiding Hydra/argparse/output-directory ownership there.
- Creating `tmp.py`, `run2.py`, `final_final.py`, `old_impl.py`, or large commented-out blocks.
- Using conversation memory as the only record of a baseline change or invalid result.

## Required when adding a new task-slot

Create or update:

```text
tests/<task-slot>/index.md
scripts/<task-slot>/index.md
outputs/<task-slot>/index.md
docs/research-log/tasks/<task-slot>.md
```

If one of these is unnecessary, write a one-line reason in the nearest parent index.
