# Authoring guide

Write an explanation a game or network programmer can follow, with enough exact detail to implement or verify it. This guide owns the book’s voice, reading depth, examples, and figures. The [contributor handbook](../CONTRIBUTING.md) covers the change workflow and checks; [research policy](research-policy.md) owns evidence and subsystem requirements. Paths in code spans are relative to the repository root.

Use this guide by need: [audience and voice](#book-audience-and-voice), [topic organization](#book-organization), [page shape](#book-authoring-style), [pseudocode](#code-and-pseudocode-style), [reading depth](#reading-depth), [worked explanations](#voice-and-worked-explanations), and [diagrams](#diagrams-that-explain-a-relationship).

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
- Use C-style pseudostructs for runtime memory and fixed file layouts. Packet wire layouts use the shared [field-list notation](../docs/network/packet-body-notation.md), not C structs.
- Era-appropriate C++ is acceptable when classes, vtables, constructors, or destructors are relevant.
- Avoid templates, lambdas, ranges, heavy STL use, clever macros, and modern language features that obscure the algorithm.
- Use straightforward loops, explicit branches, and small helper functions.
- Use fixed-width protocol names such as `u8`, `u16`, and `u32` when documenting wire fields.
- Packet body schemas use the book's global big-endian rule and write `u16`, `u24`, and `u32` without an endian suffix. State endianness explicitly for file formats and other data where it is not fixed by that packet rule.
- Preserve bounds, loop counts, conditional fields, and nested structures.
- Keep examples expressive rather than production-framework specific.
- Do not include a full launcher, injected DLL, or other compile-ready program in the book when pseudocode explains the design.

## Writing a consistent page

Open with what the client does and why the behavior matters. Follow with the flow, the named functions or objects involved, and the details a reader needs to use the result. Keep reconstructed behavior, observed captures, proposed extensions, and unresolved questions distinguishable.

Packet pages put that purpose before the metadata table. Use `Transform` with `raw`, `static`, or `derived`, then describe the body in the shared [packet notation](../docs/network/packet-body-notation.md). Keep fragmentary or observed bodies labeled as such. Use behavior-specific headings for the remaining sections and `Known limits` when a separate uncertainty section is useful.

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

The [game loop](../docs/application/game-loop.md), [event system](../docs/systems/events.md), and [UI and panes](../docs/systems/ui.md) form the first worked reading path. [NPC dialogs](../docs/systems/npc-dialogs.md) applies the same progression to a larger topic with live exchanges, exact selection rules, native invocation, and dormant implementations.

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

The [walking timeline](../docs/rendering/players.md#walk-timeline-and-world-displacement), [music replacement](../docs/audio/music.md#fade-timer), [pursuit exchange](../docs/systems/npc-dialogs.md#pursuit), and [packet byte example](../docs/network/packet-body-notation.md#a-body-in-bytes) demonstrate these conventions.

Each figure answers one question. Label arrows with the action or message they carry. Use arrow direction and written labels to show meaning; color is only a secondary cue. Show optional or alternative paths explicitly, and state which paths a focused example leaves to the surrounding reference. Never give a waiting period a proportional length unless its duration is established.

Keep the complete explanation available as text and retain exact schemas and tables as the reference. Give the image meaningful alternative text and a caption stating the takeaway and any limit that affects interpretation. A diagram must not become a second, less qualified source of truth.

#### Authoring and checking figures

Store editable, self-contained SVG source in `docs/assets/diagrams/`. Use descriptive lowercase filenames, a `viewBox`, and a `<title>` and `<desc>`. Keep labels as text, with system sans-serif for prose and monospace for identifiers, bytes, and exact values. Use dark brown ink on a plain parchment surface; avoid textures behind information. Do not embed private game art, external fonts, scripts, or remote resources.

Use the `figure.diagram` and `.diagram-scroll` wrapper shown in the worked pages. The scroll region needs an accessible name and `tabindex="0"` so keyboard users can pan it. Include the `.diagram-hint` text and a full-size source link in the caption. `theme/diagrams.css` keeps wide figures readable on small screens and fits them to the printed page. `theme/diagrams.js` lets Left and Right scroll a focused diagram without triggering mdBook's chapter shortcuts; Tab still leaves the region normally.

When behavior changes, update the explanation, exact reference, and figure in the same change. Check every constant, branch, owner, and direction against the canonical text or evidence. Build with the CI-pinned mdBook version and inspect the rendered page at desktop and narrow widths, with keyboard focus and in print. Verify that labels remain readable in light and dark themes, in monochrome, and without the image. Use the handbook's [temporary build or ignored preview directory](../CONTRIBUTING.md#run-the-checks); keep rendered output out of authored sources.

## Review two reading paths

Follow the changed topic once as a programmer meeting the subsystem for the first time. Can you state the visible result, identify each owner, and follow the normal and failure paths without interpreting an address? Define a missing term where it matters, and move proof that interrupts the explanation to its canonical reference.

Then follow it as someone implementing the behavior. Check field order, units, bounds, timing, variants, and ownership against the reference. Follow a named function to its specific evidence entry and source record. Make sure the simpler explanation has not dropped a condition, exception, or unresolved case.

Automated checks cover structure and freshness. A passing build cannot establish a client behavior, resolve an identity warning, or decide whether an explanation is understandable. Report those review limits with the change.
