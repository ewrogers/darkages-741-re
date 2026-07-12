# Map lighting and masks

The client uses an 8-bit light mask over the rendered 16-bit world viewport. Server opcode `0x20`, the metadata section named `Light`, the `SMapSize` low-nibble map mode, optional `.hea` resources, and per-human EPF masks all participate.

The final effect is a color blend, not a second set of darkened map tiles.

## Server update

Local opcode `0x20` is registered as `SChangeHour`. `net_handle_s_change_hour` at `0x5F2160` stores its `u8` value at world offset `+0x25C`, then calls `lighting_update_for_server_hour` at `0x5EF360`.

The metadata time slot is:

```c
slot = server_hour * 2;
if (slot > 24)
    slot = 24;
```

This matches the local `Light` profile ranges `0..24`. The byte is therefore time or hour input, while its visible result is a change in light level and tint.

`SChangeWeather` opcode `0x1F` has a registered packet class and one `u8` field, but `net_dispatch_game_server_message` at `0x5ED990` has no `0x1F` handler branch. No local `SChangeDay` opcode `0x1E` factory or game-dispatch branch was recovered. These related-engine names should not be treated as active local lighting paths.

## Light metadata

`lighting_request_metadata` at `0x4AEA80` requests a metadata section with the literal name `Light`. `lighting_lookup_map_profile` at `0x4AEAD0` resolves the current map ID and time slot to:

| Value | Internal record offset | Use |
|---|---:|---|
| Start slot | `+0x00` | Inclusive start of the time range |
| End slot | `+0x04` | Inclusive end of the time range |
| Light value | `+0x08` | Mask value, normally `0..32` |
| Red | `+0x09` | Tint red byte |
| Green | `+0x0A` | Tint green byte |
| Blue | `+0x0B` | Tint blue byte |
| Flags | `+0x0C` | Bit `0` disables HEA use when set |

The extracted version-741 `metafile/Light` assigns the `Default` profile to these 22 maps:

```text
500, 501, 502, 503, 504, 505
662, 663, 664, 665, 666, 667
2001, 2002, 2003, 2006, 2007, 2008, 2009, 2011, 2012, 2013
```

Its profile is:

| Slot range | Light | RGB tint |
|---|---:|---|
| `0..1` | `18` | `6, 11, 60` |
| `2..3` | `20` | `27, 1, 59` |
| `4..5` | `23` | `100, 10, 100` |
| `6..7` | `26` | `170, 36, 50` |
| `8..17` | `32` | Tint is visually unused |
| `18..19` | `26` | `170, 36, 50` |
| `20..21` | `23` | `100, 10, 100` |
| `22..24` | `20` | `27, 1, 59` |

Light value `32` preserves the rendered viewport. Lower values blend progressively toward the tint color.

## Map mode

`map_handle_s_map_size` at `0x5F1BF0` stores `map_flags & 0x0F` at world offset `+0x264`. `lighting_apply_map_mode` at `0x5F26C0` compares the complete low-nibble value with `0`, `1`, `2`, and `3`.

| Mode | Recovered lighting behavior |
|---:|---|
| `0` | No forced lighting. A `Light` metadata entry can still enable time-based lighting. |
| `1` | Runs a separate special-map path at `0x5C82C0`; no forced darkness is established. |
| `2` | No forced lighting in this routine. |
| `3` | Enables the viewport mask and local object lights, sets light to `0`, and uses packed tint `0`, which is black. |

Mode `3` is the strong local gate for lantern-style light sources. The metadata map list is the separate gate for ordinary time-of-day lighting.

## Runtime state

These are offsets in the world pane object:

| Offset | Type | Meaning |
|---:|---|---|
| `+0x1E4` | pointer | 8-bit viewport light-mask surface |
| `+0x1E8` | `u8` | Viewport lighting active |
| `+0x1E9` | `u8` | Local object-light masks enabled |
| `+0x200` | `u8` | Current global light value |
| `+0x202` | `u16` | Tint color packed for the current display format |
| `+0x204` | pointer | HEA view |
| `+0x208` | `u8` | Current map HEA loaded successfully |
| `+0x25C` | `u8` | Last `SChangeHour` byte |
| `+0x264` | `u8` | `SMapSize` low-nibble map mode |
| `+0x26C` | `u32` | Current map ID |

## Building the light mask

