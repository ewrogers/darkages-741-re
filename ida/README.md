# IDA workspace

For IDA Free and MCP installation, read the repository [agent instructions](../AGENTS.md#ida-free-and-mcp-setup).

Place the local version-741 IDA database and its temporary working files in:

```text
ida/workspace/Darkages.exe.i64
```

The entire `ida/workspace/` directory and common IDA database extensions are intentionally ignored by Git. A database is large and binary, cannot be meaningfully merged, and may contain bytes or other material derived from the original client executable.

## Naming conventions

- Use lowercase `snake_case`.
- Prefix network functions with `net_`.
- Use subsystem prefixes such as `ui_`, `render_`, `audio_`, and `file_` when the subsystem is established.
- Use `maybe_` for a useful but uncertain IDA symbol; documentation can use a trailing `?`.
- Add comments explaining packet opcodes, field layouts, important branches, and the evidence behind non-obvious names.
- Treat the version-741 client as authoritative when a related engine or later game disagrees.

## Sharing IDA findings

Commit durable findings in one or both of these forms:

1. Human-readable pages under `docs/` with addresses and evidence.
2. Machine-readable names and signatures in `ida/exports/functions.yaml`.
3. Reproducible scripts under a future `ida/scripts/` directory.

Run `python tools/render_function_report.py` after changing the function export. The generated report is [docs/functions/README.md](../docs/functions/README.md).

Do not commit the original `Darkages.exe`, the IDA database, or expanded `.id0/.id1/.id2/.nam/.til` working files.
