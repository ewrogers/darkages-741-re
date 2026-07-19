# SPF images

SPF stores one or more rectangular images without compressing their pixel bytes. A frame can use palette indexes or direct 16-bit pixels. `file_spf_view_initialize` maps the file, and `file_spf_get_frame` returns a zero-copy view of one frame.

```text
struct SpfPrefix {
    u8 unknown[8]     // +0x00
    u8 pixel_mode     // +0x08
    u8 palette_mode   // +0x09
    u8 unknown_0a[2]  // +0x0A
}

struct SpfFrameRecord {
    u16le left             // +0x00
    u16le top              // +0x02
    u16le right            // +0x04
    u16le bottom           // +0x06
    u16le optional_08      // +0x08, used when flags bit 0 is set
    u16le optional_0a      // +0x0A, used when flags bit 0 is set
    u32le flags            // +0x0C
    u32le data_offset      // +0x10
    u32le pitch            // +0x14, source bytes per row
    u32le unknown_18       // +0x18
    u32le alternate_offset // +0x1C, used by one pixel mode
}                          // size 0x20
```

If both mode bytes are zero, a 0x400-byte palette block follows the 12-byte prefix:

```text
u16le rgb565_palette[256]
u16le rgb555_palette[256]
```

The client selects the first table for RGB565 output and the second for RGB555 output. Next come:

```text
u32le frame_count
SpfFrameRecord frames[frame_count]
u32le pixel_blob_size
u8 pixel_blob[pixel_blob_size]
```

The normal frame pointer is `pixel_blob + data_offset`. Bounds define the visible rectangle:

```text
width  = right - left
height = bottom - top
```

## Indexed pixels

For `pixel_mode = 0` and `palette_mode = 0`, each source byte is one palette index. Rows are stored in normal row-major order and advance by `pitch` bytes. Index zero is transparent. Every nonzero byte selects one packed 16-bit color from the active embedded palette.

The NPC illustration files reached through the local `NPCIllust` metadata all use this mode. Each has one frame, no frame flags, and `pitch == width`. See [NPC dialog illustrations](../systems/npc-dialog-illustrations.md).

## Direct 16-bit pixels

For `pixel_mode = 2`, the frame data contains direct 16-bit pixels and does not use the embedded palette block. When the active pixel format is the alternate format, the reader adds `alternate_offset` to the normal frame pointer. The installed NPC illustrations do not use this path.

No SPF path shown here decompresses or unscrambles the pixel blob.

## Generated writer shape

```text
write_spf(source):
    write_prefix(source.mode_fields)
    if pixel_mode == 0 and palette_mode == 0:
        write_exactly_0x400_bytes(source.palette)

    write_u32_le(frame_count)
    reserve(frame_count * 0x20)
    write_u32_le(pixel_blob_size)
    write(pixel_blob)
    fill_frame_records_with_blob_offsets()
```

This is a generated inverse of the reader. Unknown prefix and record fields must be preserved from a compatible template. It has not yet passed a decode, encode, decode round trip, so it is not a confirmed production writer.

PNG conversion depends on the two mode bytes. For the all-zero indexed mode, expand each nonzero index through the RGB565 or RGB555 table and preserve index zero as alpha zero. Other modes must follow their confirmed pixel path. See [Exporting images](image-export.md).
