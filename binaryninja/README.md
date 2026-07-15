# Binary Ninja workspace

Binary Ninja stores saved analysis in `.bndb` files. Save the local version-741 database at:

```text
binaryninja/workspace/Darkages.exe.bndb
```

`binaryninja/workspace/` and all `.bndb` files are ignored. A `.bndb` can be loaded directly and may contain snapshots and other client-derived analysis state, so do not commit or distribute it through this repository.

Reusable source files belong here instead:

- `binaryninja/scripts/`: import, export, validation, and repeatable analysis scripts
- `analysis/exports/`: mergeable YAML or JSON produced by those scripts
- `docs/`: conclusions and evidence written for humans

Keep scripts cross-platform. Use `pathlib` or Binary Ninja APIs instead of hard-coded separators and machine-specific installation paths. Prefer user symbols and user types for durable human conclusions.

See [Getting Started](../docs/getting-started.md) for local setup.