`render_world_frame_with_lighting` at `0x5CE280` draws the normal world first. When lighting is active and the light value is below `32`, it calls `lighting_build_viewport_mask` at `0x5C8760`.

The mask is built in this order:

1. If `%06d.hea` loaded, decode its spatial RLE mask for the visible rectangle.
2. Otherwise fill the visible rectangle with the global light value.
3. If local lights are enabled, find visible objects with attached masks.
4. Translate and clip each object mask to the viewport.
5. Merge it with `destination = max(destination, source)`.

The maximum operation means a local lamp can make pixels lighter, but a weaker mask cannot darken a pixel that is already brighter.

## HEA role

HEA is the static spatial darkness mask, not the lantern image itself. `lighting_update_for_server_hour` attempts to load `%06d.hea` when the metadata record allows HEA and the global light value is below `32`. Missing HEA data falls back to a uniform mask, so the map can still become dark.

`file_hea_prepare_region_rows` at `0x487380` uses the HEA header and lookup tables to resolve payload pointers for the visible rectangle. `lighting_decode_hea_mask_region` at `0x5C8540` interprets each little-endian `u16` token as:

```text
bits 15..8: run length
bits  7..0: light value
```

The decoder caps each HEA light value to the current global light value before writing it to the viewport mask.

```c
void decode_hea_row(u8 *dst, int width, const u16 *tokens, u8 global_light)
{
    int remaining;

    remaining = width;
    while (remaining > 0) {
        u16 token;
        int run;
        u8 light;

        token = *tokens++;
        run = token >> 8;
        light = (u8)token;

        if (light > global_light)
            light = global_light;
        if (run > remaining)
            run = remaining;

        memset(dst, light, run);
        dst += run;
        remaining -= run;
    }
}
```

The real function also skips leading runs for a clipped X origin and advances through multiple rows using the pointers prepared from HEA.

## Lantern and object masks

The normal `SDrawHumanObjects` appearance variant contains a `u8` value that the handler treats as a light-mask number. It defaults to `1`. On map mode `3`, `net_handle_s_draw_human_objects` passes that value and the object ID to `lighting_attach_mask_to_object` at `0x5CCA80`.

Values greater than zero construct `lighting_object_mask_ctor` at `0x5B8C90`, which loads:

```text
mask1%02d.epf
```

Examples are `mask101.epf`, `mask102.epf`, and so on. The decoded EPF supplies an 8-bit light mask centered on the object. Moving, changing, or removing the object invalidates the affected mask rectangle through `lighting_invalidate_object_region` at `0x5CD000` or `lighting_invalidate_removed_object_region` at `0x5CD200`.

## Viewport blend

`lighting_apply_viewport_tint` at `0x5CE350` blends the completed mask over the 16-bit world surface. It selects `render_blend_rgb565_mask` at `0x603A90` or `render_blend_rgb555_mask` at `0x603F00` according to the active display mode.

For each color channel, the operation is:

```c
output = (source * light + tint * (32 - light)) >> 5;
```

Therefore:

- `light == 32` keeps the original world pixel.
- `light == 0` replaces it with the tint color.
- intermediate values produce the night-time color mask.

The packed implementations preserve channel boundaries with these masks:

| Format | Red and blue mask | Green mask |
|---|---:|---:|
| RGB565 | `0xF81F` | `0x07E0` |
| RGB555 | `0x7C1F` | `0x03E0` |

## Important functions

| Function | Address | Role |
|---|---:|---|
| `net_handle_s_change_hour` | `0x5F2160` | Store opcode `0x20` time input |
| `lighting_update_for_server_hour` | `0x5EF360` | Resolve metadata and update lighting state |
| `lighting_lookup_map_profile` | `0x4AEAD0` | Select the current map and time record |
| `lighting_apply_map_mode` | `0x5F26C0` | Apply the `SMapSize` low-nibble mode |
| `lighting_build_viewport_mask` | `0x5C8760` | Combine HEA or flat base with local lights |
| `lighting_decode_hea_mask_region` | `0x5C8540` | Decode HEA run tokens |
| `lighting_object_mask_ctor` | `0x5B8C90` | Load `mask1%02d.epf` |
| `lighting_merge_mask_max` | `0x6036B0` | Merge a local light mask |
| `lighting_apply_viewport_tint` | `0x5CE350` | Blend the mask over the world viewport |
