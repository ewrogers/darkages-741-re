# Inside the Dark Ages client

This book explains how the game client starts, runs, draws its UI, handles events, and talks to the server. It is written for programmers who know common game and network ideas but may be new to older Windows clients.

Start with the question you want to answer. You can read the book without setting up Binary Ninja. Use the appendices when you need an address, exact runtime layout, or proof detail.

## Choose a route

| I want to... | Start here | Continue to the exact details |
| --- | --- | --- |
| Understand one turn of the client | [Game loop](application/game-loop.md) | [Event delivery](systems/events.md#dispatch-flow), then [UI and panes](systems/ui.md) |
| Implement an NPC conversation | [NPC dialogs](systems/npc-dialogs.md) | Choose the [screen-menu or pursuit packet pair](network/README.md#npc-conversations) |
| Decode an asset and draw it correctly | [File formats](file-formats/README.md#choose-a-reader) | Follow the matching reader, its [asset-loading rules](systems/asset-loading.md), and its renderer |
| Find a function or runtime field | [Appendices](appendix/README.md#choose-a-reference) | Use the named function group or the owner-specific layout |

For a command you already know, open the [client](network/client/README.md#packet-index) or [server](network/server/README.md#packet-index) opcode index. The same opcode can mean different things in the two directions.

## The client in layers

| Layer | What it explains |
| --- | --- |
| [Application](application/README.md) | Startup, configuration, lifecycle, and shutdown |
| [Game loop](application/game-loop.md) | Windows messages, queued work, timers, and redraw checks |
| [Game systems](systems/README.md) | Events, input, panes, dialogs, player actions, portraits, and formatted text |
| [Rendering](rendering/README.md) | UI and world drawing, image composition, and presentation |
| [Audio](audio/README.md) | Music, sound effects, volume, and fades |
| [File formats](file-formats/README.md) | Archives, maps, raw tile banks, image frames, effects, and lookup tables |
| [Network](network/README.md) | Connection, transport, transforms, and separate client and server packets |
| [Appendices](appendix/README.md) | Function addresses, runtime patches and structures, pane inheritance, and UI layout mappings |

## Suggested reading order

For a broader introduction, follow the client from startup into its running systems:

1. [Application lifecycle](application/lifecycle.md)
2. [Game loop](application/game-loop.md)
3. [Event system](systems/events.md)
4. [UI and panes](systems/ui.md)
5. [UI layout files](systems/ui-layouts.md)
6. [Rendering system](rendering/README.md)
7. [Audio system](audio/README.md)
8. [File formats](file-formats/README.md)
9. [Network system](network/README.md)

The [function reference](appendix/functions.md) is available whenever a chapter's named routines need closer inspection. It is not a prerequisite for following the client.

## Study the binary or contribute

[Getting started](getting-started.md) sets up the matching private client, Binary Ninja, and MCP. [How we study the client](methodology.md) explains the evidence workflow and how to write a finding. These pages support research work; the behavior chapters above are the reading entry point.

## How facts are recorded

The matching client is the source of truth. Binary Ninja names, comments, and types are exported as reviewable YAML under [`analysis/exports/`](../analysis/exports/README.md).

The main pages explain what the game does. Appendices and exports keep the addresses, instruction bytes, confidence, and detailed provenance. An uncertain reconstructed class or field name can end in `?` in the book or start with `maybe_` in Binary Ninja. Verified packet names keep their spelling; their pages state any uncertainty about fields or behavior separately.

See [How we study the client](methodology.md) for the full workflow.
