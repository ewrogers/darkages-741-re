# Inside the Dark Ages client

This book explains how the game client starts, runs, draws its UI, handles events, and talks to the server. It is written for programmers who know common game and network ideas but may be new to older Windows clients.

Start with behavior. Use the appendices when you need an address or proof detail.

## The client in layers

```text
Application
  +-- startup and configuration
  +-- game loop and shutdown

Game systems
  +-- events and input
  +-- UI panes and dialogs

Network
  +-- connection and transport
  +-- packet transforms
  +-- client and server packets

Lookup material
  +-- function addresses
  +-- runtime patches
  +-- runtime structures
  +-- pane inheritance
  +-- YAML analysis exports
```

## Suggested reading order

1. [Application lifecycle](application/lifecycle.md)
2. [Game loop](application/game-loop.md)
3. [Event system](systems/events.md)
4. [UI and panes](systems/ui.md)
5. [Network system](network/README.md)

The [function reference](appendix/functions.md) is an address book, not required reading. Packet programmers can jump straight to the [client](network/client/README.md) and [server](network/server/README.md) command indexes.

## How facts are recorded

The matching client is the source of truth. Binary Ninja names, comments, and types are exported as reviewable YAML under [`analysis/exports/`](../analysis/exports/README.md).

The main pages explain what the game does. Appendices and exports keep the addresses, instruction bytes, confidence, and detailed provenance. Uncertain names end in `?` in the book or start with `maybe_` in Binary Ninja.

See [How we study the client](methodology.md) for the full workflow.
