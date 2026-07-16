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

## Book audience and voice

Write the book for beginner to moderate programmers who understand common programming, game-loop, UI, and network patterns. Do not assume the reader knows Binary Ninja, assembly, compiler internals, or reverse-engineering terminology.

The reader should be able to understand how the client works before learning how the conclusion was recovered.

- Use natural, simple, and terse language.
- Keep the first paragraph inviting. Start with what the game does and why it matters.
- Lead with the result, then explain the flow and important details.
- Prefer game-development terms such as game loop, scene tree, pane, event, packet, state, and handler.
- Prefer network-programming terms such as connection, frame, command, body, client, and server.
- Explain uncommon low-level terms the first time they matter.
- Do not open a page with addresses, pointer arithmetic, RTTI details, vtable slots, or tool steps.
- Avoid debugger, offensive-security, defensive-security, and incident-response language when ordinary game or network language works.
- Describe what the client does. Avoid a running diary of how the behavior was discovered.
- Use short examples or analogies only when they make the idea easier to picture.
- State uncertainty plainly. Do not make a guess sound confirmed.
- Do not use em dashes.
- Do not use emojis.
- Avoid decorative formatting, filler, and unnecessary jargon.

## Book organization

Organize the book as layers of the client:

1. **Application:** startup, configuration, lifecycle, and shutdown.
2. **Game loop:** the main loop as its own topic, including when queued work and timers run.
3. **Game systems:** events, input, UI panes, dialogs, rendering, audio, maps, and other focused systems.
4. **Network:** endpoint selection, connection, transport, transforms, and separate client and server packet references.
5. **Appendices:** function addresses, runtime patches, object layouts, inheritance lists, and other lookup-heavy material.

Use overview pages to explain how a layer fits together, then link to focused pages for individual systems or packets. Keep one source of truth for each topic. Extend or replace the existing page instead of creating a competing explanation.

Main chapters should refer to functions by their project names. Put static addresses, RVAs, patch bytes, long call-site lists, and confidence notes in appendices or YAML exports. Object-relative offsets may remain beside a compact structure when they are necessary to understand that structure.

Keep `docs/SUMMARY.md` synchronized with the book. Keep client-to-server and server-to-client packet indexes separate because the same command code can mean different things in each direction.

## Book authoring style

A focused page should normally follow this order:

1. A short result or purpose statement.
2. A simple mental model or flow.
3. The named functions, states, or objects involved.
4. A compact structure or pseudocode block when it improves understanding.
5. Known limits, uncertainty, and links to deeper reference material.

This is a guide, not a required template for tiny packet pages.

- Keep paragraphs short and centered on one idea.
- Use headings that help a reader scan for behavior, data, happy paths, unhappy paths, or known limits.
- Use tables for exact mappings and comparisons.
- Prefer C-style pseudostructs over offset tables when programmers can understand the layout faster that way.
- Use small ASCII diagrams for real flows, trees, or inheritance when prose would be harder to follow. Do not add a diagram by habit.
- Use brief pseudocode for decisions, loops, and construction. Do not replace an explanation with a wall of code.
- Use analogies from game engines or network programming when they are accurate, such as a pane tree behaving like a scene tree or an event queue behaving like the game's inbox.
- Preserve technical details that matter. Move lookup-heavy proof into an appendix or export instead of deleting it.
- Keep packet pages useful as developer reference: purpose, direction, command, encoding, known trigger or owner, body layout, paired messages, and unknowns.
- Link to the function, structure, pane, or patch appendix instead of repeating address lists in prose.

## Code and pseudocode style

Use short C-like pseudocode because it matches the client and is easy to translate elsewhere. Examples do not need to compile.

- Prefer a few clear lines that show the decision, loop, or data flow.
- Use C-style pseudostructs for memory and packet layouts.
- Era-appropriate C++ is acceptable when classes, vtables, constructors, or destructors are relevant.
- Avoid templates, lambdas, ranges, heavy STL use, clever macros, and modern language features that obscure the algorithm.
- Use straightforward loops, explicit branches, and small helper functions.
- Use fixed-width protocol names such as `u8`, `u16`, and `u32` when documenting wire fields.
- State endianness explicitly, such as `u16be`.
- Preserve bounds, loop counts, conditional fields, and nested structures.
- Keep examples expressive rather than production-framework specific.
- Do not include a full launcher, injected DLL, or other compile-ready program in the book when pseudocode explains the design.

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

- `docs/README.md`: book entry point
- `docs/SUMMARY.md`: mdBook navigation
- `docs/getting-started.md`: local client, Binary Ninja, and MCP setup
- `docs/methodology.md`: evidence and client-study method
- `docs/application/`: startup, configuration, lifecycle, and game loop
- `docs/systems/`: event, input, UI, and other game systems
- `docs/rendering/`: renderer lifecycle, pane drawing, world layers, sprites, effects, and blending
- `docs/audio/`: audio lifecycle, music, sound effects, volume, fades, and MIDI status
- `docs/file-formats/`: one developer-facing page per confirmed asset or data format
- `docs/network/`: connection, transport, transform, and packet documentation
- `docs/appendix/`: function addresses, runtime patches, runtime structures, inheritance, and large lookup tables
- `analysis/`: policy and version-controlled analysis exports
- `analysis/exports/`: deterministic symbols, functions, types, and comments exported from Binary Ninja
- `binaryninja/README.md`: Binary Ninja workspace and database policy
- `binaryninja/scripts/`: reusable import, export, and analysis scripts
- `binaryninja/workspace/`: local ignored `.bndb` files
- `scripts/`: repository-level documentation and validation helpers
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
- Documentation may use a trailing `?` for an uncertain non-packet class or field name.
- Do not add `?` to a verified packet name. Record uncertainty about packet behavior, fields, or provenance in prose instead.
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

