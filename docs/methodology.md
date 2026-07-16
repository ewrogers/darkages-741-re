# How we study the client

The goal is to explain the game, not to fill pages with disassembly. We start from something visible, follow it through the client, and keep the proof where other contributors can check it.

## A small investigation loop

1. Pick one question, such as "what sends the map request?"
2. Find a strong clue: a command code, string, import, RTTI class, or known function.
3. Follow callers and callees until the game behavior is clear.
4. Check important branches and data layouts against lower-level views.
5. Name and comment the result in Binary Ninja.
6. Export the durable details to YAML and update the matching book page.

This is similar to tracing a signal through a game engine. Start at the input or event, follow the systems it crosses, and stop when both the trigger and result make sense.

## Source of truth

The matching client wins when sources disagree. Older notes, related games, packet captures, and project-owner knowledge are useful leads, but each conclusion should connect back to local code or observed behavior.

The `legacy/` directory is an archive of leads. It is not part of the current book.

## Names and confidence

Use short subsystem names:

- `app_` for application lifecycle and configuration
- `game_`, `session_`, and `character_` for narrower state
- `net_` for networking
- `event_`, `input_`, and `ui_` for game events and interface code
- `render_`, `audio_`, `file_`, and `map_` when those systems are confirmed

Use `maybe_` when a useful function name is still uncertain. Documentation may place `?` after a reconstructed class or field name.

RTTI proves a class spelling and inheritance relationship. It does not prove the purpose of every method. Behavior still needs to be traced.

## Main pages and lookup pages

Main pages use function names and explain behavior in game terms. They avoid long address lists.

Use the appendices and YAML exports for:

- static addresses and RVAs
- original and replacement bytes
- confidence and evidence notes
- full pane inheritance
- call sites and unnamed helper functions

Object offsets may stay beside a small structure when they are needed to understand the object. Wire positions stay on packet pages because they define the protocol.

## Packet work

Keep client and server command codes separate. The same byte can mean something different in each direction.

For each packet, record the name source, transform mode, known body fields, trigger or handler, visible effect, paired messages, and unknowns. Do not invent a field name just to make a layout look complete.

## Text and localization

The client may contain Korean text that renders as `????` on another Windows locale. Preserve the original bytes before guessing. Test code page 949 when the bytes support it, and say clearly when the original text cannot be recovered.

## Runtime patches

Patch research documents changes for a launcher that edits suspended process memory. It does not modify the executable on disk.

A safe patch verifies the exact client fingerprint and original bytes, uses the loaded module base, writes complete instructions, flushes the instruction cache, and stops on any mismatch. See [Runtime patches](appendix/runtime-patches.md).
