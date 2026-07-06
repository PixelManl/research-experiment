# Run registry and generated indexes are tracked; heavy artifacts are ignored.
# This is also a snapshot-correctness precondition: git snapshots capture
# everything not ignored (see experiment-runtime/run-registry.md).
outputs/**
!outputs/
!outputs/index.md
!outputs/*/
!outputs/*/runs.jsonl
!outputs/*/index.md
data/**
!data/
!data/processed/
!data/processed/**/manifest.json
!data/processed/**/input_hashes.json
