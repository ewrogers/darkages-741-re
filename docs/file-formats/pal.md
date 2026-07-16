# PAL color palettes

A PAL file is exactly 768 bytes. It contains 256 colors with no header and no compression.

All 847 PAL entries found in the inspected client data have this exact size.

```c
struct PalColor {
    u8 red;
    u8 green;
    u8 blue;
};

struct PalFile {
    PalColor colors[256];
};
```

The bytes are full 0 through 255 color channels. They are not VGA 6-bit colors.

`file_palette_load_rgb` copies the 768 bytes. `render_palette_pack_16bit` then converts them to RGB565 or RGB555 for the active display mode.

In the common indexed sprite path, index 0 is the transparent key. The renderer keeps packed color 0 for that index. If any other palette index contains black and also packs to zero, it changes that packed value to 1 so it remains visible.

## Use a palette

```text
color = palette[pixel_index]

if sprite_uses_color_key and pixel_index == 0:
    alpha = 0
else:
    alpha = 255
```

The PAL file itself has no alpha channel. Background art may use index 0 as an ordinary opaque color, so transparency is a property of the drawing path, not the file.

Palette lookup tables such as `itempal.tbl`, `stcpal.tbl`, and `mptpal.tbl` choose which PAL number belongs to an asset range. See [TBL lookup files](table-files.md) and [Exporting images](image-export.md).

## Evidence

- `file_palette_load_rgb` at `0x00548650`
- `render_palette_pack_16bit` at `0x00593B00`
