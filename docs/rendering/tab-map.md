# Tab wireframe map

The Tab map is a transparent software-rendered overlay built from small 2:1 diamonds. It does not draw the normal map art at a smaller size. Instead, it converts each map cell into one collision level, projects that cell around the current view center, and paints a filled wall or a dithered object marker.

The result can be reproduced exactly from four inputs:

- the map dimensions and two static tile IDs at each cell
- the live world objects and their minimap collision levels
- the current center tile and integer scale
- the matching `legend.pal` colors from `Legend.dat`

## Frame flow

The overlay is a normal pane with its own 16-bit software canvas. It covers the live `WorldPane` rectangle, so changing the UI layout also changes the map canvas width, height, and midpoint.

```text
static collision flags + live objects
                 |
                 v
      one level byte per tile
                 |
                 v
       isometric projection
                 |
                 v
 diamond fill + shared wall edges
                 |
                 v
 transparent copy over the world pane
```

`map_refresh_collision_cache` updates the cell data. `render_world_minimap` projects and paints it. `render_canvas_fill_diamond_palette` supplies the exact diamond scan conversion.

## Cell data

The pane allocates a fixed cache for 256 by 256 cells. Map width and height are each clamped to the range 0 through 256.

```c
struct MinimapCell {
    u8 collision_level;
    u8 refresh_requested;
    u8 redraw_pending;
};

MinimapCell cells[256 * 256];
u8 visible[256 * 256];
u8 level_to_palette[256];
```

The index is `y * 256 + x`. A cell refresh recomputes its level and sets `redraw_pending`.

### Choosing one level

`map_get_collision_level` first scans every live `WorldObject` in the cell and retains the greatest collision-level byte. The highest numeric level wins when several objects share a tile.

If no object supplies a positive level, the client reads both static tile IDs. Tile ID 10000 is treated as empty. It ORs the two low-nibble collision masks from [SOTP.DAT](../file-formats/sotp.md). The cell becomes level 1 only when the result is exactly `0x0F`, meaning that all four movement-direction bits are set. Otherwise it remains level 0.

This produces the following priority from greatest to least:

| Level | Source |
|---:|---|
| 180 | Local player |
| 150 | Monster `CreatureType` 1 |
| 140 | Monster `CreatureType` 2 |
| 130 | Monster `CreatureType` 3 |
| 120 | Other monster `CreatureType` values |
| 100 | Visible remote human |
| 1 | Fully blocked static cell |
| 0 | Empty or not represented |

A remote human normally receives level 100. A human appearance whose body sprite is zero resets the level to zero, matching the hidden all-zero appearance described by [User Appearance](../network/server/005-0x05-user-appearance.md).

## Projection

All projection coordinates below are local to the minimap canvas. Let:

```text
W, H            canvas width and height
center_x/y      current center map cell
x, y            cell being rendered
s               signed integer scale
dx = x - center_x
dy = y - center_y
```

The cell center is:

```text
pixel_x = trunc(W / 2) + 2 * s * (dx - dy)
pixel_y = trunc(H / 2) +     s * (dx + dy)
```

The two cell basis steps are therefore:

| Map step | Screen step |
|---|---|
| `x + 1` | `(+2s, +s)` |
| `y + 1` | `(-2s, +s)` |

This makes neighboring cells meet as 2:1 isometric diamonds. Two additional projection-offset fields exist, but the matching client initializes them to zero and has no writer for them.

Before drawing, the client rejects a cell when its conservative diamond bounds do not overlap the clip rectangle:

```text
pixel_x + 2s < clip_left   or pixel_x - 2s > clip_right
pixel_y +  s < clip_top    or pixel_y -  s > clip_bottom
```

The drawing primitives then perform the final pixel clipping. Their right and bottom clip limits are exclusive.

## Scale and centering

Opening the overlay with Tab centers it on the local player's tile. While it is active, the world-view update path keeps the minimap center synchronized.

The starting scale is class dependent:

| Character class | Starting scale | Zoom keys enabled |
|---|---:|---|
| Class value 2, Rogue | 3 | Yes |
| Every other class | 5 | No |

