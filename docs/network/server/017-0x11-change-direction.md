# Change Direction (`SChangeDirection`)

`SChangeDirection` sets the facing of one living world object. The target does not have to be the local player, so the server can turn another player, a creature, or a Mundane without moving it.

| Item | Value |
| --- | --- |
| Direction | Server to client |
| Command | `0x11` (17) |
| Transform | derived |
| Runtime owner | `WorldPane` |
| Name provenance | Microsoft C++ RTTI in the target |

## Plaintext body

```text
packet SChangeDirection {
    u8      opcode                    // 0x11
    u32     user_id                   // target world object ID
    u8      direction                 // Direction
}
```

`direction` uses the shared [`Direction`](../protocol-types.md#direction) type. Despite its wire name, `user_id` is passed to the general world-object lookup and is not restricted to player objects.

`net_deserialize_change_direction_server_packet` consumes exactly these five bytes after the opcode. The class defines no additional stored or skipped fields.

## Applying the turn

```text
find user_id in the world object index
    |
    +-- missing --> send CRequestObject(user_id)
    |
    +-- found --> require WorldObject_Living
                     |
                     +-- living ----> set direction
                     +-- not living -> ignore
```

`net_handle_change_direction_server_packet` performs an RTTI cast from the found `WorldObject` to `WorldObject_Living`. This includes `WorldObject_User`, other `WorldObject_Human` instances, and `WorldObject_Monster`. Creatures and Mundanes both use `WorldObject_Monster`, so the packet can turn them too. Ground items are not living objects and fail this check.

If the object is missing, the handler sends [`CRequestObject`](../client/012-0x0c-request-object.md) with the same ID so the server can describe it. A present but non-living object is simply ignored.

`world_living_object_set_direction` does nothing when the direction already matches. Otherwise it runs the object's transition hook, stores the facing byte at living-object offset `+0x192`, and refreshes the directional motion or image state.

## Relationship to the client request

[`CChangeDirection`](../client/017-0x11-change-direction.md) carries no object ID because it always requests a turn for the local player. This server packet supplies the ID, so it works both as the normal authoritative response and as an independent server-directed turn for another living object.

The handler does not range-check `direction`. Confirmed client producers and normal world records use values `0` through `3`; behavior for other values is not established.
