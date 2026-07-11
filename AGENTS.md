# Agent instructions

These instructions apply to the entire repository.

## Project goal

This project documents the Dark Ages client that reports version `741`. The goal is to crowdsource a clear, evidence-based understanding of the client, server protocol, packet encryption, CRC routines, runtime memory structures, UI behavior, and future file formats.

The version-741 client is the local source of truth. Related games, leaked names, packet captures, and external implementations can provide useful context, but they do not override what this binary does.

Target executable fingerprint:

```text
File: Darkages.exe
Size: 3,112,960 bytes
SHA-256: 054A5D6ADC56099C6BFD9D2A58675AFF62DC788B63209A3D906492F5B89E96C6
Reported client version: 741
```

Do not commit the executable or original game assets.

## Language and voice

- Use natural, simple human language whenever possible.
- Keep the work approachable without hiding important technical facts.
- Write at a senior developer and reverse engineer level when the subject requires it.
- Explain uncommon low-level terms the first time they matter.
- Lead with the result, then provide the evidence.
- Keep responses and documentation concise. Less is more.
- Do not use em dashes.
- Do not use emojis.
- Avoid decorative formatting, filler, and unnecessary jargon.
- State uncertainty plainly. Do not make a guess sound confirmed.

## Code and pseudocode style

Use pseudocode or C/C++ for algorithm examples because they match the likely implementation language and are easy to translate elsewhere.

- Prefer plain C-like pseudocode or minimal C99-style code.
- Era-appropriate C++ is acceptable when classes, vtables, constructors, or destructors are relevant.
- Avoid templates, lambdas, ranges, heavy STL use, clever macros, and modern language features that obscure the algorithm.
- Use straightforward loops, explicit branches, and small helper functions.
- Use fixed-width protocol names such as `u8`, `u16`, and `u32` when documenting wire fields.
- State endianness explicitly, such as `u16be`.
- Preserve bounds, loop counts, conditional fields, and nested structures.
- Keep examples expressive rather than production-framework specific.

Example:

```c
u16 read_u16_be(const u8 *p)
{
    return (u16)(((u16)p[0] << 8) | p[1]);
}
```

## IDA Free and MCP setup

IDA Free is enough for this project. The target is a 32-bit x86 Windows client, and IDA Free supports x86 analysis, decompilation, and saved databases.

Requirements:

