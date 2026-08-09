# World interactions

An ordinary click on a living entity and a click on a map static use two variants of the same client packet. Players, monsters, and NPCs use an entity ID. Doors and other static map art use tile coordinates plus a left or right static-layer selector. An empty ground tile has no left-click interaction packet.

## Input flow

The world pane offers a pointer event to the live world objects from front to back. The first object whose visible bounds consume the event decides what happens next.

| Input target | Client result |
| --- | --- |
| Player, monster, or NPC | Living-object action `4`, then [`CRequestObjectInfo`](../network/client/067-0x43-request-object-info.md) subtype `1` with the entity ID |
| Another player while Ctrl is held | Opens the local player popup; the click sends no packet |
| Static map object such as a door | World-object message `0x50001`, then opcode `0x43` subtype `3` with tile X, tile Y, and static side |
| Empty ground with left button | No interaction packet |
| Empty ground with right button | Starts local click-to-move pathfinding |
| Living entity with double-right button | Starts local pursue-and-auto-attack behavior |

A double-left press takes the same living-object action `4` path as an ordinary left press. It has no separate packet meaning.

## Interacting with an entity

`world_living_handle_pointer_event` hit-tests the living object's drawn bounds. A left press calls `world_living_dispatch_left_click_action`, which retains the object's `u32` ID and dispatches action `4`. `ui_world_pane_handle_living_object_message` then applies the local player-specific rules before calling:

```c
u32 __thiscall net_send_world_entity_interaction(
    WorldPane *world,
    u32 entity_id);
```

This producer queues opcode `0x43`, subtype `1`, and the big-endian entity ID. It sends only while the unresolved `WorldPane +0x258` state is zero.

The native UI path rejects the local character. For category-1 user objects, Ctrl opens the player popup and a positive `UserClickMode` suppresses the ordinary packet. NPC and monster categories do not use that `UserClickMode` gate.

For a direct entity action, resolve `entity_id` through `world_find_object_by_id` during the main-thread command tick and require a current `WorldObject_Living` that is not the local object. Then call `net_send_world_entity_interaction`. This deliberately performs the server interaction, so it bypasses Ctrl-popup behavior. Reproduce the `UserClickMode` check separately if the command is meant to behave exactly like an ordinary player click.

`net_request_object_info` builds the same subtype-1 body for a merchant target context, but it lacks the WorldPane state gate and keeps a context-shaped `ECX` calling convention. The WorldPane producer is the clearer direct entry for a world entity.

The server decides the result. A player can produce the other-user information pane, while an NPC can begin a server-owned merchant, pursuit, or menu conversation.

## Interacting with a static tile

A door click is not an empty-ground click. `world_static_handle_pointer_event` must first hit visible `WorldObject_Static` art. It dispatches the object's tile and side to `ui_world_pane_handle_world_object_message`, which calls:

```c
u32 __thiscall net_send_world_static_interaction(
    WorldPane *world,
    u16 tile_x,
    u16 tile_y,
    u8 internal_side);
```

The internal side is `1` for the left static layer and `0` for the right static layer. The producer inverts it on the wire, where `0` means left and `1` means right. It uses the same `WorldPane +0x258 == 0` gate as entity interaction.

A coordinate alone can be ambiguous because one map cell has independent left and right static slots. A direct `(x, y)` command should:

1. Validate the coordinate against the current map.
2. Resolve the left and right live objects with `world_get_static_object_at_tile_side`. That lookup accepts the wire convention, `0` for left and `1` for right.
3. If exactly one side contains a live `WorldObject_Static`, read its internal side at `+0x80` and call the sender.
4. If both sides contain statics, require an explicit side or object choice instead of guessing.

The lookup returns a reference-counted object, so a wrapper must follow the client's retain and release convention. Do not keep that object pointer between dispatcher ticks.

The packet does not claim that the selected static is a door. It reports the same interaction the native hit-test would have reported, and the server decides whether that tile changes state. Later [`SStaticObjectState`](../network/server/050-0x32-static-object-state.md) updates replace the live tile art and collision state.

## Direct-call rules

Run both producers on the main game thread. Resolve the complete live `WorldPane`, entity, map dimensions, and static object again for every command. Do not retain pointers from IPC or an earlier frame.

Static addresses, RVAs, calling contracts, and evidence are in [Manual native actions](../appendix/runtime/manual-actions.md#interact-with-a-world-entity-or-static) and [`analysis/exports/manual-actions.yaml`](../../analysis/exports/manual-actions.yaml).