## UI layout documentation

- Treat the underscore-prefixed text layouts in `setoa.dat` as named geometry and skin data, not as a complete scene tree.
- Record the layout filename and the RTTI-backed pane class that loads it. Keep an asset with no proven filename reference marked unresolved.
- Keep layout definition order separate from `DialogPane` attachment order. Numeric action IDs come from `ui_dialog_add_control` order in the constructor.
- Treat `NAME` as the code-to-asset contract. A missing layout or named control takes a fatal invalid-layout path in this client.
- Record `TYPE`, `RECT`, repeated `IMAGE`, `VALUE`, and `COLOR` fields independently. Do not infer a runtime control class from `TYPE` alone.
- Preserve the order of repeated image, value, and color entries. Image-button construction can consume up to three ordered image states.
- When describing custom UI work, separate reskinning or repositioning existing controls from adding new behavior. A new interactive control also needs code to construct, attach, handle, and clean it up.
- Keep private extracted layout text and game art out of the repository. Commit only grammar notes, sanitized examples, and deterministic metadata.

## Portrait, profile, and formatted text documentation

- Keep the empty `SRequestPortrait` request separate from the `CSendPortrait` response body.
- Record portrait filename lookup order, image validation, exact size limits, and the independent zero-length image and profile cases.
- Describe `Face.epf` as a wildcard fallback, not a hardcoded client filename.
- Treat profile limits as bytes. Preserve the DBCS-safe truncation behavior and do not call the packet text Unicode.
- Separate saving `profile.txt`, refreshing the local preview, and uploading after a server request.
- Record inline `{=<letter>` codes as palette indexes. Do not invent fixed RGB values when the renderer resolves the final color through a palette.

For injected event or network proxies:

- Verify the executable fingerprint and resolve static targets as module-base-relative RVAs.
- Keep IPC and configuration parsing outside hooks. Hooks may consult local bounded state but must not wait for another process.
- Queue external commands and invoke client event or packet producers from the main-thread dispatcher tick.
- Prefer native `EventMan` producers for pointer, keyboard, text, and IME events so client state and ownership rules remain intact.
- Treat pointer-bearing event variants as unsafe for generic IPC until construction and cleanup are fully verified.
- Make rule failure fail-open, bound command and telemetry queues, and drop telemetry rather than blocking the client.
- Keep persistent proxy rules in YAML. A compact fixed binary IPC format is acceptable when the controller owns YAML parsing.
- Give every proxy rule a stable ID, explicit enabled state, and deterministic priority.
- Queue rule add, edit, remove, enable, disable, list, and reset commands from IPC. Apply mutations from the main-thread dispatcher tick.
- Publish runtime rule changes as immutable versioned snapshots. Hooks read the last valid snapshot without waiting or modifying it.
- Require an expected revision for rule mutations so stale controller edits are rejected without changing the active rules.
- Keep runtime edits in memory. Persistence is an explicit controller action that writes YAML outside the injected DLL.

## Rendering and file-format documentation

- Separate renderer behavior from the file format that supplies its data.
- Explain the live frame path from pane or world draw through canvas composition and presentation.
- Distinguish software drawing and blending from the final DirectDraw or GDI presentation step.
- For each format, record byte order, header size, record size, offsets, counts, alignment, compression, palettes, and unknown fields when known.
- Use one main page per confirmed format. Keep internal storage class names separate from unproven file extensions.
- State whether writing is client-confirmed, a generated inverse of the reader, or still incomplete.
- Do not call an encoder compatible until a decode, encode, decode round trip preserves the meaningful fields and pixels.
- Preserve unknown fields from a compatible source when showing a generated writer. Do not silently fill them with guessed constants.
- Keep pseudocode short. Show the smallest read or write loop that makes the layout usable.
- Put large mode tables, address lists, and deeper structure layouts in appendices or deterministic YAML exports.

## Audio documentation

- Separate the game-owned playback rules from the codec and mixer supplied by middleware.
- Record the requested output format, source codec, sample rate, channel count, bitrate range, storage path, and naming convention when local assets confirm them.
- Check file headers instead of treating an extension as proof of a codec.
- Keep music streams, sound-effect samples, video sound, and dormant MIDI code as separate paths.
- For volume, record the user-facing range, internal conversion, default, clamp behavior, and where the value is applied.
- For fades, record the timer interval, step rule, stream lifetime, and whether two tracks overlap.
- Distinguish compiled codec or MIDI support from a path reached by the matching game flow and assets.
- Link packet-driven audio behavior from both the packet page and the audio system page.

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

