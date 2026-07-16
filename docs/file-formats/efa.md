# EFA effects

EFA stores compressed effect frames. Each frame has a 64-byte descriptor and its own zlib-compressed payload.

```text
struct EfaHeader {
    u32le unknown_00
    u32le frame_count   // +0x04
    u8 unknown_08[0x38]
}                       // size 0x40

struct EfaFrameRecord {
    u32le unknown_00
    u32le data_offset       // +0x04, from payload area
    u32le compressed_size   // +0x08
    u32le decoded_size      // +0x0C
    u32le plane_kind        // +0x10
    u32le pixel_offset      // +0x14, inside decoded data
    u32le pixel_pitch       // +0x18
    u32le pixel_mode        // +0x1C
    u32le second_offset     // +0x20, optional second plane
    u32le second_pitch      // +0x24
    u16le value_28          // +0x28
    u16le value_2a          // +0x2A
    u16le bounds[4]         // +0x2C
    u16le crop[4]           // +0x34
    u8 unknown_3c[4]
}                           // size 0x40
```

The frame records start at file offset `0x40`. Compressed payloads start after all records:

```text
payload_base = 0x40 + frame_count * 0x40
```

`file_decode_efa_frame` finds the selected payload, inflates it with zlib, and creates an image over the described pixel planes.

## Decode

```text
decode_efa_frame(file, index):
    record = records[index]
    compressed = payload_base + record.data_offset
    decoded = zlib_inflate(compressed, record.compressed_size,
                           record.decoded_size)

    pixels = decoded + record.pixel_offset
    optional_second_plane = decoded + record.second_offset
    return image_view(record, pixels, optional_second_plane)
```

## Writer status

A generated writer can serialize the table, zlib-compress each decoded payload, and calculate offsets and sizes. It still needs the unknown header fields, plane kinds, and pixel modes to be classified before it can safely create new effects from raw images. Preserving those fields from an existing compatible frame is the current safe approach.

```text
write_efa(source):
    preserve unknown header and descriptor fields
    reserve 0x40 + frame_count * 0x40 bytes

    for each frame:
        payload = build_existing_plane_layout(frame)
        compressed = zlib_compress(payload)
        write compressed at the next payload offset
        fill record offset, compressed size, and decoded size
```

For PNG output, inflate the frame first and decode the main 16-bit plane as RGB555 or RGB565 according to the active pixel mode. Use an auxiliary plane as alpha only after its plane kind is verified. See [Exporting images](image-export.md).
