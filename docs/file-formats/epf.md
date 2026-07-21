# EPF images

EPF stores multiple indexed image frames. The client maps a small header, a pixel blob, and a 16-byte record for each frame.

```text
file Epf {
    record header {
        u16le frame_count        // +0x00
        u16le width              // +0x02, overall metadata width
        u16le height             // +0x04, overall metadata height
        bytes unknown_06[2]      // +0x06
        u32le table_displacement // +0x08, from pixel_data at +0x0C
    }                            // 0x0C bytes
    bytes pixel_data[header.table_displacement]
    repeat header.frame_count {
        record frame {
            u16le bound_0       // +0x00
            u16le bound_1       // +0x02
            u16le bound_2       // +0x04
            u16le bound_3       // +0x06
            u32le data_offset_a // +0x08
            u32le data_offset_b // +0x0C
        }                        // 0x10 bytes
    }
    if bytes_remaining == 0x10 {
        record terminal_boundary {
            bytes unknown_00[8]
            u32le next_data_offset_a // used to bound the final second range
            bytes unknown_0c[4]
        }                         // 0x10 bytes
    }
}
```

Pixel data starts at file offset `0x0C`. The frame table starts at:

```text
0x0C + header.table_displacement
```

`file_read_image_metadata` returns the header's frame count, width, and height. `file_load_image_frame` uses the selected record to build the pixmap passed to `render_blit_pixmap`.

The loader also reads `data_offset_a` from the next 16-byte table position when it calculates the selected frame's second byte range. Of 35,324 local EPF entries, 9,992 store a terminal frame-shaped record for this final boundary. The other 25,332 end after the declared frame records. A final-frame load on the shorter form can therefore read beyond the archive entry even when the drawing path does not use that range. Preserve the source variant when rebuilding a container.

The lighting compositor also uses the ordinary EPF reader. In Darkness map mode, a server-supplied human light selector `N` loads frame zero from `mask1%02d.epf`, then treats its indexed pixels as a light mask centered on that human. See [Map lighting](../rendering/lighting.md).

## Reader shape

```text
read_epf_frame(file, index):
    header = read_header()
    require 0 <= index < header.frame_count
    pixel_base = file + 0x0C
    table = pixel_base + header.table_displacement
    frame = table[index]
    next = table[index + 1]

    primary = pixel_base + frame.data_offset_a
    secondary = pixel_base + frame.data_offset_b
    second_size = next.data_offset_a - frame.data_offset_b
    return image_view(frame.bounds, primary, secondary, second_size)
```

The loader checks the frame index but does not prove that these offsets remain inside the archive entry. The meaning of both payload ranges and the full pixel stream encoding are not yet proven. A container writer could reproduce an existing file while preserving those streams, but creating new image payloads is not documented as safe yet.

## Portrait-sized EPF

The portrait upload path accepts one narrow EPF profile:

```text
file_size == 0xB1C
header.table_displacement == 0xAF0
bound_2 - bound_0 == 56   // vertical span
bound_3 - bound_1 == 48   // horizontal span
```

The client uploads the complete EPF file without converting it. The portrait decoder copies the `0xAF0`-byte pixel stream and uses the first bounds to build a pixmap 48 pixels wide and 56 pixels high. The remaining layout still follows the EPF container rules above.

For local display, the portrait decoder assigns palette selector 0. The renderer resolves those indexed pixels through `legend.pal`. JPEG portraits take a separate direct-pixel path and do not use this palette.

This does not make every 48 by 56 EPF a valid portrait. The exact size and displacement checks must also pass. See [Portraits and profiles](../systems/portraits-and-profiles.md) for filename priority and packet limits.

The photo album Save action does not call an EPF writer. It always writes JPEG. The client can upload an EPF created elsewhere, but no dormant album branch converts its stored 16-bit pixels back into palette indexes.

## Generated writer shape

```text
write_epf(source):
    preserve source.unknown_header
    write_u16_le(frame_count)
    write_preserved_header_fields()
    reserve_table_displacement()
    write_existing_or_verified_pixel_streams()
    write_frame_records_with_rebased_offsets()
    write_preserved_terminal_boundary_if_present()
    fill_table_displacement()
```

This generated inverse is useful for rebuilding a container around known payloads. It is not yet an encoder from raw pixels.

For a basic primary-plane PNG exporter, use the frame bounds as width and height, read palette indexes from `data_offset_a`, and apply the selected external palette. The second offset is not enough to prove alpha or blending by itself. See [Exporting images](image-export.md).
