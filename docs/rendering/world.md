# World rendering

`render_world_frame` draws the visible game world into the `WorldPane` canvas. It uses a ground cache, background images, and sorted world objects.

## Frame order

```text
ground tile cache
      |
map background images and tile markers
      |
ordinary world-object queues 0 through 31
      |
world light mask
      |
late layer-zero queue and local-player replay
      |
copy WorldPane into the UI tree
```

This order lets the map act as the floor while characters, items, and effects appear above it.

## Ground tiles

`render_ground_layer` finds the visible map cells and compares each ground tile with a cached copy. Only changed tiles are redrawn into the ground canvas.

`map_get_tile_pixels` asks the tile library for one decoded diamond. `render_ground_tile` then copies its scanlines into the cached ground canvas. The active storage reads the raw tile banks `tilea.bmp` and `tileas.bmp`. Their names are misleading because the files are not Windows BMP images.

The map cell itself stores three tile IDs. The first is the ground. The other two create left and right isometric static layers. See the [map format](../file-formats/map.md).

[`SStaticObjectState`](../network/server/050-0x32-static-object-state.md) can replace the live tile ID of either isometric static layer. It selects a row in a built-in 66-pair state table, swaps the `WorldObject_Static` image to the other tile ID, and leaves the original map-cell value unchanged. Doors use this path for their open and closed art.

The server can select the alternate ground and static art during map setup. See [Snow and weather](weather.md) and [raw map tile banks](../file-formats/map-tile-banks.md).

## Tile animation

Ground and static tile animation is local and table-driven. `gndani.tbl` rotates ground tile IDs, while `stcani.tbl` rotates static tile IDs. A shared 100 ms timer advances each group and clears the affected cache.

The live mappings use separate fixed-capacity owners. Static tiles start with 0x2000 remap entries and ground tiles with 0x5000; an absent remap falls back to the requested tile ID. Matching 0x2000 and 0x5000 integer flag vectors begin at zero and are marked as the palette tables load. Animation rotates the appropriate remap vector, so the source tables remain unchanged while subsequent tile lookup sees the next frame.

The server does not send every animation frame. See [tile animation tables](../file-formats/tile-animation-tables.md) for the text format.

## Background images

`render_map_background_images` draws map background or bottom-layer images before world objects. These images use the same pixmap blitter used by normal UI and sprite art.

`MapBtmLayer` supplies that optional bottom layer. When `SMapSize` selects a map, the client asks its resource manager for a six-digit `NNNNNN.mbl` entry using a fixed 0x1394-byte destination buffer. The active loader reads a placement count followed by records containing three decimal integers: a bottom-image ID, x, and y. It resolves each image as `btmNNNNN.pcx` from the SEO archive, caches repeated IDs in `MapBtmImageLib`, and expands each placement to a rectangle using the decoded image width and height.

The layer keeps visible and hidden placement lists. It recomputes the expanded isometric viewport only when the camera cell changes, moves overlapping records into the visible list, and sends that list to the common background-image renderer.

A separate loader understands loose `.\\maps\\lodN.mbl` text and `.\\bottom\\btmNNNNN.pcx` files, but it has no local caller in this build. The resource-manager and SEO-archive path is the one connected to map changes.

## Sprites and objects

`render_collect_world_objects` gathers objects that overlap the visible cells. It clips their screen bounds and places them into one of 32 draw queues.

`render_world_layer_queue` walks the queues from 0 through 31. Objects within one queue retain the visible-object collection order. `render_world_object` then calls the object's virtual draw method. RTTI confirms distinct object types for static map objects, humans, monsters, items, effects, and moving effects.

The confirmed constructor-assigned layers are:

| Layer | Object |
| ---: | --- |
| 4 | ground item |
| 7 | human, including the local player |
| 10 | monster |
| 13 | object-attached or moving effect |
| 16 | static map art |
| 24 | static effect |

Layer zero is retained in a separate queue instead of the ordinary layer-zero draw. After the light mask is built, `render_replay_layer_zero_and_self` draws that late queue and replays the recorded local-player entry. The local player has already participated in ordinary layer 7. In the normal non-blinded state, the replay selects living-object blend mode 3.

The useful draw paths include:

- `render_living_object` for humans and monsters
- `render_item_object` for ground items
- `render_static_object` for fixed world objects
- `render_effect_object` for effect frames

The object chooses a blend mode, but the common image blitter does the pixel work.

Human objects are themselves composites of body, head, hair, clothing, equipment, and accessories. See [Player rendering](players.md) for their 21 part categories and direction rules.

## Effects

`render_update_effect_frame` advances an effect through the sequence loaded from `Effect.tbl`. A nonzero EFA frame interval overrides the fallback interval in `SEffectLayer`; a zero resource interval leaves the packet value active. The sequence position comes from elapsed dispatcher time divided by that effective interval, so a delayed callback can skip frames instead of stretching the animation.

`render_effect_object` draws that frame with the effect's current blend mode. There is no separate hardware effect renderer. Normal and alpha-blended effects both pass through the software image blitter.

See [Effect.tbl](../file-formats/effect-table.md), [EFA effects](../file-formats/efa.md), and [`SEffectLayer`](../network/server/041-0x29-effect-layer.md#animation-timing) for the sequence, resource interval, fallback value, and loop rules.

## Walls and fixed art

Static tile IDs become fixed world objects. `SOTP.DAT` controls both their movement collision and special over-player blend. See [SOTP static tile flags](../file-formats/sotp.md) and [Walls and occlusion](walls-and-occlusion.md).

## UI connection

The pane tree is part of the render path. `render_screen_subtree` clips each visible pane, asks it to draw, then visits its children. `WorldPane` overrides the content hook to draw the game world. `ImagePane` overrides the same kind of hook to draw an image.

The common pane hook `ui_pane_draw_to_target` copies a pane canvas into its parent canvas. This is the main bridge between pane layout and pixel rendering.

See [UI composition and compact layout](ui-composition.md) for sibling order and for the GUI layout toggle that changes the actual world viewport.
