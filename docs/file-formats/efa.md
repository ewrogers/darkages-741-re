# EFA effects

EFA stores compressed effect frames. Each frame has a 64-byte descriptor and its own zlib-compressed payload.

```text
file Efa {
    record header {
        u32le unknown_00
        u32le frame_count       // +0x04
        u32le frame_interval_ms // +0x08, zero permits a caller interval
        u32le blend_selector    // +0x0C, interpreted by EffectImageSession
        u32le flags             // +0x10, bit 0 enables direction flips
        bytes unknown_14[0x2C]
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
            u16le anchor_x        // +0x28
            u16le anchor_y        // +0x2A
            u16le bound_left      // +0x2C
            u16le bound_top       // +0x2E
            u16le bound_right     // +0x30
            u16le bound_bottom    // +0x32
            u16le crop_left       // +0x34
            u16le crop_top        // +0x36
            u16le crop_right      // +0x38
            u16le crop_bottom     // +0x3A
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

## Frame position and direction

EFA stores its two rectangles in X-first order, unlike EPF. The decoder zero-extends these 16-bit fields and converts them to the renderer's internal Y-first rectangle order. The effect image session uses the crop rectangle and the two anchors for placement. Do not substitute the human body's fixed anchor or use `bound_left` as the crop's origin.

For an ordinary unflipped effect, the cropped image starts at:

```c
draw_x = object_origin.x + crop_left - anchor_x;
draw_y = object_origin.y + crop_top - anchor_y;
```

Width is `crop_right - crop_left`, and height is `crop_bottom - crop_top`. Right and bottom are exclusive. The decoded image is rebased for storage; the world effect restores its crop-relative placement when it subtracts the runtime anchor adjustment.

Header flag bit 0 enables direction-dependent flipping. If clear, no direction flip is requested. If set, the effect uses the direction captured at creation:

| Direction | Flip X | Flip Y |
| --- | --- | --- |
| left, 0 | no | yes |
| down, 1 | no | no |
| right, 2 | yes | no |
| up, 3 | yes | yes |

Before placement, replace `anchor_x` with `crop_right - (anchor_x - crop_left)` when X is flipped, and replace `anchor_y` with `crop_bottom - (anchor_y - crop_top)` when Y is flipped. Then use the placement formula and flip the corresponding pixel traversal. These are rectangle-boundary coordinates; do not add a second pixel correction to the pivot.

The effect session converts header `blend_selector` to the software blit mode: 1 becomes `0x6E`, 2 becomes `0x6D`, 3 with frame pixel mode 4 becomes 9, 3 with pixel mode 7 becomes `0x6F`, and 4 with pixel mode 5 becomes `0x70`. Preserve other combinations as unresolved rather than treating every EFA as ordinary alpha. See [Blending](../rendering/blending.md) and the [player rendering evidence](../appendix/player-rendering.md#effect-geometry).

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

The returned RTTI-backed `Image` stores a rectangle and three plane descriptors. Each descriptor contains a data pointer, row stride, byte count, and ownership flag. EFA decoding normally attaches borrowed pointers into the inflated frame storage, while generated effect images can copy plane zero into owned memory. Replacing or destroying a plane frees it only when that ownership flag is set.

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