One internal key code, `0x93`, increments the scale. Code `0x94` decrements it when the scale is greater than 1. Both events are consumed even when zoom is disabled. Their user-facing key labels have not been verified.

There is no upper clamp. Projection uses the complete integer `s`, but the diamond function receives an 8-bit radius. At ordinary scales these agree. Above 255, radius wrapping makes the native result pathological and must be preserved for a strict behavioral clone.

The [Map Size](../network/server/021-0x15-map-size.md) `NoMap` bit prevents Tab from opening the overlay.

## Exact diamond fill

The wall radius is `r = u8(s)`. Every non-wall cell uses `r = u8(s - 1)`. At the normal scales this gives:

| Scale | Wall radius | Marker radius |
|---:|---:|---:|
| 1 | 1 | 0 |
| 3 | 3 | 2 |
| 5 | 5 | 4 |

For center `(cx, cy)` and radius `r`, generate inclusive horizontal spans as follows:

```c
for (i = 0; i <= r; i++) {
    y = cy - r + i;
    half_width = 2 * i;
    span(cx - half_width, cx + half_width, y);
}

for (i = 1; i <= r; i++) {
    y = cy + i;
    half_width = 2 * (r - i) + 1;
    span(cx - half_width, cx + half_width, y);
}
```

The diamond is `2r + 1` rows high. Its north tip is one pixel wide, its center is `4r + 1` pixels wide, and its south tip is three pixels wide. This one-pixel bottom asymmetry is part of the client rasterizer.

Clip each inclusive span to the canvas. In solid mode, write every remaining pixel. In dither mode, write only pixels satisfying:

```text
(x & 1) == ((trunc(y / 2)) & 1)
```

Visible canvas coordinates are nonnegative, so the pattern is:

| `y mod 4` | Painted x coordinates |
|---:|---|
| 0 or 1 | Even x |
| 2 or 3 | Odd x |

The test uses canvas coordinates, not coordinates relative to the diamond. All markers therefore share one continuous screen-space pattern.

## Colors and paint modes

The client loads palette slot 0 from `legend.pal` inside [Legend.dat](../file-formats/dat-archives.md). The following are the exact 8-bit source RGB values and the 16-bit words produced by the client's normal packing rules.

| Level or use | Palette | RGB | RGB565 | RGB555 | Paint |
|---|---:|---|---:|---:|---|
| Empty or unmapped | `0x00` | `#000000` | `0x0000` | `0x0000` | Dithered transparent erase |
| Static wall | `0x16` | `#979797` | `0x94B2` | `0x4A52` | Solid, radius `s` |
| Remote human, 100 | `0x58` | `#7FA7F3` | `0x7D3E` | `0x3E9E` | Dithered, radius `s - 1` |
| Monster, 120 | `0x28` | `#CB0017` | `0xC802` | `0x6402` | Dithered, radius `s - 1` |
| Monster, 130 | `0xFF` | `#1B7F7F` | `0x1BEF` | `0x0DEF` | Dithered, radius `s - 1` |
| Monster, 140 | `0x80` | `#00FF00` | `0x07E0` | `0x03E0` | Dithered, radius `s - 1` |
| Monster, 150 | `0x28` | `#CB0017` | `0xC802` | `0x6402` | Dithered, radius `s - 1` |
| Local player, 180 | `0x45` | `#FFE73B` | `0xFF27` | `0x7F87` | Dithered, radius `s - 1` |
| Wall boundary | `0xFF` | `#1B7F7F` | `0x1BEF` | `0x0DEF` | Direct one-pixel writes |

The packing formulas are:

```c
rgb565 = ((r >> 3) << 11) | ((g >> 2) << 5) | (b >> 3);
rgb555 = ((r >> 3) << 10) | ((g >> 3) << 5) | (b >> 3);
```

Exact comparison should use the 16-bit word for the client's active display mode. A modern RGBA renderer may use the source RGB column, but that is a presentation conversion rather than the native canvas value.

The level table has 256 entries and starts filled with palette index 0. Only the rows above are assigned. An unexpected nonzero level therefore paints transparent zero on its dither pixels.

## Wall boundary pixels

Teal boundaries are not a general polygon stroke. The renderer compares only whether a cell is level 1 and emits one of two north-facing shared half-edges.

