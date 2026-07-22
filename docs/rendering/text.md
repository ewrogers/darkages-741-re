# Text and fonts

The client draws text with its own bitmap font renderer. It does not ask Windows to draw a TrueType or system font. This keeps the UI visually consistent, but it also ties language support to the selected bitmap font and the Windows ANSI code page.

## Drawing a string

The active path is:

```text
ANSI byte string
      |
      v
single byte or DBCS pair
      |
      v
16-bit font lookup key
      |
      v
LFT glyph metrics and 1-bit bitmap
      |
      v
software canvas mask blit
```

`render_canvas_draw_text` copies the requested bytes into a small local buffer. It calls `IsDBCSLeadByte` for each leading byte. A single-byte character becomes a key from `0x0000` through `0x00FF`. A double-byte character becomes `(lead << 8) | trail`.

`render_font_build_glyph_mask` looks up that key in the active LFT entry. It expands the stored glyph into a one-bit mask and returns its advance width and drawing bounds. `render_canvas_blit_mask` then writes the current foreground color into the 16-bit software canvas. Its drawing mode can also preserve, replace, or blend the background pixels.

The matching LFT face has a nominal 12 by 12 cell. Individual records keep their own bounds and advance, so narrow Latin glyphs do not consume the full cell while double-byte glyphs can use the wider space.

Color is separate from the font. Normal controls set a canvas color before drawing. Formatted text can change the color between runs through the palette codes described in [Text color markup](../systems/text-color-markup.md).

`render_canvas_set_text_position` records the x and y origin used by the next text draw. The primary and secondary colors can be supplied as packed 16-bit values, RGB triplets, or client palette indexes. The setters return the old packed value where a caller needs to restore drawing state.

The text layout path also preserves fixed-width spacing behavior. `text_rotate_leading_spaces_to_end` moves leading spaces to the end of a bounded span, while `text_count_trailing_and_total_spaces` reports the trailing and overall space counts used by `render_canvas_draw_text`. These helpers operate on byte spans, so their limits follow the same ANSI and DBCS rules as glyph lookup.

Two UI helpers use a simpler six-pixel cell model. `text_truncate_with_ellipsis_dbcs` shortens a mutable label to its available cells and appends three dots without cutting a detected DBCS pair. `render_canvas_draw_wrapped_fixed_text` splits a bounded byte span into six-pixel columns and advances twelve pixels per line. It restores the caller's original text position after drawing.

The final canvas reaches DirectDraw or the window DC only after all text, UI, sprites, and effects have already been composed. The client imports no `TextOut`, `DrawText`, or `CreateFont` function for this path.

## Active font selection

The language mode selects one archive entry:

| Language mode | Font entry | Message label | Code-page setting |
| ---: | --- | --- | ---: |
| `0` | `lod.lft` | `msgkor.h` | 949 |
| `1` | `da.lft` | `msgeng.h` | system ANSI code page |
| `2` | `yami.lft` | `msgjpn.h` | 932 |
| `3` | `taiwan.lft` | `msgtai.h` | system ANSI code page |

The distribution selector maps the normal USA build to language mode 1, Japan to mode 2, Taiwan to mode 3, and the original/default path to mode 0. Singapore also uses the English mode.

The stored code-page value does not change the process locale. Its getter has no callers in this executable, while the live renderer calls `IsDBCSLeadByte` without an explicit code-page argument. Actual byte splitting therefore follows the Windows active ANSI code page. Selecting another font mode by itself is not enough to make its text work correctly.

This exact executable always selects the USA distribution, so `da.lft` is the active font. The matching `national.dat` contains `da.lft` and `lod.lft`; those two entries are byte-for-byte identical. It does not contain `yami.lft` or `taiwan.lft`. Japanese and Taiwan support therefore remains compiled code in this installation, not a usable local configuration.

## Character sets

The game text path is byte-oriented, not Unicode-oriented.

- English and other single-byte ANSI text can use one glyph key per byte.
- Korean mode explicitly records Windows code page 949 and enables the IME native conversion bit during input setup.
- Japanese mode explicitly records Windows code page 932.
- Taiwan mode expects the system ANSI environment to supply its double-byte rules. The code does not explicitly select code page 950, so calling this confirmed Big5 support would be too strong.
- UTF-8 and UTF-16 are not accepted by the game text renderer. There is no shaping or combining-character engine.

The LFT index has a slot for nearly every 16-bit byte value. That does not mean every language is supported. The same two bytes identify different characters under different code pages, so the selected LFT and the process ANSI locale must agree.

`MultiByteToWideChar` and `WideCharToMultiByte` remain in the import table, but neither has a code reference in this executable. They do not form a hidden Unicode font path.

Text input follows the same model. The client uses the ANSI IME functions, including `ImmGetCompositionStringA` and `ImmGetCandidateListA`, then posts composition, candidate, and committed-text events to the focused control. Composition and committed-text event buffers retain at most 127 bytes.

## Older fixed fonts

The executable also retains loaders for `eng%02d.fnt` and `han%02d.fnt`. The matching `Legend.dat` contains two English files and four Korean files, and `Darkages.cfg` still stores `EngFont` and `HanFont` indexes.

These loaders have no callers and are not part of the `FontImageLib` vtable in this target. The active renderer uses LFT instead. They are best treated as a dormant earlier font system, not as a second live font choice. Their formats are described in [FNT fixed fonts](../file-formats/fnt.md).

Static addresses and confidence notes are kept in the [function reference](../appendix/functions.md).
