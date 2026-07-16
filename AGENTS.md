# Agent instructions

These instructions apply to the entire repository.

## Project goal

This project documents the Dark Ages client that reports version `741`. The new book is a clean Binary Ninja-based analysis. Its goal is to build a clear, evidence-based understanding of the client, server protocol, packet encryption, CRC routines, runtime memory structures, UI behavior, and file formats.

The target client is the local source of truth. Related games, leaked names, packet captures, external implementations, and archived prior work can provide context, but they do not override what this binary does.

Target executable fingerprint:

```text
File: Darkages.exe
Size: 3,112,960 bytes
SHA-256: 054A5D6ADC56099C6BFD9D2A58675AFF62DC788B63209A3D906492F5B89E96C6
Reported client version: 741
Architecture: 32-bit x86 Windows PE
```

Do not commit the executable, original game assets, `.bndb` files, or other client-derived binary workspace state.

## Clean-slate rule

`legacy/` contains the previous project. Treat it only as a collection of leads.

- Do not copy a legacy conclusion into the new book without rechecking it in Binary Ninja.
- Do not import old friendly names in bulk.
- When a legacy page points to useful evidence, follow the evidence from the matching binary again.
- If new evidence contradicts legacy material, document the new result and leave the archive unchanged.
- Keep new documentation outside `legacy/`.

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

## Binary Ninja and MCP setup

Binary Ninja is the analysis tool for this project. The target remains a 32-bit x86 Windows client, but the analysis workstation may run Windows, macOS, or Linux.

Requirements:

