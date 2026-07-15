# Dark Ages 7.41 Reverse Engineering

This repository documents the matching Dark Ages client through evidence-based reverse engineering in Binary Ninja. Binary Ninja MCP provides agent-assisted access to the local analysis workspace.

Material under [`legacy/`](legacy/NOTICE.md) is retained for reference. It may provide useful leads, but every claim must be independently verified against the target client in Binary Ninja.

## Target build

```text
File: Darkages.exe
Size: 3,112,960 bytes
SHA-256: 054A5D6ADC56099C6BFD9D2A58675AFF62DC788B63209A3D906492F5B89E96C6
Reported client version: 741
Architecture: 32-bit x86 Windows PE
```

The matching executable is the local source of truth. Do not commit it or any original game assets.

## Binary Ninja database policy

Binary Ninja stores saved analysis in a `.bndb` database. A `.bndb` can be reopened directly and may retain snapshots and other analysis history. This project therefore treats it as private client-derived workspace state. It is intentionally ignored and should not be committed.

Share durable analysis through reviewable text exports and documentation instead:

| Path | Purpose | Commit? |
| --- | --- | --- |
| `client/` | Local copy of the complete matching client | No |
| `binaryninja/workspace/` | Local `.bndb` databases and Binary Ninja project state | No |
| `binaryninja/scripts/` | Reusable Binary Ninja import, export, and analysis scripts | Yes |
| `analysis/exports/` | Deterministic symbols, types, comments, and function metadata | Yes |
| `docs/` | The evidence-based book | Yes |
| `legacy/` | Reference material, used only for hints | Yes |

See [Binary Ninja workspace notes](binaryninja/README.md) and [analysis export policy](analysis/README.md).

## Requirements

- [Binary Ninja](https://binary.ninja/) with a license that supports plugins. Binary Ninja Free does not load plugins, so the MCP workflow requires a paid Non-Commercial/Personal, Commercial, or Ultimate edition.
- [fosdickio/binary_ninja_mcp](https://github.com/fosdickio/binary_ninja_mcp)
- Python 3.12 or newer, as required by the MCP plugin
- A legally obtained copy of the matching client
- An MCP-capable agent or editor
- [mdBook](https://rust-lang.github.io/mdBook/) to build the documentation locally

Binary Ninja runs on Windows, macOS, and Linux. A 32-bit Windows target does not require analysis to run on Windows.

## Start here

1. Put the complete private client installation under `client/`.
2. Verify `client/Darkages.exe` against the target size and SHA-256 above.
3. Open it in Binary Ninja and save the local database as `binaryninja/workspace/Darkages.exe.bndb`.
4. Install and configure Binary Ninja MCP in the Binary Ninja GUI.
5. Read the [getting started chapter](docs/getting-started.md) and [analysis method](docs/methodology.md).

Build the new book with:

```shell
mdbook build
```

## Current status

Verified analysis covers the [startup controls](docs/client/startup.md), [initial connection](docs/network/initial-connection.md), [network architecture](docs/network/architecture.md), [packet transforms](docs/network/packet-transforms.md), and direction-specific [client](docs/network/client/README.md) and [server](docs/network/server/README.md) packet indexes. Durable Binary Ninja analysis and packet metadata are stored as YAML under [`analysis/exports/`](analysis/exports/README.md).

## License

Original project content in this repository is licensed under the [MIT License](LICENSE). Dark Ages and its original software and assets belong to their respective owners and are not distributed here.
