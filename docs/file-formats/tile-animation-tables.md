# Tile animation tables

Ground and static map animation is driven by two plain text files:

| File | Animated art |
| --- | --- |
| `gndani.tbl` | Ground tiles from `tilea.bmp` or `tileas.bmp` |
| `stcani.tbl` | Static `stc` or `sts` HPF images |

Each non-empty line contains a cycle of decimal tile IDs followed by a delay. The delay is counted in 100 ms ticks.

```text
frame_id frame_id ... delay_ticks
```

For example, this synthetic line changes every 200 ms:

```text
100 101 102 2
```

The IDs rotate as a mapping:

```text
100 -> 101
101 -> 102
102 -> 100
```

This means a map may use any ID in the group and keep its starting phase.

## Runtime flow

`map_tile_animation_manager_ctor` loads both files. `map_tile_animation_timer` runs every 100 ms and advances each group after its own delay expires.

Ground animation is applied before `map_load_tile_pixels` chooses a ground bank. Static animation is applied before `render_get_static_tile_image` chooses an `stc` or `sts` resource. The same animation group therefore works with base and snowy art.

When a group advances, the client clears the affected image cache so the next frame is decoded with the new mapped ID. The server does not send each animation frame.

## Write a table

Write one group per line using decimal integers separated by spaces. A useful line needs at least two frame IDs and one positive delay.

```text
require frame_count >= 2
require delay_ticks > 0
write frame IDs
write delay_ticks last
```

Keep every tile ID valid for the matching art bank. The client does not add missing animation art.
