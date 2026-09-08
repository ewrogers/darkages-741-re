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

[`exports/startup.yaml`](exports/startup.yaml) establishes schema version `1`. Additional focused manifests, such as [`exports/network.yaml`](exports/network.yaml) and [`exports/rendering.yaml`](exports/rendering.yaml), use the same deterministic format. No symbol or conclusion is inherited from archived material without revalidation.

## Durable function records

The `.bndb` is not the collaboration format. It is binary, snapshot-based local state and is intentionally ignored.

Commit analysis that other contributors need in `analysis/exports/` using deterministic YAML. Export files should be reviewable and mergeable. Every export format must include a schema version and the target fingerprint.

For a function, preserve as much of the following as the export supports:

- User-defined project name
- Static virtual address
- Function size or range
- Type or inferred signature
- Confidence
- Short evidence or provenance note

Keep export records sorted deterministically. Avoid absolute local paths, timestamps that change on every run, opaque Binary Ninja object identifiers, or auto-analysis noise. Put the matching exporter and importer in `binaryninja/scripts/`.

Do not invent an export schema during an unrelated task. Establish the first schema alongside the first verified subsystem and test a round trip against a fresh local database.


For the surrounding workflow, see the [contributor handbook](../CONTRIBUTING.md#research-or-correct-a-finding). The [export inventory](exports/README.md) identifies the existing manifests and synchronization script.
