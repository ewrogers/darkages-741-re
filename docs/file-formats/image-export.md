# Exporting images

Most art starts as palette indexes or 16-bit pixels. A PNG exporter should separate three jobs: decode the container, choose the palette or 16-bit pixel mode, then decide how transparency should be represented.

## Palette-indexed pixels

```text
indexed_to_rgba(indexes, palette, color_key):
    output = []

    for index in indexes:
        rgb = palette[index]
        alpha = 0 if color_key and index == 0 else 255
        output.push(rgb.red, rgb.green, rgb.blue, alpha)

    return output
```

Use the matching TBL lookup to select the PAL file. Sprite paths commonly use index 0 as a color key. Ground and background paths may draw it as opaque.

An HPF static image first needs HPF decoding, then its eight-byte private header is skipped. Its image width is 28 pixels. A raw map tile is 56 by 27 with transparent padding outside the diamond.

```text
export_static_hpf(hpf, palette):
    decoded = decode_hpf(hpf)
    indexes = decoded[8 :]
    height = indexes.length / 28
    rgba = indexed_to_rgba(indexes, palette, color_key = true)
    write_png(28, height, rgba)
```

For EPF, use the selected frame bounds for width and height and read the primary indexed plane from `data_offset_a`. Do not infer the second plane from its offset alone. SPF mode fields decide whether the embedded 0x400-byte palette area or another pixel path applies.

## RGB555 and RGB565

Some render-ready images already contain 16-bit pixels.

```text
expand_5(value) = (value << 3) | (value >> 2)
expand_6(value) = (value << 2) | (value >> 4)

rgb565(pixel):
    red   = expand_5((pixel >> 11) & 31)
    green = expand_6((pixel >> 5) & 63)
    blue  = expand_5(pixel & 31)

rgb555(pixel):
    red   = expand_5((pixel >> 10) & 31)
    green = expand_5((pixel >> 5) & 31)
    blue  = expand_5(pixel & 31)
```

The active display mode tells the client which layout to use. EFA's main render plane follows that mode after its frame payload is inflated.

## Blending and alpha

Color-key copy maps cleanly to PNG alpha 0 or 255. A verified per-pixel alpha plane can be copied into PNG alpha.

Average, screen, additive, and destination-dependent blends do not describe a source alpha channel. To export what the game shows, first render onto a chosen background with the same blend, then save the composited result as an opaque PNG. Do not invent semi-transparent alpha from a blend mode alone.

See [PAL files](pal.md), [HPF static images](hpf.md), [raw map tile banks](map-tile-banks.md), [EPF](epf.md), [SPF](spf.md), [EFA](efa.md), and [blending](../rendering/blending.md).