- [Binary Ninja](https://binary.ninja/) with plugin support
- [fosdickio/binary_ninja_mcp](https://github.com/fosdickio/binary_ninja_mcp)
- Python 3.12 or newer
- A legally obtained copy of the matching client executable
- An MCP-capable agent or editor

Binary Ninja Free does not support plugins. The MCP workflow therefore requires a paid Non-Commercial/Personal, Commercial, or Ultimate license. Non-Commercial/Personal supports plugins while the GUI is running. Headless plugin execution requires Commercial or Ultimate.

Initial setup:

1. Install Binary Ninja for the local platform.
2. Install `binary_ninja_mcp` through Binary Ninja's Plugin Manager or follow the plugin repository's manual installation instructions.
3. Place the complete private client under `client/`.
4. Verify `client/Darkages.exe` against the required size and SHA-256.
5. Open `client/Darkages.exe` in Binary Ninja.
6. Save the analysis database as `binaryninja/workspace/Darkages.exe.bndb`.
7. Click the MCP plugin button in the lower-left corner of the Binary Ninja GUI and configure the MCP client as described by the plugin.
8. Verify the session with a small read-only request such as reading the entry point, listing imports, or inspecting one known address.

Do not encode machine-specific plugin paths or credentials in committed files.

## Repository map

- `docs/README.md`: new documentation entry point
- `docs/SUMMARY.md`: mdBook navigation
- `docs/getting-started.md`: local client, Binary Ninja, and MCP setup
- `docs/methodology.md`: evidence and reverse-engineering method
- `docs/client/`: verified client behavior and runtime patch documentation
- `docs/network/`: connection, transport, transform, and packet documentation
- `analysis/`: policy and version-controlled analysis exports
- `analysis/exports/`: deterministic symbols, functions, types, and comments exported from Binary Ninja
- `binaryninja/README.md`: Binary Ninja workspace and database policy
- `binaryninja/scripts/`: reusable import, export, and analysis scripts
- `binaryninja/workspace/`: local ignored `.bndb` files
- `examples/windows/`: small Windows C99 examples derived from verified analysis
- `client/`: complete local ignored client installation
- `legacy/`: archived prior repository content

Add focused documentation directories only when direct Binary Ninja evidence justifies them. Extend an existing page instead of creating a competing source of truth.

## Reverse-engineering workflow

1. Confirm that the opened file matches the target fingerprint.
2. Search the new docs, committed analysis exports, Binary Ninja user symbols, and comments before naming anything.
3. Search `legacy/` separately for possible leads. Treat every result as unverified.
4. Start from direct evidence such as an opcode comparison, packet reader call, string, import, vtable, caller, or runtime observation.
5. Trace callers and callees. Check cross-references and nearby branches.
6. Use HLIL and decompiled C as conveniences. Verify important layouts, constants, register use, stack behavior, and control flow against MLIL, LLIL, or disassembly.
7. Apply useful user symbols, types, and comments in Binary Ninja when confidence is sufficient.
8. Export durable analysis into `analysis/exports/` with a checked-in script when an export format exists.
9. Update the matching Markdown documentation in the same task.
10. Record uncertainty, contradictory evidence, and provenance.
11. Validate links, exports, scripts, and the mdBook build before finishing.

When command-line or regional behavior is involved, identify the active build or distribution selector before presenting a parser as usable. Document dormant parsers separately. For connection analysis, distinguish configuration-time endpoint fallbacks from connect-time retries, and record whether each failure returns, reports an error, retries, or terminates the process.

If the binary and any related source disagree, keep the local behavior. Record the related name or behavior only as context with its provenance.

Ask the project owner for tribal knowledge when in-game behavior would resolve an ambiguity. Treat the answer as behavioral evidence and still connect it to the local code where possible.

## Binary Ninja naming and comments

- Use lowercase `snake_case`.
- Prefix network functions with `net_`.
- Use clear subsystem prefixes such as `ui_`, `input_`, `render_`, `audio_`, `file_`, or `map_` after the subsystem is established.
- Reserve `app_` for application-wide lifecycle or configuration state. Use `session_`, `game_`, or `character_` for state owned by those narrower lifetimes or subsystems.
- Use `maybe_` for useful but uncertain Binary Ninja names.
- Documentation may use a trailing `?` for a reconstructed class or field name.
- Preserve a useful existing name unless stronger evidence improves it.
- Do not rename a function from a legacy or related-game name alone.
- Add comments at important opcode checks, packet field reads, loop boundaries, mode branches, key derivation, and state writes.
- Comments should explain intent and evidence, not restate the instruction.

When scripting Binary Ninja changes, prefer user symbols, user types, and other `_user_` APIs for human conclusions that must survive reanalysis. Auto-analysis results can be replaced when analysis is rerun or upgraded.

## UI and event documentation

Treat the UI as several connected mechanisms instead of assuming one universal scene graph.

- Distinguish the spatial `HierList<Screen>`, the runtime `EventHandlerList` pane tree, a `DialogPane` local control collection, and `Singleton<T>` access wrappers.
- Record an exact RTTI class name separately from a reconstructed method or field name. RTTI proves the class spelling, not the method's purpose.
- For a pane event handler, record the primary-vtable slot, event family, consumed return behavior, coordinate space, and base implementation being overridden.
- Track registration, visibility, input priority, mouse capture, control focus, and object validity as separate states.
- Record secondary-base offsets. `Pane` uses a `TimerHandler` subobject at `this + 0x11C`, so a timer callback may receive an adjusted `this` pointer.
- When documenting propagation, state whether traversal is child-first or parent-first and where a true return stops it.
- For dialogs, preserve control attachment order when the collection index becomes the action or focus ID.
- Do not infer the live pane tree from the static RTTI inventory. Use registration code or runtime observation to establish live parent, sibling, and visibility state.
- Distinguish vtable name-search results from distinct complete-object RTTI classes. Derive inheritance from the MSVC Class Hierarchy Descriptor and Base Class Array, not from a qualified vtable display name alone.

For injected event or network proxies:

- Verify the executable fingerprint and resolve static targets as module-base-relative RVAs.
- Keep IPC and configuration parsing outside hooks. Hooks may consult local bounded state but must not wait for another process.
- Queue external commands and invoke client event or packet producers from the main-thread dispatcher tick.
- Prefer native `EventMan` producers for pointer, keyboard, text, and IME events so client state and ownership rules remain intact.
- Treat pointer-bearing event variants as unsafe for generic IPC until construction and cleanup are fully verified.
- Make rule failure fail-open, bound command and telemetry queues, and drop telemetry rather than blocking the client.
- Keep persistent proxy rules in YAML. A compact fixed binary IPC format is acceptable when the controller owns YAML parsing.

## Text encoding and localization

The client originated in the Korean market and may contain untranslated or incorrectly rendered Korean text. Treat text shown as `????`, especially near `MessageBoxA`, as an encoding question rather than assuming the literal text is known.

- Inspect and preserve the raw bytes and their static address before interpreting the string.
- Test non-ASCII byte strings as Windows code page 949, also called Unified Hangul Code, when the byte sequence supports it.
- Distinguish Binary Ninja display behavior, Windows active-ANSI-code-page behavior, dynamic conversion loss, and literal `0x3F` bytes stored in the executable.
- Remember that `MessageBoxA` interprets text through the process environment's active ANSI code page, so the same bytes may render differently under another Windows system locale.
- Trace string-building and conversion calls when the message is produced dynamically.
- If the text is recoverable, document the original Korean, an English translation, the encoding, and the translation provenance. Do not present a speculative decoding as confirmed.
- If the executable contains literal replacement question marks, state that the original text is not recoverable from that string alone.

Do not patch executable bytes unless the user explicitly asks to apply a patch. A request to find, explain, or document a patch authorizes analysis and documentation only. It does not authorize Binary Ninja byte patching, saving a modified executable, or creating a patched copy. Renaming, typing, and commenting the local analysis database are normal project work.

## Runtime patch documentation

When a finding is intended for a launcher that patches process memory:

- Record the static Binary Ninja address, preferred image base, module-relative RVA, original bytes, and replacement bytes.
- Treat file offsets as reference information only. A launcher must use the actual loaded module base plus the RVA because ASLR can relocate the image.
- Verify the exact target fingerprint and original instruction bytes before writing.
- Prefer a same-size instruction change that follows an existing valid control-flow or state-machine path.
- Explain why the chosen patch is narrower and safer than nearby alternatives.
- Require a suspended launch, temporary page protection change, instruction-cache flush, protection restoration, and fail-closed cleanup.
- Never write the original executable as part of runtime-patch research.

## Version-controlled analysis

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

## Address and evidence requirements

Preserve memory and code addresses in documentation whenever they are known and useful.

For a function or global, record:

- Current Binary Ninja user symbol, if one exists
- Static virtual address, such as `0x567DE0`
- Role in the control flow
- Important callers or callees when relevant
- Confidence and provenance

For runtime pointers, distinguish clearly between:

- Static image addresses
- Globals that contain pointers
- Object-relative offsets such as `this + 0x638`
- Values that move because of ASLR or allocation

Do not present a static Binary Ninja address as a stable runtime address without explaining the image base or relocation requirement.

## Packet documentation

`SPacket` means server-to-client. `CPacket` means client-to-server.

Write the word `packet` in full in documentation and user-defined symbols. Do not abbreviate it. Quote a compiler-recovered abbreviation only when the exact spelling is necessary evidence.

Use `SPacket` and `CPacket` only as generic direction terms. Concrete display names omit the redundant `Packet` suffix, even when related material includes it. Write `SUserPosition`, `CVersion`, and `CRefresh`, not their suffixed forms. Packet page and navigation titles use the friendly name followed by the concrete class name, such as `User Position (SUserPosition)` or `Version (CVersion)`.

Preserve exact server class names recovered through RTTI even when a friendlier behavioral label is useful. Client packet names supplied by the project owner are protocol vocabulary, not compiler-recovered RTTI. Record that provenance and keep descriptive aliases separate when the names differ. Do not force paired client and server names to match.

Some control bodies may resemble an opcode-first packet without representing a normal packet class. Document their exact bytes, framing path, and sequence effects instead of forcing them into the ordinary packet model.

Every client packet page should include a known send-site list. Record each direct static call address, its containing function, and an exact RTTI pane or subsystem owner when one can be reached reliably. Distinguish a direct virtual-method owner from an owner found through caller traversal. State when the owner is unresolved, and do not imply that static cross-references cover indirect or queued runtime calls.

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

Keep master indexes synchronized with packet pages.

Keep client and server opcode evidence separate. The server direction may have RTTI-backed concrete class names. The client direction has no recovered derived packet RTTI classes, so each friendly client name must cite builder behavior or related-name provenance.

Do not treat absence from the server packet factory as proof that an opcode is unused. Search decoded-body event consumers in UI panes, session state, and manager classes. An RTTI-backed owner may handle a raw decoded buffer without constructing a concrete RTTI packet object. Record the packet name provenance separately from the owner class RTTI.

Record the common transform as `raw`, `static`, or `derived` on each packet page. Do not infer one direction's opcode policy from the other direction.

When documenting common packet encryption, distinguish the static key, the per-packet 9-byte derived key, the 1024-byte MD5 salt source, the 256-entry seed XOR table, the rolling selector, and direction-specific trailers. Do not collapse these into a single generic salt or key.

## Source-of-truth rules

- Derive encryption, CRC, packet layouts, and memory mappings from this client unless the user explicitly asks for an external comparison.
- Do not silently copy algorithms or field names from `legacy/` or online implementations.
- Leaked or related-engine names can improve terminology, but mark their provenance.
- Runtime captures can confirm behavior, sizes, sequencing, and encryption state.
- For negotiated protocol state, document the compiled default separately from values selected or supplied by the server.
- Treat seed-table selectors outside the locally handled range `0` through `9` as invalid, even if the client reaches an undefined implementation path.
- Preserve contradictory evidence instead of forcing an early conclusion.

## Repository hygiene

- Preserve unrelated user changes.
- Do not commit anything under `client/` or `binaryninja/workspace/`.
- Do not commit `.bndb` files, original binaries, game archives, credentials, character data, or unsanitized captures.
- Small sanitized fixtures are acceptable when necessary to reproduce a parser or test. Add ignored binary fixtures deliberately with `git add -f` only after review.
- Keep generated files and tool output out of the documentation tree.
- Use relative Markdown links inside the repository.
- Do not commit or push unless the user asks.

## Completion standard

A reverse-engineering task is complete when the local behavior is explained from Binary Ninja evidence, useful user symbols or comments are updated, durable analysis is exported when supported, documentation is synchronized, uncertainty is visible, and basic validation has passed.
