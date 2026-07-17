# EPF images

EPF stores multiple indexed image frames. The client maps a small header, a pixel blob, and a 16-byte record for each frame.

```text
struct EpfHeader {
    u16le frame_count       // +0x00
    u8    unknown[6]        // +0x02
    u32le table_displacement // +0x08, measured from pixel data at +0x0C
}

struct EpfFrameRecord {
    u16le bound_0           // +0x00
    u16le bound_1           // +0x02
    u16le bound_2           // +0x04
    u16le bound_3           // +0x06
    u32le data_offset_a     // +0x08
    u32le data_offset_b     // +0x0C
}                           // size 0x10
```

Pixel data starts at file offset `0x0C`. The frame table starts at:

```text
0x0C + header.table_displacement
```

`file_read_image_metadata` reads the header. `file_load_image_frame` uses the selected record to build the pixmap passed to `render_blit_pixmap`.

The lighting compositor also uses the ordinary EPF reader. In Darkness map mode, a server-supplied human light selector `N` loads frame zero from `mask1%02d.epf`, then treats its indexed pixels as a light mask centered on that human. See [Map lighting](../rendering/lighting.md).

## Reader shape

```text
read_epf(file):
    header = read_header()
    pixel_base = file + 0x0C
    table = pixel_base + header.table_displacement

    for each frame record:
        validate both data offsets against the pixel blob
        keep the four bounds and the two payload positions
```

The meaning of both payload offsets and the full pixel stream encoding are not yet proven. A container writer could reproduce an existing file while preserving those streams, but creating new image payloads is not documented as safe yet.

## Portrait-sized EPF

The portrait upload path accepts one narrow EPF profile:

```text
file_size == 0xB1C
header.table_displacement == 0xAF0
first_bounds.width == 56
first_bounds.height == 48
```

The client uploads the complete EPF file without converting it. The portrait decoder copies the `0xAF0`-byte pixel stream and uses the first bounds to build a 56 by 48 pixmap. The remaining layout still follows the EPF container rules above.

For local display, the portrait decoder assigns palette selector 0. The renderer resolves those indexed pixels through `legend.pal`. JPEG portraits take a separate direct-pixel path and do not use this palette.

This does not make every 56 by 48 EPF a valid portrait. The exact size and displacement checks must also pass. See [Portraits and profiles](../systems/portraits-and-profiles.md) for filename priority and packet limits.

## Generated writer shape

```text
write_epf(source):
    preserve source.unknown_header
    write_u16_le(frame_count)
    write_preserved_header_fields()
    reserve_table_displacement()
    write_existing_or_verified_pixel_streams()
    write_frame_records_with_rebased_offsets()
    fill_table_displacement()
```

This generated inverse is useful for rebuilding a container around known payloads. It is not yet an encoder from raw pixels.

For a basic primary-plane PNG exporter, use the frame bounds as width and height, read palette indexes from `data_offset_a`, and apply the selected external palette. The second offset is not enough to prove alpha or blending by itself. See [Exporting images](image-export.md).
