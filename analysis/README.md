# Version-controlled analysis

`analysis/` holds durable, reviewable facts exported from Binary Ninja. It replaces the idea of sharing the local analysis database through Git.

## Why the `.bndb` is not committed

A Binary Ninja `.bndb` is the local analysis database. It can be opened directly and may retain snapshots, undo actions, and other analysis state. It is also a binary file that does not merge or review well. The project treats it as private client-derived state under `binaryninja/workspace/`.

## Export requirements

Committed exports belong in `analysis/exports/` and should:

- Use deterministic UTF-8 YAML
- Include a schema version
- Include the target filename, size, and SHA-256
- Use static virtual addresses in a documented format
- Distinguish user conclusions from Binary Ninja auto-analysis
- Preserve confidence and provenance when useful
- Sort records deterministically
- Omit absolute local paths and volatile timestamps
- Round-trip through checked-in scripts under `binaryninja/scripts/`

[`exports/startup.yaml`](exports/startup.yaml) establishes schema version `1`. Additional focused manifests, such as [`exports/network.yaml`](exports/network.yaml), use the same deterministic format. No symbol or conclusion is inherited from archived material without revalidation.
