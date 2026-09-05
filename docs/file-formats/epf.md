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
            s16le top           // +0x00, also called bound_0
            s16le left          // +0x02, also called bound_1
            s16le bottom        // +0x04, also called bound_2, exclusive
            s16le right         // +0x06, also called bound_3, exclusive
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

The frame reader sign-extends all four bounds. They are placement coordinates, not unsigned dimensions. The primary pixmap pitch is `right - left`, and the cropped height is `bottom - top`. Negative coordinates and empty rectangles occur in the installed character art. The header dimensions do not bound those placement coordinates: local `MM00101.epf` reports 27 by 54 while frame 1 reaches right 40 and bottom 76.

## Character position companions

The human part loader looks for a same-stem `.tbl` in the same character archive. This is a binary position array, distinct from the text tables described elsewhere in the book. It has no header or count in this reader:

```text
record position {       // selected at file offset frame_index * 4
    u16le anchor_x
    u16le anchor_y
}
```

The index is the final EPF frame index, including the selected view group. The loader reads X into the pixmap's horizontal anchor and Y into its vertical anchor. It subtracts these anchors from the signed bounds before horizontal mirroring and composition. When the table is missing, the human category supplies `(28, 70)` or `(55, 70)` as documented in [Player rendering](../rendering/players.md#part-categories).

This path writes only two bytes into each 32-bit runtime anchor field. It does not sign-extend a negative 16-bit value or validate a companion-record count. Fresh pixmaps start with zero anchors, but the short writes do not establish a general signed-offset format for reused descriptors. Preserve the stored words, check table lengths in an external reader, and do not claim negative companion anchors work like signed EPF bounds. The inspected split M/W character archives contain no such tables, so this installation exercises the category defaults for its human parts.

The general EPF reader also probes a same-stem position table for `Efct` and `Mefc` resources. Those effect pixmaps start with zero anchors rather than the human category defaults. A raw EPF header does not carry this anchor.

## Character legend badges

The character-legend list uses `legends.epf` from `setoa.dat`. Both of its dialog layouts name that asset as `LegendImage`, and `LegendListPane` loads its first eight frames. The legend record's first byte chooses the frame during `ui_legend_list_draw_item`.

The general EPF loader recognizes this filename and assigns legacy palette number `3`. It combines that number with the standard UI palette family, so the renderer resolves selector `0x05000003` through `gui03.pal` in `setoa.dat`. This is distinct from profile EPFs, whose decoder explicitly uses `legend.pal`. Indexed pixel zero is transparent for the legend badge blit.

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

The ordinary indexed drawing path reads the primary payload as row-major, one-byte palette indexes with pitch `right - left`. It advances one byte per pixel and one pitch per row; normal human-part drawing skips index zero. The EPF effect conversion uses the same primary bytes. This path needs no decompression or row-run decoder.

The loader checks the frame index but does not prove that these offsets remain inside the archive entry. Validate the primary rectangle's byte count against the pixel blob in an external reader. The secondary range is still not fully classified, so a complete compatible writer must preserve it rather than assuming it is empty or disposable.

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
