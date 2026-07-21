# LFT bitmap fonts

LFT supplies the glyphs used by the active text renderer. Each entry contains one fixed lookup table followed by packed one-bit glyph rows. The renderer indexes it with a single ANSI byte or a two-byte DBCS key.

The local `da.lft` and `lod.lft` entries are stored inside `national.dat`. Each is 3,476,705 bytes and the two payloads are identical.

## Layout

All multi-byte fields are little-endian.

```text
file Lft {
    u16le nominal_width        // 12 in the matching entries
    u16le nominal_height       // 12 in the matching entries
    repeat 65535 {
        record glyph {
            u8 advance
            u8 left
            u8 top
            u8 right
            u8 bottom
            u16le packed_size
            u32le bitmap_offset // relative to bitmap_data
        }                       // 11 bytes, keys 0x0000 through 0xFFFE
    }
    bytes bitmap_data[to end_of_file] // begins at 0x0AFFF9
}
```

The client seeks directly to `0x0AFFF9` to establish the bitmap-data base. This matches `4 + 65535 * 11` exactly.

## Glyph rows

The visible glyph width is `right - left`. The number of stored rows is `bottom - top`. Source rows are one bit per pixel, most-significant bit first, and each source row is padded to a four-byte boundary:

```text
row_stride = ((right - left + 31) / 32) * 4
```

The local `packed_size` values match `row_stride * (bottom - top)`. The active loader calculates that size from the bounds rather than trusting the stored field.

When drawing, the loader copies the useful bits into a temporary mask. Advances of eight pixels or less use one output byte per row; wider advances use two. The glyph is placed at its stored left and top offsets, then the canvas advances by `advance` pixels.

Backspace, tab, line feed, and carriage return have a forced advance of zero. Space normally uses its stored advance. If an LFT omits the space bitmap, the fallback is half of `nominal_width`.

## Measure and render text

An LFT entry contains everything needed to measure and render a line of text. A standalone tool does not need the client renderer. The simplest output is an 8-bit alpha bitmap where zero is transparent and 255 is a font pixel. That mask can then be colored or composited into RGB or RGBA output.

### Build glyph keys

First encode the source text with the character set expected by the chosen LFT. Walk those bytes exactly as the client does:

```c
u16 next_glyph_key(u8 *text, int length, int *position)
{
    u8 first = text[(*position)++];

    if (is_lead_byte_for_selected_code_page(first)) {
        if (*position >= length)
            return INVALID_GLYPH;

        return (first << 8) | text[(*position)++];
    }

    return first;
}
```

Use explicit lead-byte rules for the intended code page. Relying on the host machine's current locale can make the same byte string split differently. Reject key `0xFFFF`, which has no record.

### Measure a line

The layout width is the sum of the glyph advances. Ink bounds are slightly different because each bitmap has its own left, top, right, and bottom values.

```c
int glyph_advance(LftFile *font, u16 key)
{
    if (key == 0x08 || key == 0x09 || key == 0x0A || key == 0x0D)
        return 0;

    LftGlyphRecord *glyph = &font->glyphs[key];

    if (key == 0x20 && glyph->bitmap_offset == 0)
        return font->header.nominal_width / 2;

    return glyph->advance;
}

TextMetrics measure_line(u16 *keys, int count, LftFile *font)
{
    TextMetrics result = empty_metrics();
    int pen_x = 0;

    for (int i = 0; i < count; i++) {
        u16 key = keys[i];
        LftGlyphRecord *glyph = &font->glyphs[key];
        int advance = glyph_advance(font, key);

        if (glyph->bitmap_offset != 0) {
            include_x(&result.ink, pen_x + glyph->left,
                                      pen_x + glyph->right);
            include_y(&result.ink, glyph->top, glyph->bottom);
        }

        pen_x += advance;
    }

    result.advance_width = pen_x;
    return result;
}
```

Use `advance_width` when positioning the next string or control. Use `ink` when producing a tightly cropped image. For a client-like line surface, allocate at least `advance_width` by `nominal_height` and retain the original cell offsets.

The low-level client draw helper does not lay out paragraphs. Line feed and carriage return have zero advance. A separate text-layout layer must split lines, move down by `nominal_height`, and decide how tabs should behave.

### Draw one glyph

Rendering can read the packed LFT rows directly. There is no need to reproduce the client's temporary one-byte or two-byte row mask.

```c
void draw_glyph(AlphaBitmap *target, int pen_x, int line_top,
                LftFile *font, u16 key)
{
    LftGlyphRecord *glyph = &font->glyphs[key];

    if (glyph->bitmap_offset == 0)
        return;

    int width = glyph->right - glyph->left;
    int height = glyph->bottom - glyph->top;
    int stride = ((width + 31) / 32) * 4;
    u8 *source = font->bitmap_data + glyph->bitmap_offset;

    for (int y = 0; y < height; y++) {
        for (int x = 0; x < width; x++) {
            u8 bit = 0x80 >> (x & 7);

            if ((source[y * stride + x / 8] & bit) != 0) {
                set_alpha(target,
                          pen_x + glyph->left + x,
                          line_top + glyph->top + y,
                          255);
            }
        }
    }
}
```

After drawing, advance `pen_x` by `glyph_advance(font, key)`, even when the record contains no visible bitmap. The client places a nominal cell from `cursor_y - nominal_height` through `cursor_y`; using `line_top` directly is the equivalent top-left-oriented form.

Before drawing, validate that `bitmap_offset + packed_size` stays within the bitmap region. The matching files have 65,535 valid records, no packed-size mismatches, and no bitmap ranges outside the entry.

## Encoding is outside the file

LFT does not name Unicode characters. Its array index is the raw one-byte or two-byte value assembled by the text renderer. Interpreting a key as English, Korean, Japanese, or Traditional Chinese depends on both the chosen LFT entry and the Windows ANSI code page.

There is no confirmed LFT writer in the client. A generated writer should preserve all 65,535 records, recalculate every bitmap offset, retain the four-byte row alignment, and round-trip every glyph mask before it is called compatible.
