# World rendering

`render_world_frame` draws the visible game world into the `WorldPane` canvas. It uses a ground cache, background images, and sorted world objects.

## Frame order

```text
ground tile cache
      |
map background images
      |
visible world objects
      |
WorldPane overlays
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

The server does not send every animation frame. See [tile animation tables](../file-formats/tile-animation-tables.md) for the text format.

## Background images

`render_map_background_images` draws map background or bottom-layer images before world objects. These images use the same pixmap blitter used by normal UI and sprite art.

## Sprites and objects

`render_collect_world_objects` gathers objects that overlap the visible cells. It clips their screen bounds and places them into one of 32 draw queues.

`render_world_layer_queue` walks those queues. `render_world_object` then calls the object's virtual draw method. RTTI confirms distinct object types for static map objects, humans, monsters, items, effects, and moving effects.

The useful draw paths include:

- `render_living_object` for humans and monsters
- `render_item_object` for ground items
- `render_static_object` for fixed world objects
- `render_effect_object` for effect frames

The object chooses a blend mode, but the common image blitter does the pixel work.

## Effects

`render_update_effect_frame` advances an effect through the sequence loaded from `Effect.tbl`. The effect image pool loads the matching EFA or EPF resource only when a frame is needed.

`render_effect_object` draws that frame with the effect's current blend mode. There is no separate hardware effect renderer. Normal and alpha-blended effects both pass through the software image blitter.

## Walls and fixed art

Static tile IDs become fixed world objects. `SOTP.DAT` controls both their movement collision and special over-player blend. See [SOTP static tile flags](../file-formats/sotp.md) and [Walls and occlusion](walls-and-occlusion.md).

## UI connection

The pane tree is part of the render path. `render_screen_subtree` clips each visible pane, asks it to draw, then visits its children. `WorldPane` overrides the content hook to draw the game world. `ImagePane` overrides the same kind of hook to draw an image.

The common pane hook `ui_pane_draw_to_target` copies a pane canvas into its parent canvas. This is the main bridge between pane layout and pixel rendering.
