# EFA effects

EFA stores compressed effect frames. Each frame has a 64-byte descriptor and its own zlib-compressed payload.

```text
file Efa {
    record header {
        u32le unknown_00
        u32le frame_count       // +0x04
        u32le frame_interval_ms // +0x08, zero permits a caller interval
        bytes unknown_0c[0x34]
    }                           // 0x40 bytes
    repeat header.frame_count {
        record frame {
            u32le unknown_00
            u32le data_offset     // +0x04, from compressed_payloads
            u32le compressed_size // +0x08
            u32le decoded_size    // +0x0C
            u32le plane_kind      // +0x10
            u32le pixel_offset    // +0x14, inside decoded data
            u32le pixel_pitch     // +0x18
            u32le pixel_mode      // +0x1C
            u32le second_offset   // +0x20, optional second plane
            u32le second_pitch    // +0x24
            u16le value_28        // +0x28
            u16le value_2a        // +0x2A
            repeat 4 {
                u16le bound       // begins at +0x2C
            }
            repeat 4 {
                u16le crop        // begins at +0x34
            }
            bytes unknown_3c[4]
        }                         // 0x40 bytes
    }
    bytes compressed_payloads[to end_of_file] // one zlib stream per frame
}
```

The frame records start at file offset `0x40`. Compressed payloads start after all records:

```text
payload_base = 0x40 + frame_count * 0x40
```

`file_decode_efa_frame` finds the selected payload, inflates it with zlib, and creates an image over the described pixel planes.

`file_open_efa` returns both `frame_count` and `frame_interval_ms` from the header. Ordinary world effects prefer a nonzero EFA interval over the fallback timer supplied by [`SEffectLayer`](../network/server/041-0x29-effect-layer.md). A zero interval leaves that packet value in use. The timer advances frames, so this is not the effect's total lifetime.

The ordinary-effect start path contains a dead calculation that raises a local copy of the resource interval to 50 ms. The scheduled timer still reads the original stored interval, so the client does not actually enforce that apparent minimum.

When the effective interval is positive, the client selects the current `Effect.tbl` entry from elapsed time divided by the interval. If the main-thread timer runs late, the effect may therefore skip frames to catch up instead of extending its total playback time.

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
