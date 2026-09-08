# Dark Ages client research

This repository documents how the Dark Ages game client works. The book follows the application from startup and the game loop through UI events, networking, packet transforms, and individual client and server messages.

The writing is aimed at game and network programmers. Main pages explain behavior in plain language. Function addresses, patch bytes, inheritance lists, and detailed evidence live in appendices and YAML exports.

## Start here

- [Read the book](https://ewrogers.github.io/darkages-741-re/)
- [Choose a reading route](docs/README.md#choose-a-route) for a client turn, NPC conversation, asset reader, or exact reference.
- [Look up a client opcode](docs/network/client/README.md#packet-index) or [server opcode](docs/network/server/README.md#packet-index).

To contribute research, [set up Binary Ninja and MCP](docs/getting-started.md), then follow the [analysis method](docs/methodology.md). Reading the book does not require the analysis tools.

## Target client

```text
File: Darkages.exe
Size: 3,112,960 bytes
SHA-256: 054A5D6ADC56099C6BFD9D2A58675AFF62DC788B63209A3D906492F5B89E96C6
Reported version: 741
Architecture: 32-bit x86 Windows PE
```

The matching client is the source of truth. Related games, old notes, captures, and outside implementations are treated as leads.

## Private and shared files

Keep the complete client under ignored `client/`. Save local Binary Ninja databases under ignored `binaryninja/workspace/`.

Share findings through:

- `docs/` for the readable book
- `analysis/exports/` for deterministic YAML evidence
- `binaryninja/scripts/` for Binary Ninja import, export, and analysis helpers
- `scripts/` for generated book navigation and lookup pages

Do not commit the executable, original game assets, `.bndb` files, credentials, character data, or private captures.

## Current coverage

The book covers application startup and configuration, the game loop, events, UI panes, software rendering, audio, map and image formats, initial connection, TCP transport, packet transforms, runtime launcher patches, pane inheritance, and direction-specific packet indexes.

## License

See [LICENSE](LICENSE).
