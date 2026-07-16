# SPF images

SPF is another multi-frame indexed image container. `file_spf_view_initialize` maps the file, and `file_spf_get_frame` returns one frame view without copying the whole resource.

```text
struct SpfPrefix {
    u8 unknown[8]     // +0x00
    u8 pixel_mode     // +0x08
    u8 palette_mode   // +0x09
    u8 unknown_0a[2]  // +0x0A
}

struct SpfFrameRecord {
    u16le bound_0          // +0x00
    u16le bound_1          // +0x02
    u16le bound_2          // +0x04
    u16le bound_3          // +0x06
    u16le value_08         // +0x08, optional use
    u16le value_0a         // +0x0A, optional use
    u32le flags            // +0x0C
    u32le data_offset      // +0x10
    u32le pitch            // +0x14
    u32le unknown_18       // +0x18
    u32le alternate_offset // +0x1C, used by one pixel mode
}                          // size 0x20
```

If both mode bytes are zero, a 0x400-byte palette follows the 12-byte prefix. Next come:

```text
u32le frame_count
SpfFrameRecord frames[frame_count]
u32le pixel_blob_size
u8 pixel_blob[pixel_blob_size]
```

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

PNG conversion depends on the two mode bytes. The all-zero mode carries a 0x400-byte embedded palette area; other modes must follow their confirmed pixel path. See [Exporting images](image-export.md).
