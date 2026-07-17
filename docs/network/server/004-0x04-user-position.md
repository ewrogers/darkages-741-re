# User Position (`SUserPosition`)

`SUserPosition` snaps the local player and world view to an authoritative tile coordinate. The client consumes only `x` and `y`. The two additional words seen in captures remain trailing bytes and have no effect in client 7.41.

| Item | Value |
| --- | --- |
| Direction | Server to client |
| Command | `0x04` (4) |
| Transform | derived |
| Runtime owner | `WorldPane` and `WorldObject_User` |
| Name provenance | Microsoft C++ RTTI in the target |

## Body

The concrete RTTI packet object is only `0x14` bytes. Its deserializer reads exactly two words into the two fields following the `0x10`-byte packet base:

```text
packet SUserPosition {
    u8      opcode                    // 0x04
    u16     x                         // packet object +0x10
    u16     y                         // packet object +0x12

    // Observed in captures, but not read by client 7.41:
    u16     observed_trailing_0
    u16     observed_trailing_1
}
```

The two trailing `u16` types describe their observed capture shape. The client does not read these bytes at all, so it supplies no evidence for their original names or even whether their producer regards them as two words rather than four opaque bytes.

The supplied login trace makes the boundary visible:

```text
04 00 2B 00 28 00 0B 00 0B 00
   \___/ \___/ \___/ \___/  |
     x     y    ignored ignored local receive terminator
```

That places the player at `(43, 40)`. Both observed trailing words are `11`. The final zero is consistent with the separate local buffer terminator written by `net_decrypt_server_packet`; it is not another `SUserPosition` field.

`net_deserialize_user_position_server_packet` returns immediately after reading `y`. The main dispatcher then gives `net_handle_user_position_server_packet` only the RTTI packet object. It does not pass the raw decoded body to the opcode `0x04` handler. There is therefore no later client path that can use the four trailing bytes.

## Applying the position

Although the reader is named for unsigned `u16`, the handler sign-extends both stored words before using them:

```c
x = (s16)packet.x;
y = (s16)packet.y;

self = world_get_self_user_object();
if (self != NULL) {
    self->tile_y = y;
    self->tile_x = x;
    world_reindex_object(self);
}

world_set_view_position(y, x, true);
```

`WorldObject` stores `tile_y` before `tile_x`, which explains the reversed-looking memory writes. The wire order remains `x`, then `y`. Reindexing updates the spatial object collection after the coordinate replacement. Updating the view stores the same position in `WorldPane`, rebuilds visible static objects and the light mask, and invalidates the world for redraw.

The self-object lookup is guarded. If the local `WorldObject_User` has not been created yet, the client skips its object writes but still moves the world view.

## Why use 16-bit coordinates?

This does not make the active map grid larger. Client 7.41 reads `SMapSize` width and height as one byte each, then widens them in memory. Local movement checks still require:

```text
0 <= x < map_width
0 <= y < map_height
```

One grid loaded through that path is therefore still limited to 255 cells on either axis. Values at or above `0x8000` also become negative when this handler sign-extends them.

The wider wire fields appear to be a protocol-wide coordinate choice. `SDrawHumanObjects` also carries its object coordinates as `u16`, while the client stores and calculates positions as 32-bit integers. That can explain how the format has more range than this map loader needs, but the binary does not reveal whether the original reason was engine reuse, older transports, or planned larger maps.

[`SMove`](011-0x0b-move.md) handles subsequent server movement updates, while [`CMove`](../client/006-0x06-move.md) reports locally attempted steps.
