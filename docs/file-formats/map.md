# MAP files

A map file is a row-major array of six-byte cells. It has no header. The caller must already know the width and height.

```text
struct MapCell {
    u16le ground_tile        // floor diamond
    u16le left_static_tile   // one isometric foreground side
    u16le right_static_tile  // the other isometric foreground side
}                            // size 6 bytes
```

The meaningful file body is:

```text
width * height * 6
```

`file_format_map_path` builds names in the form `maps\lod<map_id>.map`. Both paths first ask Windows to create the `maps` directory if necessary.

`file_read_map_cells` reads the entire expected cell array into temporary storage. It copies that storage into the live grid only when all `width * height * 6` bytes were read. A short file is rejected without a partial copy. A longer file is accepted, but bytes after the expected array are ignored.

`file_write_map_cells` opens the path with `wb`, truncates any prior file, and writes the complete contiguous array once. The resulting file is exactly the meaningful size during a successful write. MAP therefore has a client-confirmed two-way path.

The embedded `fopen_s` path permits concurrent `rb` readers but makes a `wb` writer exclusive until `fclose`. No map-cache handle is retained afterward. See [Multiple client processes](../systems/map-loading.md#multiple-client-processes) for the resulting multibox race.

## Decode

```text
decode_map(bytes, width, height):
    require bytes.length >= width * height * 6

    for y in 0 .. height - 1:
        for x in 0 .. width - 1:
            cell.ground_tile       = read_u16_le()
            cell.left_static_tile  = read_u16_le()
            cell.right_static_tile = read_u16_le()
```

## Encode

```text
encode_map(cells, width, height):
    require cells.count == width * height

    for cell in row_major_order:
        write_u16_le(cell.ground_tile)
        write_u16_le(cell.left_static_tile)
        write_u16_le(cell.right_static_tile)
```

The meaningful body carries no dimensions, names, checksums, or compression. Those values must come from the game state or another source.

After the final-index [`SMapPart`](../network/server/060-0x3c-map-part.md), the client computes the CRC over the in-memory cells and writes this entire file. It does not stream individual rows to disk. The packet handler ignores the writer's result, and the writer treats opening the file as success without checking the returned write count. See [Map loading and cache](../systems/map-loading.md) for the full lifecycle.

Ground IDs select records from the [raw map tile banks](map-tile-banks.md). The two static IDs select HPF art, [SOTP collision and render flags](sotp.md), and optional [static tile animation](tile-animation-tables.md).
