# MAP files

A map file is a row-major array of six-byte cells. It has no header. The caller must already know the width and height.

```text
struct MapCell {
    u16le ground_tile        // floor diamond
    u16le left_static_tile   // one isometric foreground side
    u16le right_static_tile  // the other isometric foreground side
}                            // size 6 bytes
```

The file size must be:

```text
width * height * 6
```

`file_format_map_path` builds names in the form `maps\lod<map_id>.map`. `file_read_map_cells` reads the entire cell array in one operation. `file_write_map_cells` writes the same array back, so MAP is the first format in this section with a client-confirmed two-way path.

## Decode

```text
decode_map(bytes, width, height):
    require bytes.length == width * height * 6

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

There is no room for dimensions, names, checksums, or compression in this file. Those values must come from the game state or another source.

Ground IDs select records from the [raw map tile banks](map-tile-banks.md). The two static IDs select HPF art, [SOTP collision and render flags](sotp.md), and optional [static tile animation](tile-animation-tables.md).
