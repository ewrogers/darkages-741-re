# Dark Ages 7.41 Reverse Engineering

Community reverse-engineering notes and tooling for the Dark Ages client that reports protocol/client version **741**.

The project documents how this specific client works from the inside out: network framing and dispatch, packet encryption, CRCs, client and server packet layouts, runtime data structures and memory pointers, UI behavior, and eventually the game's resource and file formats.

This is an independent interoperability and preservation effort. It is not affiliated with or endorsed by Nexon or the original developers.

## Current coverage

- TCP framing, receive buffering, decryption, and dispatch
- Client packet construction, sequencing, encryption, and transmission
- Server and client opcode indexes with per-packet documentation
- Packet-reader primitives and nested/count-based payload structures
- Salt-table generation, session keys, character-name key derivation, and CRC routines
- Recovered MSVC RTTI names, IDA function names, handler addresses, and behavioral evidence
- Editable-paper and read-only-paper UI/network behavior
- Security behavior including the persistent `SBadGuy` installation marker and login kill switch
- WinMain, window, Miles audio, DirectDraw, archive, profile, and table initialization
- Endpoint hostname resolution, numeric caches, and connection fallback order
- Legacy and extended fastfile archives, including metadata XOR and zlib 1.1.3 decompression
- Declarative UI layouts, pane construction, input dispatch, EPF/SPF image loading, and 302 pane-related RTTI records
- Win32 message routing, internal input events, focus and modal priority, keyboard shortcuts, mouse modifiers, and world actions
- A version-controlled [friendly function index](docs/functions/README.md) generated from IDA exports

Start with the [documentation index](docs/README.md), the [combined SPacket/CPacket opcode list](docs/network/README.md), or the [client security notes](docs/security/README.md).

## Documentation site

The documentation is an [mdBook](https://rust-lang.github.io/mdBook/). Pull requests validate its structure and links. Changes merged into `main` are built and published through GitHub Actions.

For local preview:

```text
cargo install mdbook --locked
python -m pip install -r requirements-docs.txt
python tools/render_function_report.py --check
python tools/render_ui_pane_report.py --check
python tools/check_docs.py
mdbook serve --open
```

Repository administrators must select **GitHub Actions** as the Pages source once under `Settings > Pages`.

## Agent-assisted IDA setup

IDA Free is sufficient for this 32-bit x86 client. The [agent instructions](AGENTS.md) include a basic IDA Free and `ida-free-mcp` installation guide, project voice and code conventions, and the expected reverse-engineering workflow.

## Repository layout

```text
docs/
  SUMMARY.md          mdBook navigation and chapter order
  client/             Startup, client internals, send/receive paths, crypto, and CRC
  file-formats/       Resource archives, compression, configuration, NFO markers, and tables
  functions/          Friendly IDA function index and contribution workflow
  input/              Win32, keyboard, mouse, modal, and world input routing
  network/            Combined opcode index plus client and server packet pages
  security/           Anti-abuse, installation identity, and kill-switch behavior
  ui/                 Layout grammar, runtime behavior, and pane class catalog
ida/
  README.md           IDA workflow and naming conventions
  exports/            Version-controlled names and signatures exported from IDA
  workspace/          Local IDA database location; intentionally gitignored
book.toml             mdBook configuration
```

Future format research should extend `docs/file-formats/` or grow into focused directories such as `docs/graphics/` and `docs/audio/`, with parsers and verification tools kept in a top-level `tools/` directory.

## Evidence and naming

The version-741 client is the source of truth. Information from packet captures, server behavior, leaked symbols, or later games using a related engine is valuable, but its provenance must remain visible.

Use these confidence categories when adding findings:

- **Confirmed local:** directly established from the version-741 binary or a repeatable runtime observation.
- **Observed:** established from a packet capture or in-game behavior but not fully traced in code.
- **Related-engine:** authoritative terminology from a related title, pending confirmation in this client.
- **Provisional:** a reasoned interpretation that still needs verification.

A question mark in documentation marks a reconstructed or uncertain name. IDA identifiers cannot contain `?`, so uncertain symbols use `maybe_` where appropriate.

## Packet documentation conventions

- `SPacket` means server-to-client; `CPacket` means client-to-server.
- Packet files use `DDD-0xhh-name.md`, for example `027-0x1b-enter-editing-mode.md`. The decimal prefix keeps filesystem ordering aligned with opcode order.
- Describe the post-decrypt or pre-encrypt body beginning with the opcode.
- State byte order, conditional fields, counted loops, nested readers, and transform mode explicitly.
- Include parser, builder, sender, and handler addresses whenever they are known.
- Keep internal/company terminology when supported; record friendly behavioral aliases separately.

## IDA workflow

Network functions use the `net_` prefix and other subsystems use similarly clear snake_case prefixes such as `input_`, `ui_`, `audio_`, or `render_`.

Keep the local IDA database under `ida/workspace/`. IDA databases and temporary sidecars are ignored because they are large, non-mergeable, and may embed material from the original executable. Collaborative names and signatures belong in `ida/exports/functions.yaml` and the generated [friendly function index](docs/functions/README.md). Pane RTTI and layout associations belong in `ida/exports/ui-pane-classes.yaml` and the generated [pane class catalog](docs/ui/pane-classes.md). See [the IDA workspace notes](ida/README.md).

## Contributing

Contributions are welcome for packet layouts, captures with sensitive information removed, function and structure identifications, memory mappings, algorithms, file formats, parsers, and corrections.

Please:

1. Identify the client build and record exact addresses where relevant.
2. Separate confirmed evidence from inference and related-game comparisons.
3. Preserve unknown fields instead of discarding them.
4. Prefer reproducible descriptions, test vectors, and small sanitized fixtures.
5. Do not commit original executables, proprietary game archives/assets, credentials, character data, or unsanitized packet captures.

## License

Original research, documentation, and source code in this repository are available under the [MIT License](LICENSE). Dark Ages and all original game software and assets remain the property of their respective owners.
