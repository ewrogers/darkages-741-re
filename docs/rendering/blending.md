# Blending

Transparency and alpha blending are done in software on 16-bit pixels.

## Transparent pixels

In the common sprite paths, a source pixel value of zero is transparent. The blitter skips it and leaves the destination pixel unchanged.

```text
if source_pixel != 0:
    destination_pixel = source_pixel
```

This is simple color-key transparency. It is used for sharp sprite edges where partial transparency is not needed.

## Blend modes

`render_blit_pixmap`, `render_blit_image`, and `render_blit_canvas` accept a numeric mode. The mode selects a copy loop, a fixed blend, a table-driven alpha path, or a color effect.

The confirmed building blocks are:

- direct copy for normal opaque sprite pixels
- `render_average_pixels` for a fixed half-like blend
- `render_blend_pixel` for a variable software blend
- special paths for images with a second pixel or alpha plane
- color-shift paths used by selected object states

The client has many numeric modes, but their game-facing names are not stored in RTTI. The book therefore keeps the raw mode number when a friendly name is not proven.

## Static occluder blend

SOTP render flag `0x80` selects mode `0x6D` for walls, trees, and other static art. This mode uses a screen-style component operation:

```text
output = source + destination * (max - source) / max
```

The static art is blended over the pixels already drawn for the player. See [Walls and occlusion](walls-and-occlusion.md).

## Lookup tables

`render_build_blend_tables` creates two 256 by 256 tables. One handles five-bit color components and the other handles six-bit components. `render_blend_pixel` uses them to combine RGB555 or RGB565 pixels without repeating the full component math for every draw.

The tables are created with the video system and released by `render_free_blend_tables` during shutdown.

The optimized blitter dispatch has a second table family. `render_initialize_blit_dispatch` selects RGB565 or RGB555, installs the format-specific software routines, and calls `render_build_16bit_blend_tables`. Those tables split packed pixels into component and carry values so the inner loops can process several 16-bit pixels at once. Video shutdown clears the dispatch and frees all six buffers.

Its indexed-image entry points make the transparency rule explicit:

- `render_blit_indexed_opaque` maps every source index through the palette.
- `render_blit_indexed_zero_transparent` maps index 0 to packed pixel value 0.
- `render_blit_indexed_transparent` skips index 0 and preserves the destination.

All three accept horizontal and vertical flip flags. The ordinary loops handle all four combinations directly; optimized paths encode the flags in a shared byte before drawing.

### Alpha sources

The 16-bit dispatch supports three alpha sources:

- one uniform `0..32` weight for the whole draw
- a second pixel plane containing per-pixel weights
- row-based run-length alpha streams

An RLE alpha token stores its repeat count in the high byte and its alpha value in the low byte. One image representation locates each row by an offset relative to the packed alpha blob; another stores absolute row pointers. Variants can also apply a source color key, a global opacity, or two alpha streams.

Separate entry points implement luminance-ramp recoloring, screen-style per-component composition, and saturating additive blending. The dispatcher selects paired RGB565 or RGB555 scalar loops, or an MMX implementation when the optimized path is active.

## Per-canvas blit state

A canvas carries more than a pixel buffer. `render_canvas_blit_pixels_software` reads several optional inputs while copying a source rectangle:

- horizontal and vertical flip flags
- a 16-bit color key
- a signed offset for each scanline, with clamped or wrapped lookup
- an optional pointer to an alpha mask for each row
- four byte-sized alpha-mask parameters

The scanline-offset table can be phased or rotated without changing the source image. This supplies row-by-row displacement to the software blitter. The alpha-screen pane uses the row-mask path: it builds one mask buffer per row, installs those row pointers on its canvas, and lets the normal software blit apply the gradient.

For a DirectDraw-backed canvas, `render_canvas_set_color_key` also calls the surface `SetColorKey` method. Heap-backed canvases retain the same value for the software path. The color key therefore remains part of Canvas state even though only one backing type forwards it to DirectDraw.

## Why DirectDraw is not doing the blend

The sprite loops read source pixels, test transparency, combine color components, and write the destination canvas directly. DirectDraw receives the completed canvas later. This means normal sprites and alpha effects behave the same across the DirectDraw and window DC presentation paths.
