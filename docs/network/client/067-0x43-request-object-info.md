# Request Object Info (`CRequestObjectInfo`)

`CRequestObjectInfo` carries two confirmed world-interaction forms. Living entities use an object ID. Static map objects, including the path used when a player clicks a door, use tile coordinates and a left or right static-layer selector.

| Item | Value |
| --- | --- |
| Direction | Client to server |
| Opcode | `0x43` |
| Transform | `static` |
| Name provenance | Project-owner protocol name; subtype `1` is confirmed against merchant and world-object paths, while subtype `3` is confirmed from the static-object click path |
| UI owner | Living-object click, static-object click, and merchant object-selection paths |

The client has no derived packet RTTI for this name. The confirmed builders send one of two bodies.

## Living entity

Subtype `1` sends a four-byte big-endian entity identifier. It is used for players, monsters, and NPCs. The provisional owner-named [`SObjectInfo`](../server/052-0x34-object-info.md) is one paired response for user objects and opens exact RTTI `UserInfoPane_ForOthers`. The server can choose a different conversation or UI response for other entity categories.

## Sent by

Known subtype-1 callers lead to:

- merchant object-selection paths
- the world-object click handler

For clicked user objects, the local `UserClickMode` setting can suppress this request. Other object categories continue through their normal click paths.

## Body

```text
packet CRequestObjectInfo {
    u8      opcode                    // 0x43
    u8      subtype                   // 1
    u32     entity_id
}
```

## Static map object

Subtype `3` is produced when a left press hits visible `WorldObject_Static` art. Empty-ground left click does not send it.

```text
packet CRequestObjectInfo {
    u8      opcode                    // 0x43
    u8      subtype                   // 3
    u16     tile_x
    u16     tile_y
    u8      static_side               // 0 left, 1 right
}
```

The world object stores the opposite internal side convention: `1` is left and `0` is right. `net_send_world_static_interaction` inverts that internal value while building the packet.

Both world producers suppress submission while the unresolved state at `WorldPane +0x258` is nonzero. The server decides whether the selected static changes. A later [`SStaticObjectState`](../server/050-0x32-static-object-state.md) can update its live art and collision tile.

The complete pointer and direct-call flow is in [World interactions](../../systems/world-interactions.md).
