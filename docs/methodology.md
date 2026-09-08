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

Runtime type information (RTTI) is compiler-generated data that records class names and inheritance. It proves a class spelling and inheritance relationship, but not the purpose of every method. Behavior still needs to be traced.

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

## Writing a consistent page

Open with what the client does and why the behavior matters. Follow with the flow, the named functions or objects involved, and the details a reader needs to use the result. Keep reconstructed behavior, observed captures, proposed extensions, and unresolved questions distinguishable.

Packet pages put that purpose before the metadata table. Use `Transform` with `raw`, `static`, or `derived`, then describe the body in the shared [packet notation](network/packet-body-notation.md). Keep fragmentary or observed bodies labeled as such. Use behavior-specific headings for the remaining sections and `Known limits` when a separate uncertainty section is useful.

Overview pages explain how a section fits together and link to its focused topics. Keep long lookup material in the appendices, preserve useful timing values and provenance, and update the [navigation generator](../scripts/README.md) when a page is added. An editorial change should not make an uncertain finding sound established.

### Reading depth

A reader should be able to understand a behavior before needing its memory layout or instruction evidence. Give a focused topic this progression:

| Reader's question | What belongs here |
| --- | --- |
| What happens? | Purpose, visible result, and a small mental model |
| How does it happen? | Owners, a complete normal flow, state changes, and relevant failure paths |
| What must an implementation preserve? | Exact fields, ordering, counts, bounds, timing, and exceptions |
| How is it established? | Links to the matching layouts, named functions, and evidence reference |

Use headings that describe the behavior rather than repeating these four questions on every page. Keep a short packet or format reference together when its exact layout is already the most useful explanation. Split a topic only when the reader's purpose or prerequisites change, not to satisfy a page-length target.

Keep uncertainty and correctness conditions beside the behavior they qualify. A dormant path must be labeled before a reader could mistake it for live behavior. A timer's cadence, callback limit, and total duration must remain distinct. Required fields, bounds, and warnings should not depend on expanding an optional section.

Put a shared layout in one canonical reference. Explain how its fields affect behavior in the main chapter, then link to the exact section. Before removing a duplicate, transfer any unique fields or exceptions. Preserve existing heading anchors when moving or regrouping sections.

The [game loop](application/game-loop.md), [event system](systems/events.md), and [UI and panes](systems/ui.md) form the first worked reading path. [NPC dialogs](systems/npc-dialogs.md) applies the same progression to a larger topic with live exchanges, exact selection rules, native invocation, and dormant implementations.

### Voice and worked explanations

Start with an action the reader can picture, then name the mechanism that owns it. For example: "The old track becomes silent before the new track starts. `BGMPlayer` owns one stream and replaces it when the fade reaches zero." Use the same owner, state, and field names in the prose, figure, pseudocode, and reference.

Define a technical term at the point where it changes the explanation. A walking **sample** updates both the pose and displacement; two samples can reuse the same pose. A timer entry runs once; a repeating behavior schedules another entry from its callback. These distinctions explain behavior more usefully than a detached glossary definition.

Give a worked example a starting state, a small sequence of changes, and an observable result. State whether its numbers come from the client, a matching asset, a capture, or an invented teaching example. Explain the relevant limit immediately: nominal timing can slip, text length counts bytes, and a server reply has no fixed arrival time. Follow the example with the exact rule and its exceptions.

Keep the old-spellbook character in the presentation. Technical headings, controls, and explanations use ordinary game and network terms. An event queue remains an event queue, and an unresolved field remains unresolved.

### Diagrams that explain a relationship

Choose a diagram for the question it answers. Keep a short ASCII flow when it already makes the relationship clear; a figure should add useful comparison, ownership, or alignment.

| Reader needs to see | Useful form | What to make explicit |
| --- | --- | --- |
| Which owner acts next? | Sequence diagram | Sender, receiver, message direction, waiting state, and alternative paths |
| When does a state change? | Timeline | Time origin, units, sample boundaries, final hold, and nominal versus measured timing |
| What permits a transition? | State or flow diagram | Guard, action, resulting state, and whether spacing has any timing meaning |
| Which bytes belong to a field? | Byte map | Plaintext or encoded layer, zero-based positions, byte order, lengths, and invented values |
| What contains or inherits what? | Tree | Exact relationship; keep containment, registration, and inheritance separate |

The [walking timeline](rendering/players.md#walk-timeline-and-world-displacement), [music replacement](audio/music.md#fade-timer), [pursuit exchange](systems/npc-dialogs.md#pursuit), and [packet byte example](network/packet-body-notation.md#a-body-in-bytes) demonstrate these conventions.

Each figure answers one question. Label arrows with the action or message they carry. Use arrow direction and written labels to show meaning; color is only a secondary cue. Show optional or alternative paths explicitly, and state which paths a focused example leaves to the surrounding reference. Never give a waiting period a proportional length unless its duration is established.

Keep the complete explanation available as text and retain exact schemas and tables as the reference. Give the image meaningful alternative text and a caption stating the takeaway and any limit that affects interpretation. A diagram must not become a second, less qualified source of truth.

#### Authoring and checking figures

Store editable, self-contained SVG source in `docs/assets/diagrams/`. Use descriptive lowercase filenames, a `viewBox`, and a `<title>` and `<desc>`. Keep labels as text, with system sans-serif for prose and monospace for identifiers, bytes, and exact values. Use dark brown ink on a plain parchment surface; avoid textures behind information. Do not embed private game art, external fonts, scripts, or remote resources.

Use the `figure.diagram` and `.diagram-scroll` wrapper shown in the worked pages. The scroll region needs an accessible name and `tabindex="0"` so keyboard users can pan it. Include the `.diagram-hint` text and a full-size source link in the caption. `theme/diagrams.css` keeps wide figures readable on small screens and fits them to the printed page. `theme/diagrams.js` lets Left and Right scroll a focused diagram without triggering mdBook's chapter shortcuts; Tab still leaves the region normally.

When behavior changes, update the explanation, exact reference, and figure in the same change. Check every constant, branch, owner, and direction against the canonical text or evidence. Build with the CI-pinned mdBook version and inspect the rendered page at desktop and narrow widths, with keyboard focus and in print. Verify that labels remain readable in light and dark themes, in monochrome, and without the image. Keep preview renders and build output outside the source tree.

## Text and localization

The client may contain Korean text that renders as `????` on another Windows locale. Preserve the original bytes before guessing. Test code page 949 when the bytes support it, and say clearly when the original text cannot be recovered.

## Runtime patches

Patch research documents changes for a launcher that edits suspended process memory. It does not modify the executable on disk.

A safe patch verifies the exact client fingerprint and original bytes, uses the loaded module base, writes complete instructions, flushes the instruction cache, and stops on any mismatch. See [Safe launcher workflow](appendix/runtime-patches/safe-launcher.md).
