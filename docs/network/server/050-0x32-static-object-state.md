# Static Object State (`SStaticObjectState`)

`SStaticObjectState` changes one of the two static objects drawn at a map tile. Doors are the common use: the server identifies the tile, the left or right isometric layer, and which of two paired static tile IDs should become active.

The active tile ID supplies both the art and the local collision flags. The client therefore does not need a separate door-collision Boolean.

## Packet details

| Property | Value |
| --- | --- |
| Direction | Server to client |
| Opcode | `0x32` |
| Concrete class | `SStaticObjectState` |
| Name source | Exact RTTI |
| Transform | `derived` |
| Client response | None |

## Body

```text
packet SStaticObjectState {
    u8 opcode                    // 0x32
    u8 record_count
    repeat record_count {
        u8 x
        u8 y
        u8 state
        u8 side
    }
}
```

The record count can describe up to 255 changes in one packet.

## State and side

`side` chooses one of the map cell's two isometric static layers. The client treats it as a Boolean:

| Wire value | Internal static slot |
| --- | ---: |
| `0` | Left static, slot `1` |
| Any nonzero value | Right static, slot `0` |

This mapping is confirmed where the client builds its static-object index: it inserts the map cell's left static tile with internal side `1` and its right static tile with internal side `0`. The packet handler applies the same internal-side convention after inverting the wire Boolean.

`state` is also Boolean in practice:

| Wire value | Target in the state-pair table |
| --- | --- |
| `0` | Column 1 |
| Any nonzero value | Column 0 |

The client contains 66 pairs of static tile IDs. It looks up the selected live `WorldObject_Static` tile ID in either column, records the matching row, and moves that object to the requested column. A tile not present in this table does not change.

This proves two packet-driven states, not a general numeric animation state. It is tempting to name them open and closed, but that is not universal. In the matching `SOTP.DAT`:

- 43 pairs change from fully blocked in column 0 to open in column 1.
- 22 pairs remain fully blocked in both columns.
- One pair has the reverse collision ordering.

For the common door pair, state `0` therefore opens local collision and a nonzero state closes it. The other rows may represent multi-tile door pieces or other stateful static art.

## Visual and collision update

The handler resolves the requested static layer at `(x, y)` and changes that object's live tile ID. The tile setter reloads its static image and bounds, then invalidates it for drawing.

Local movement later asks each `WorldObject_Static` for its current live tile ID and looks that ID up in `SOTP.DAT`. The packet does not rewrite the original map cell and does not install a separate collision override. Art and collision stay synchronized because both use the replacement tile ID.

The transition helper can requeue its state message after 150 ms while another table step remains. The present table has only two columns, so the visible tile and collision change on the initial handler call; the delayed callback only completes the transition state when needed.

## Failure cases

The record has no effect when the coordinate has no static object on the selected side, the object is not an exact `WorldObject_Static`, or its current tile ID is absent from the 66-pair table.

See [SOTP static tile flags](../../file-formats/sotp.md), [map format](../../file-formats/map.md), and [movement and swimming](../../systems/movement-and-swimming.md).
