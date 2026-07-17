# Runtime structures

The client keeps different kinds of runtime state in different owners. This index groups the mapped layouts by lifetime and subsystem so a reader does not have to search one long page. Offsets are relative to the object shown. They are not static process addresses.

## Structure groups

| Group | Contents |
| --- | --- |
| [Network packet objects](runtime/network-objects.md) | Decoded events, connection handshake fields, and parsed server packet objects |
| [Session and character state](runtime/session.md) | Compact inventory, spell, skill, status, and local-user records owned by `WorldUserFunc` |
| [Inventory and character panes](runtime/inventory-ui.md) | Inventory, spell, skill, equipment, status, mail, and casting UI objects |
| [Pane and event layouts](runtime/panes.md) | Events, dispatch slots, pane-tree entries, shared pane fields, messages, timers, and dialogs |
| [Rendering objects](runtime/rendering.md) | Video-system, DirectDraw, and canvas fields |
| [World objects](runtime/world.md) | Human appearance and static map-object fields |

The [pane type appendix](pane-types.md) is the RTTI-backed class inventory. The [function reference](functions.md) records static addresses and evidence notes for the functions that operate on these layouts.
