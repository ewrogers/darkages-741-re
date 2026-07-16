# SOTP static tile flags

`SOTP.DAT` gives each static tile its collision and render flags. The file is a raw byte array with no header.

```c
struct SotpEntry {
    u8 flags;                  // low nibble: collision
                               // high nibble: rendering
};
```

File byte zero belongs to static tile ID 1. The client adds an empty runtime entry at index zero, so map tile IDs can index the loaded tables directly.

The matching file is 20,423 bytes long and therefore covers static tile IDs 1 through 20,423.

## Collision bits

The low nibble can block movement by direction:

| Bit | Grid move |
| --- | --- |
| `0x01` | left, `(-1, 0)` |
| `0x02` | down, `(0, +1)` |
| `0x04` | right, `(+1, 0)` |
| `0x08` | up, `(0, -1)` |

`map_can_move_direction` checks dynamic occupants first. It then reads the two static tile IDs on the source and destination edges and tests the bit for the requested direction. Static tile ID `0x2710` is treated as empty.

The matching `SOTP.DAT` contains only four byte values:

| Byte | Count | Meaning |
| --- | ---: | --- |
| `0x00` | 4,265 | Open, normal rendering |
| `0x0F` | 15,782 | Blocks all four directions |
| `0x80` | 322 | Open, special over-player blend |
| `0x8F` | 54 | Fully blocked, special over-player blend |

The engine supports separate direction bits even though this file mostly uses all-or-nothing collision.

## Render bits

`render_build_static_objects` copies the high nibble into each `WorldObject_Static`.

- `0x80` selects the screen-style wall and tree blend described in [Walls and occlusion](../rendering/walls-and-occlusion.md).
- `0x40` selects another blend mode, but the matching file has no entries with that bit.
- Zero uses normal opaque drawing.

Collision and rendering are independent. A tile may block movement without using the over-player blend, or use the blend without blocking movement.

## Create the file

Write one byte per static tile ID, starting with ID 1:

```text
entry = (render_flags & 0xF0) | (collision_flags & 0x0F)
```

Keep the file long enough to cover every static tile ID used by the maps. An out-of-range ID receives no SOTP flags.