## Map and rendering documentation

- Treat `tilea.bmp` and `tileas.bmp` as raw fixed-record tile banks, not Windows BMP files.
- Keep alternate map art separate from weather particles. `SMapSize` bit `0x80` selects alternate ground and static art, while its low nibble selects local weather behavior.
- Describe `SOTP.DAT` as two independent flag groups: collision in the low nibble and static render behavior in the high nibble.
- State whether a wall-visibility change hides all `WorldObject_Static` art, only render-flagged occluders, or collision-bearing statics. These choices are not equivalent.
- Keep table-driven ground and static animation separate from server-driven map state. The client advances `gndani.tbl` and `stcani.tbl` locally on a timer.

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

Keep the main book focused on named functions and behavior. Put static addresses, RVAs, bytes, confidence, and long lookup tables in the matching appendix or YAML export.

Object-relative field offsets may stay beside a compact structure when they are needed to explain the layout. Packet field positions may stay on packet pages when they define the wire format.

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

Do not present a static Binary Ninja address as a stable runtime address without explaining the image base or relocation requirement. Main prose should link the function reference once and use function names after that.

## Packet documentation

`SPacket` means server-to-client. `CPacket` means client-to-server.

Write the word `packet` in full in documentation and user-defined symbols. Do not abbreviate it. Quote a compiler-recovered abbreviation only when the exact spelling is necessary evidence.

Use `SPacket` and `CPacket` only as generic direction terms. Concrete display names omit the redundant `Packet` suffix, even when related material includes it. Write `SUserPosition`, `CVersion`, and `CRefresh`, not their suffixed forms. Packet page and navigation titles use the friendly name followed by the concrete class name, such as `User Position (SUserPosition)` or `Version (CVersion)`.

Preserve exact server class names recovered through RTTI even when a friendlier behavioral label is useful. Client packet names supplied by the project owner are protocol vocabulary, not compiler-recovered RTTI. Record that provenance and keep descriptive aliases separate when the names differ. Do not force paired client and server names to match.

Verified concrete packet names do not use a trailing `?`. If part of a packet remains uncertain, keep the verified name and state the specific unknown in its page rather than making the whole packet name look tentative.

Some control bodies may resemble an opcode-first packet without representing a normal packet class. Document their exact bytes, framing path, and sequence effects instead of forcing them into the ordinary packet model.

Every client packet page should include known UI pane or subsystem owners when they can be reached reliably. Keep exact call addresses and unnamed containing functions in YAML exports or an address appendix. State when the owner is unresolved, and do not imply that static cross-references cover indirect or queued runtime calls.

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
- Parser, handler, builder, or sender names, with addresses kept in the lookup material
- State changes and UI effects
- Paired request or response packets
- Unknown fields and the reason they remain unknown

Keep master indexes synchronized with packet pages.

Client and server packet indexes and sidebar entries use a zero-padded uppercase hexadecimal label followed by the friendly and concrete names, such as `0x0E - Say (CSay)`.

Keep client and server opcode evidence separate. The server direction may have RTTI-backed concrete class names. The client direction has no recovered derived packet RTTI classes, so each friendly client name must cite builder behavior or related-name provenance.

Do not treat absence from the server packet factory as proof that an opcode is unused. Search decoded-body event consumers in UI panes, session state, and manager classes. An RTTI-backed owner may handle a raw decoded buffer without constructing a concrete RTTI packet object. Record the packet name provenance separately from the owner class RTTI.

Record the common transform as `raw`, `static`, or `derived` on each packet page. Do not infer one direction's opcode policy from the other direction.

When documenting common packet encryption, distinguish the static key, the per-packet 9-byte derived key, the 1024-byte MD5 salt source, the 256-entry seed XOR table, the sequence, and direction-specific trailers. Do not collapse these into a single generic salt or key.

Use `sequence` for the byte that advances on every encrypted packet. Keep client-to-server and server-to-client sequence streams separate, and do not confuse either sequence with the negotiated seed-table selector. Raw packets do not advance an encrypted-packet sequence.

Treat the sender and receiver as separate owners of local sequence state. For client-to-server traffic, the client's send counter and the server's receive counter advance in step but are not one shared counter. The reverse direction has its own pair.

## File format documentation

- Treat an extension as a naming convention, not proof of one shared layout. Document the reader that selects the format.
- Keep the container, compression, byte encoding, pixel encoding, palette choice, and render blend as separate layers.
- Use a compact C-like structure for fixed layouts and short pseudocode for variable records or codecs.
- State byte order, offset base, count units, terminators, size limits, and alignment when each is known.
- Distinguish compression from obfuscation and checksums. Name the exact algorithm when confirmed.
- Preserve unknown fields and opaque byte strings. Do not assign text or alpha meaning from appearance alone.
- For generated writers, say whether the client contains a writer, the inverse is only derived, or a decode, encode, decode round trip passed.
- Validate a format across several local samples when possible. Record useful sample counts without committing private asset content.
- Treat palette index transparency and destination-dependent blending as render behavior unless the file itself carries verified alpha.

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
