# Figures Contract

Figures are scientific artifacts. Plotting should be reproducible, not manual.

## Required shared module

```text
src/<package>/plotting.py
```

## Figure specs

Define shared layouts centrally:

```python
@dataclass(frozen=True)
class FigureSpec:
    name: str
    figsize: tuple[float, float]
    nrows: int
    ncols: int
    sharex: bool = False
    sharey: bool = False

FIGURE_SPECS = {
    "one_by_three": FigureSpec("one_by_three", figsize=(9.0, 2.8), nrows=1, ncols=3),
    "one_by_two": FigureSpec("one_by_two", figsize=(6.0, 2.8), nrows=1, ncols=2),
}
```

## Plot script location

Task-specific figure scripts belong in:

```text
scripts/<task-slot>/plot.py
```

They must read from:

- a run directory;
- a processed data manifest;
- or a curated `paper/results_manifest.yaml`.

## Output location

Exploratory figures:

```text
outputs/<task-slot>/<YYYY-MM-DD>/<run-id>/figures/
```

Paper/report figures:

```text
paper/figures/
```

Only copy to `paper/figures/` after human approval and a report/claim link.

## Required figure metadata

Each figure must have either a sidecar JSON or be recorded in output index:

```json
{
  "source_run": "outputs/ppo-handwritten/2026-05-31/143012-smoke",
  "script": "scripts/ppo-handwritten/plot.py",
  "config": ".hydra/config.yaml",
  "data_manifest": "..."
}
```

## Forbidden

- manual edits as the only source of a figure;
- plotting from a stale CSV with no manifest;
- changing style independently in every script;
- paper figures that cannot be regenerated.