- [IDA Free 9.0 or newer](https://hex-rays.com/ida-free)
- [0xshlomil/ida-free-mcp](https://github.com/0xshlomil/ida-free-mcp)
- A legally obtained copy of the matching client executable
- An MCP-capable agent or editor

Setup:

1. Install IDA Free from Hex-Rays.
2. Download the matching prebuilt plugin from the [ida-free-mcp releases](https://github.com/0xshlomil/ida-free-mcp/releases). Building from source is optional.
3. Copy `ida_mcp.dll` on Windows, or the matching library for another platform, into an IDA `plugins` directory. Follow the plugin repository if the filename or install location changes.
4. Place a private IDA database at `ida/workspace/Darkages.exe.i64`, or create a new database by loading the matching executable in IDA. The workspace directory is intentionally ignored by Git.
5. Open the database in IDA.
6. Start the plugin with `Edit > Plugins > MCP` or `Ctrl+Alt+M`.
7. Connect the MCP client to `http://127.0.0.1:13337/mcp`.

Claude Code can register it with:

```text
claude mcp add --transport http ida-mcp http://127.0.0.1:13337/mcp
```

Other MCP clients can use:

```json
{
  "mcpServers": {
    "ida-mcp": {
      "url": "http://127.0.0.1:13337/mcp"
    }
  }
}
```

Press `Ctrl+Alt+M` again to stop the server. If several IDA instances are open, the plugin can choose a later port. It records active instances under `~/.ida-mcp/instances/`.

The plugin's `decompile` tool works with IDA Free through the GUI decompiler. A diagnostic result such as `init_hexrays_plugin: false` is expected in IDA Free and does not by itself mean decompilation is broken.

After connecting, verify the session with a small read-only request such as looking up a known function, listing imports, or disassembling an address.

## Repository map

- `docs/README.md`: documentation entry point
- `docs/client/`: client implementation details, networking, crypto, and CRC
- `docs/file-formats/`: archive, compression, configuration, NFO, profile, and table formats
- `docs/functions/`: generated friendly function index and contribution guide
- `docs/map/`: map loading, tile rendering, SOTP flags, and collision
- `docs/network/`: combined opcode index plus client and server packet pages
- `docs/security/`: anti-abuse, installation identity, and deliberate termination behavior
- `docs/ui/`: UI layout grammar, loading, input, rendering, and pane classes
- `docs/objects/`: dynamic object classes, lifecycle, view range, runtime fields, and self-player initialization
- `ida/README.md`: IDA naming and sharing notes
- `ida/exports/functions.yaml`: version-controlled friendly IDA names and signatures
- `ida/exports/ui-pane-classes.yaml`: version-controlled pane RTTI, layout, and usage export
- `ida/workspace/`: local ignored IDA database

Read the relevant indexes before starting a new analysis. Extend existing pages instead of creating competing sources of truth.

## Reverse-engineering workflow

1. Confirm that the loaded database matches the target build.
2. Search existing docs, names, and comments before naming anything new.
3. Start from direct evidence such as an opcode comparison, packet reader call, string, import, vtable, caller, or runtime observation.
4. Trace callers and callees. Check cross-references and nearby branches.
5. Use decompiler output as a convenience, not as unquestioned truth. Verify important layouts, constants, and control flow against disassembly.
6. Record conditional fields and loops exactly. Do not flatten variant payloads into one unconditional structure.
7. Update useful IDA names and comments when confidence is sufficient.
8. Update `ida/exports/functions.yaml` when a friendly function name, address, size, or signature changes.
9. Run `python tools/render_function_report.py` to refresh the function index.
10. Run `python tools/render_ui_pane_report.py` when pane class context changes.
11. Update the matching Markdown documentation in the same task.
12. Validate links and any reference code before finishing.

If the binary and a related-engine list disagree, keep the local opcode and behavior. Record the related name as context with its provenance.

Ask the project owner for tribal knowledge when in-game behavior would resolve an ambiguity. Treat that answer as behavioral evidence and still connect it to the local code where possible.

## IDA naming and comments

- Use lowercase `snake_case`.
- Prefix network functions with `net_`.
- Use clear subsystem prefixes such as `ui_`, `render_`, `audio_`, `file_`, or `map_` after the subsystem is established.
- Use `maybe_` for useful but uncertain IDA names.
- Documentation may use a trailing `?` for a reconstructed class or field name.
- Preserve a useful existing name unless stronger evidence improves it.
- Do not rename a function from a related-game name alone.
- Add comments at important opcode checks, packet field reads, loop boundaries, mode branches, key derivation, and state writes.
- Comments should explain intent and evidence, not restate the instruction.

Do not patch executable bytes unless the user explicitly asks for a patch. Renaming, typing, and commenting the analysis database are normal project work.

## Function catalog

The ignored IDA database is not the only record of discovered names. Keep `ida/exports/functions.yaml` and `docs/functions/README.md` synchronized with useful IDA changes.

The catalog includes friendly project names, static addresses, function sizes, and IDA-inferred prototypes. A missing prototype is recorded as `null`. Treat inferred calling conventions and argument types as working assumptions until callers, register use, and stack cleanup confirm them.

When a new subsystem is reversed:

1. Choose a clear snake_case subsystem prefix.
2. Rename and comment functions in IDA.
3. Add the friendly functions to the matching prefix group in `ida/exports/functions.yaml`, sorted by name within that group.
4. Run `python tools/render_function_report.py`.
5. Add focused subsystem documentation when the table alone is not enough.

Keep prefix groups sorted by prefix. A function belongs in the group matching the beginning of its name, such as `file_`, `net_`, `render_`, or `ui_`. Add a new group when a newly reversed subsystem has a clear, durable prefix.

## Address and evidence requirements

Preserve memory and code addresses in documentation whenever they are known and useful.

For a function or global, record:

- Current IDA name
- Static virtual address, such as `0x567DE0`
- Role in the control flow
- Important callers or callees when relevant
- Confidence and provenance

For runtime pointers, distinguish clearly between:

- Static image addresses
- Globals that contain pointers
- Object-relative offsets such as `this + 0x638`
- Values that move because of ASLR or allocation

Do not present a static IDA address as a stable runtime address without explaining the image base or relocation requirement.

## Packet documentation

`SPacket` means server-to-client. `CPacket` means client-to-server.

Use `SPacket` and `CPacket` only as generic direction terms. Concrete display names omit the redundant `Packet` suffix, even when the original RTTI or leaked template included it. Write `SUserPosition`, `CVersion`, and `CRefresh`, not their suffixed forms. Packet page and navigation titles use the friendly name followed by the concrete class name, such as `User Position (SUserPosition)` or `Version (CVersion)`.

Packet filenames use a zero-padded decimal prefix followed by lowercase hexadecimal:

```text
027-0x1b-enter-editing-mode.md
053-0x35-show-paper.md
```

Each packet page should include as much of the following as is known:

- Direction and opcode
- Internal name, behavioral alias, and name provenance
- Framing and transform mode
- Plaintext body layout beginning with the opcode
- Field types, byte order, variants, counts, and nested loops
- Parser, handler, builder, or sender addresses
- State changes and UI effects
- Paired request or response packets
- Unknown fields and the reason they remain unknown

Keep the master indexes synchronized with packet pages.

## Source-of-truth rules

- Derive encryption, CRC, packet layouts, and memory mappings from this client unless the user explicitly asks for an external comparison.
- Do not silently copy algorithms or field names from online implementations.
- Leaked or related-engine names can improve terminology, but mark their provenance.
- Runtime captures can confirm behavior, sizes, sequencing, and encryption state.
- Preserve contradictory evidence instead of forcing an early conclusion.

## Repository hygiene

- Preserve unrelated user changes.
- Do not commit IDA databases, original binaries, game archives, credentials, character data, or unsanitized captures.
- Small sanitized fixtures are acceptable when they are necessary to reproduce a parser or test.
- Keep generated files and tool output out of the documentation tree.
- Use relative Markdown links inside the repository.
- Do not commit or push unless the user asks.

## Completion standard

A reverse-engineering task is complete when the local behavior is explained, relevant IDA names or comments are updated, documentation is synchronized, uncertainty is visible, and basic validation has passed.
