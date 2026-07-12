# Map loading and rendering

The client treats a map as a headerless row-major array of six-byte cells. The server supplies the map identifier, dimensions, flags, checksum, and cell data. The completed grid is cached locally and then expanded into ground and static render layers.

## Grid and cache format

The runtime grid begins with this recovered layout:

| Offset | Type | Meaning |
|---:|---|---|
| `+0x00` | `u16` | Map identifier |
| `+0x02` | `u16` | Width |
| `+0x04` | `u16` | Height |
| `+0x06` | `u16` | Cached CRC-16 |
| `+0x08` | `u8` | Dirty flag |
| `+0x0C` | pointer | Row-major cell data |

Each cell is:

```c
struct map_cell {
    u16 ground;
    u16 static_a;
    u16 static_b;
};
```

The address of a cell is:

```c
cell = grid->cells + (y * grid->width + x) * 6;
```

`map_grid_initialize` at `0x5B9030` allocates `width * height * 6` bytes. `map_grid_set_tile` at `0x5B90F0` stores the three values and marks the grid dirty.

Local files are named `maps/lod%d.map`. `map_grid_load_file` at `0x5B9450` and `map_grid_save_file` at `0x5B9680` read and write exactly `width * height * 6` bytes. There is no file header, embedded size, compression, or scrambling. The stored words are host-order little-endian.

The dimensions must already be known from the server before a cache file can be interpreted. For example, a 15,000-byte file contains 2,500 cells and is 50 by 50 only when the server says so.

## Network loading sequence

`map_handle_s_map_size` at `0x5F1BF0` is reached from `net_dispatch_game_server_message` at `0x5ED990` for [SMapSize `0x15`](../network/server/021-0x15-map-size.md). It receives:

| Packet field | Type | Use |
|---|---|---|
| Map identifier | `u16be` | Selects the map and local `lod%d.map` filename |
| Width | `u8` | Grid width |
| Height | `u8` | Grid height |
| Flags | `u8` | Map state flags, semantics incomplete |
| Unknown byte | `u8` | Preserved in map state |
| Checksum | `u24be` | Expected map checksum |
| Name | length-prefixed string | Map display name |

The load order is:

1. Compare the current map identifier, dimensions, and cached CRC with the server state.
2. Initialize a blank grid when they do not match.
3. Try `maps/lod%d.map` for the requested identifier.
4. Recalculate the CRC over the local grid.
5. Attach the grid immediately when the checksum matches.
6. Otherwise send [CMapCRC `0x05`](../network/client/005-0x05-map-crc.md) with the local dimensions and checksum.
7. Apply server map data as it arrives.
8. Calculate the final CRC, save the cache, and attach the completed grid.

The request body emitted at `0x5F1BF0` is:

```text
u8    opcode = 0x05
u16be reserved = 0
u16be reserved = 0
u8    width
u8    height
u24be local_checksum
```

Two server update forms are present:

- `map_handle_s_map_part` at `0x5F2840` reads a rectangular update. Four leading `u8` values define its start and extent, followed by three `u16be` tile identifiers for every cell.
- `map_handle_s_map_row` at `0x5F2A60` reads a `u16be` row index, then three `u16be` values for every column. The final row triggers CRC calculation, cache writing, and `map_finish_loading` at `0x5F2DE0`.

The packet words are big-endian on the wire. The grid setter stores them as native little-endian words, which is why the loose cache can be copied without conversion.

The older [SMap `0x06`](../network/server/006-0x06-map.md) class contains four leading bytes and a remaining data view. Its dispatcher path reaches the row loader. The exact semantic names of all four class fields remain under investigation.

## Map CRC

`net_calculate_map_crc16` at `0x5B9180` traverses the grid in row-major order. For each of the three `u16` values it feeds the low byte and then the high byte into the project's CRC-16 update. It stores the result at grid offset `+0x06` and clears the dirty flag at `+0x08`.

This byte order matches the local cache representation. See [Packet encryption and CRC](../client/packet-crypto-and-crc.md) for the complete CRC algorithm.

## Building render layers

