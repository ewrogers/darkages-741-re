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
