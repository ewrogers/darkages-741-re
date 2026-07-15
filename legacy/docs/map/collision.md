# Collision and SOTP flags

Static wall collision comes from `SOTP.DAT`, not directly from a special bit inside each `.map` cell. A map cell stores two static tile identifiers. Each identifier selects one byte from `SOTP.DAT`; the byte's low nibble is a four-direction wall mask.

## Loading SOTP.DAT

`SOTP.DAT` is the first entry in the local `ia.dat` archive. The observed entry starts at archive offset `0x63188` and is 20,423 bytes long.

The client loads the same entry twice:

- `map_load_sotp_collision_flags` at `0x5CF4F0` stores `value & 0x0F` in the world pane table at `+0x1A0`.
- `map_load_sotp_render_flags` at `0x5CF3B0` stores `value & 0xF0` in the world pane table at `+0x1B0`.

Both routines allocate one extra leading byte and set it to zero. Static tile identifiers can therefore index the runtime tables directly:

```c
collision_flags[0] = 0;
render_flags[0] = 0;

for (i = 0; i < sotp_size; i++) {
    collision_flags[i + 1] = sotp[i] & 0x0f;
    render_flags[i + 1] = sotp[i] & 0xf0;
}
```

Tile identifier zero means no static tile. A stored identifier `n` uses source byte `sotp[n - 1]` and runtime entry `flags[n]`.

## Direction bits

The direction-mask table at `0x6D395C` begins:

```text
01 02 04 08 03 06 0c 09
```

The first four entries are the cardinal masks used by movement validation:

| Direction | Mask | Meaning |
|---:|---:|---|
| `0` | `0x01` | North |
| `1` | `0x02` | East |
| `2` | `0x04` | South |
| `3` | `0x08` | West |

`map_direction_delta` at `0x5BE580` confirms the cyclic north, east, south, west coordinate changes. The following four table values combine adjacent cardinal bits and are consistent with diagonal directions, although the main one-step movement validator uses the first four.

## Movement validation

`map_can_move_direction` at `0x5EFFE0` returns 1 when a step is allowed and 0 when it is blocked. Its full behavior includes more than static walls:

1. Calculate the destination with `map_step_coordinate` at `0x5BE600`.
2. Reject out-of-bounds coordinates.
3. Apply player state and movement-mode exceptions.
4. Inspect dynamic world objects at the destination and their passability fields.
5. Read `static_a` and `static_b` for the source and destination cells.
6. Convert tile identifier `0x2710` to zero. This value is treated as a sentinel rather than an ordinary SOTP index.
7. Reject the step when any relevant low-nibble flags contain the requested direction bit.

A reduced static-only model is:

```c
u8 static_step_is_open(
    u8 direction,
    u16 source_a,
    u16 source_b,
    u16 destination_a,
    u16 destination_b,
    const u8 *collision_flags
)
{
    static const u8 direction_mask[4] = {
        0x01, 0x02, 0x04, 0x08
    };
    u8 mask;

    if (source_a == 0x2710) source_a = 0;
    if (source_b == 0x2710) source_b = 0;
    if (destination_a == 0x2710) destination_a = 0;
    if (destination_b == 0x2710) destination_b = 0;

    mask = direction_mask[direction & 3];

    if (collision_flags[source_a] & mask) return 0;
    if (collision_flags[source_b] & mask) return 0;
    if (collision_flags[destination_a] & mask) return 0;
    if (collision_flags[destination_b] & mask) return 0;

    return 1;
}
```

This is deliberately a reduced model. The original function has mode-dependent branches and dynamic-object checks that must remain in a faithful reimplementation.

An alternate path in the same function treats a destination as statically blocked when the OR of its two low-nibble values equals `0x0F`. `map_get_collision_level` at `0x5CF5E0` uses the same full-mask test after checking dynamic objects.

## Values used by the version-741 asset

The local 20,423-byte `SOTP.DAT` has only four complete byte values:

| Byte | Count | Interpretation |
|---:|---:|---|
| `0x00` | 4,265 | No static collision bits, no high render flag |
| `0x0F` | 15,782 | Blocked in all four cardinal directions |
| `0x80` | 322 | No collision bits, high render flag set |
| `0x8F` | 54 | Fully blocked and high render flag set |

The low-nibble distribution is therefore 15,836 entries with `0x0F` and 4,587 with `0x00`. The client supports independent directional bits, but this particular asset only uses fully blocked or fully open low nibbles.

The high nibble is `0x80` for 376 entries and zero for the rest. It is passed into static-object construction and is not tested by the collision routines. Its exact rendering meaning remains unknown.

## Authoring SOTP.DAT

An authoring tool can write one byte per static tile identifier, excluding identifier zero. Combine the low collision mask and high rendering flags:

```c
u8 make_sotp_entry(u8 collision, u8 render)
{
    return (u8)((collision & 0x0f) | (render & 0xf0));
}
```

For compatibility with the observed client data, use `0x00` for open tiles and `0x0F` for solid tiles until partial directional walls have been tested in game. Preserve `0x80` from a source tile with matching foreground or occlusion behavior until that flag is understood.

## Important functions and data

| Name | Address | Role |
|---|---:|---|
| `map_direction_delta` | `0x5BE580` | Convert a direction to a coordinate delta |
| `map_step_coordinate` | `0x5BE600` | Apply one direction step |
| `map_sotp_get_render_flags` | `0x5CF360` | Read the high SOTP nibble |
| `map_load_sotp_render_flags` | `0x5CF3B0` | Build the one-based high-nibble table |
| `map_sotp_get_collision_flags` | `0x5CF4A0` | Read the low SOTP nibble |
| `map_load_sotp_collision_flags` | `0x5CF4F0` | Build the one-based low-nibble table |
| `map_get_collision_level` | `0x5CF5E0` | Combine dynamic and fully blocked static collision |
| `map_can_move_direction` | `0x5EFFE0` | Validate a complete one-step movement attempt |
| Direction mask table | `0x6D395C` | Cardinal and combined wall masks |