`map_world_attach_grid` at `0x5C7970` stores the grid pointer at world pane offset `+0x190`, clears old map state, calls `map_build_tile_layers` at `0x5CD3C0`, and can rebuild static world objects through `map_build_static_world_objects` at `0x5CD730`.

`map_build_tile_layers` walks every coordinate and reads all three cell words:

```c
for (y = 0; y < map->height; y++) {
    for (x = 0; x < map->width; x++) {
        ground = map_grid_get_ground_tile(map, x, y);
        static_a = map_grid_get_static_a(map, x, y);
        static_b = map_grid_get_static_b(map, x, y);

        map_tile_layer_add(ground_layer, ground, x, y, 0);
        map_tile_layer_add(static_layer, static_a, x, y, 0);
        map_tile_layer_add(static_layer, static_b, x, y, 1);
    }
}
```

The real function first checks that each referenced resource exists. `map_tile_layer_add` at `0x5FA540` groups placements by tile identifier and stores the coordinate and orientation tuple used later by the renderer.

## Tile resources

`map_tile_bank_manager_ctor` at `0x4C7560` opens two raw archive entries, `tilea.bmp` and `tileas.bmp`. Despite their names, they are not Windows BMP files. Each tile occupies `0x5E8` bytes, arranged as 27 rows of 56 palette indices.

`map_decode_palette_tile` at `0x4C7390` uses static row-start and row-width tables to select the visible isometric diamond from those rows. Each source byte indexes a 256-color palette and becomes a 16-bit display pixel.

Static map art also references numbered resources:

- `map_load_hpf_resource` at `0x5FD700` loads `stc%05d.hpf` or `sts%05d.hpf` and applies the HPF adaptive-tree decoder.
- `map_load_hea_resource` at `0x5C7870` loads `%06d.hea` spatial lookup data.

HEA supplies the optional static spatial darkness mask used by the map-lighting compositor. Time profiles, map-mode gating, lantern masks, and the final color blend are documented in [Map lighting and masks](lighting.md).

The binary layouts and encoder pseudocode are documented in [Graphics and animation files](../file-formats/graphics-and-animation-files.md).

## SOTP rendering metadata

`map_build_static_world_objects` looks up the high nibble of the static tile's `SOTP.DAT` byte with `map_sotp_get_render_flags` at `0x5CF360`. It passes that value to `map_world_static_object_ctor` at `0x5E42F0`, which stores it at object offset `+0xB9`.

The current asset only uses high-nibble values `0x00` and `0x80`. The code proves that this nibble belongs to static-object construction and rendering, but its exact effect, such as occlusion or foreground ordering, is not yet confirmed. It is separate from collision.

## Important functions

| Function | Address | Role |
|---|---:|---|
| `map_grid_initialize` | `0x5B9030` | Allocate and clear the grid |
| `map_grid_set_tile` | `0x5B90F0` | Store one six-byte cell |
| `net_calculate_map_crc16` | `0x5B9180` | Calculate and cache the map checksum |
| `map_grid_load_file` | `0x5B9450` | Load a local `lod%d.map` cache |
| `map_grid_save_file` | `0x5B9680` | Write a local map cache |
| `map_world_attach_grid` | `0x5C7970` | Attach a complete grid to the world pane |
| `map_build_tile_layers` | `0x5CD3C0` | Expand map cells into render-layer placements |
| `map_build_static_world_objects` | `0x5CD730` | Construct static world objects |
| `map_handle_s_map_size` | `0x5F1BF0` | Validate server map state and choose cache or download |
| `map_handle_s_map_part` | `0x5F2840` | Apply a rectangular server update |
| `map_handle_s_map_row` | `0x5F2A60` | Apply one server map row |
| `map_finish_loading` | `0x5F2DE0` | Publish the completed map to the world pane |
| `map_tile_layer_add` | `0x5FA540` | Add a tile placement to a render layer |
| `lighting_apply_map_mode` | `0x5F26C0` | Apply the `SMapSize` low-nibble lighting mode |
| `lighting_build_viewport_mask` | `0x5C8760` | Build HEA, flat, and object light masks |
