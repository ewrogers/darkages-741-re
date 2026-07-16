# Getting started

You need Binary Ninja, its MCP plugin, and your own copy of the matching game client. The client and Binary Ninja database stay private on your machine.

## Requirements

- Binary Ninja with plugin support
- [`binary_ninja_mcp`](https://github.com/fosdickio/binary_ninja_mcp)
- Python 3.12 or newer
- An MCP-capable editor or agent
- A legally obtained copy of the target client

Binary Ninja Free does not load plugins. A paid Non-Commercial/Personal, Commercial, or Ultimate license is required for this workflow. Non-Commercial/Personal works while the GUI is open. Headless plugin use requires Commercial or Ultimate.

## Check the client

Place the full private client under `client/`, then confirm:

```text
File: Darkages.exe
Size: 3,112,960 bytes
SHA-256: 054A5D6ADC56099C6BFD9D2A58675AFF62DC788B63209A3D906492F5B89E96C6
Architecture: 32-bit x86 Windows PE
```

Do not commit the executable, game assets, captures with private data, or saved Binary Ninja databases.

## Open the workspace

1. Open `client/Darkages.exe` in Binary Ninja.
2. Let initial analysis finish.
3. Save the database as `binaryninja/workspace/Darkages.exe.bndb`.
4. Install `binary_ninja_mcp` from Binary Ninja's Plugin Manager or its repository instructions.
5. Start the MCP plugin from the Binary Ninja window.
6. Configure Codex or another MCP client with the connection details shown by the plugin.

Machine-specific paths and credentials stay in local configuration, not the repository.

## First MCP check

Begin with a small read-only request:

- show the executable entry point
- list a few imports
- display one known function by name

If that works, ask for callers, callees, or pseudocode for one focused function. Save useful names and comments in Binary Ninja, then export them to YAML when they should be shared.

## What gets committed

| Path | Purpose | Commit? |
| --- | --- | --- |
| `client/` | Complete local client | No |
| `binaryninja/workspace/` | Local `.bndb` workspace | No |
| `binaryninja/scripts/` | Reusable analysis scripts | Yes |
| `scripts/` | Generated book and repository helpers | Yes |
| `analysis/exports/` | Reviewable Binary Ninja findings | Yes |
| `docs/` | The book | Yes |

Continue with [How we study the client](methodology.md).