For `k` from 0 through `2s`, inclusive:

```c
// Northwest edge
x = cx - k;
y = cy - s + trunc(k / 2);

// Northeast edge
x = cx + k;
y = cy - s + trunc(k / 2);
```

Each point is written with palette index `0xFF`. Because two consecutive `k` values share the same y coordinate, most scanlines contain two horizontally adjacent stroke pixels.

After processing a cell:

```c
if (x > 0 && (level[y][x] == 1) != (level[y][x - 1] == 1))
    draw_northwest_edge();

if (y > 0 && (level[y][x] == 1) != (level[y - 1][x] == 1))
    draw_northeast_edge();
```

Cells are visited with y as the outer loop and x as the inner loop. A later right or lower neighbor supplies the matching shared edge. The client never compares against cells outside the map, so it does not invent an outline around the map perimeter.

Edges are evaluated on every visible render. Cell fills are incremental and run only when `redraw_pending` is set.

## Transparency and composition

The minimap canvas is copied over the world with color value 0 treated as transparent. Nonzero pixels overwrite the world pixel. There is no alpha blend in this path.

The apparent transparency of an object marker comes entirely from the spatial dither rule. Half of the marker positions contain color and the other half retain transparent zero, allowing the world pane to show through.

A forced refresh clears the overlay canvas to zero, refreshes every map cell, and marks every cell for repaint. During normal play, the canvas persists and only dirty fills are changed. This retained canvas matters when cloning frame-by-frame behavior.

## Restricted visibility in Darkness

Map mode 3 enables a second 256 by 256 byte mask. Other map modes disable it. The mask is the union of keyed, axis-aligned tile rectangles, not a circular per-pixel light calculation.

For a retained region centered at `(x, y)` with supplied half-extent `E`, the exact half-open rectangle is:

```text
[x - E, x + E + 1) by [y - E, y + E + 1)
```

The known object-light caller derives `E` as `2 * light_bitmap_value + 1`. Regions are keyed by the owning entity ID so they can be updated or removed independently.

In restricted mode:

1. The renderer clears the dirty part of the visibility mask.
2. It unions every active region into that dirty rectangle.
3. An unmasked cell is erased with a palette-0 dithered diamond of radius `s - 1`.
4. Level 180 bypasses the mask, so the local yellow player marker remains visible.
5. A wall edge against the left or upper neighbor is emitted only when that neighbor is also marked visible.

A hidden cell keeps its redraw-pending state. It can therefore paint its current color when a later mask update reveals it.

## Reference implementation order

To reproduce a fresh frame rather than the retained update behavior:

```c
clear_canvas_to_zero();
refresh_every_collision_cell();
rebuild_visibility_mask_if_enabled();

for (y = 0; y < map_height; y++) {
    for (x = 0; x < map_width; x++) {
        project_cell_center(x, y, &cx, &cy);
        if (!conservative_bounds_overlap_clip(cx, cy, scale))
            continue;

        level = cells[y * 256 + x].collision_level;

        if (restricted && visible[y * 256 + x] == 0 && level != 180) {
            fill_diamond(cx, cy, scale - 1, palette[0], DITHER);
            continue;
        }

        if (level == 1)
            fill_diamond(cx, cy, scale, palette[0x16], SOLID);
        else
            fill_diamond(cx, cy, scale - 1,
                         palette[level_to_palette[level]], DITHER);

        if (x > 0 && wall(level) != wall(cells[y * 256 + x - 1].collision_level))
            draw_northwest_edge(cx, cy, scale, palette[0xFF]);

        if (y > 0 && wall(level) != wall(cells[(y - 1) * 256 + x].collision_level))
            draw_northeast_edge(cx, cy, scale, palette[0xFF]);
    }
}

copy_nonzero_pixels_over_world();
```

When restricted visibility is enabled, add the neighbor-mask conditions described above to both edge tests. For a frame-by-frame clone, preserve the software canvas and the three cell bytes, repaint only pending fills, leave hidden cells pending, and continue to evaluate visible boundary edges every frame.

Function addresses and evidence are kept in the [function reference](../appendix/functions.md) and the deterministic rendering export.
