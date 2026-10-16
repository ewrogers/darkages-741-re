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

Another compact lookup family supports luminance recoloring. `render_initialize_luminance_tables` builds red, green, and blue contributions using coefficients 0.299, 0.587, and 0.114, then creates four 32-entry output ramps for RGB565 and four for RGB555. Video setup tells the shared mapper which source packing is active. The blitter can then reduce a packed pixel to five-bit luminance and select one of four recolored ramps without repeating floating-point work per pixel.

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

An RLE alpha token stores its repeat count in the high byte and its intensity in the low six bits. A run is therefore at most 255 pixels long. The shared editor splits longer constant spans, cuts runs at range boundaries, replaces or extracts intervals, and merges adjacent equal-intensity runs when their combined length still fits in one token.

The maximum-overlay operation walks two streams pixel by pixel, keeps the larger intensity, and coalesces the result. Alpha-screen gradients and HEA light masks both use these generic helpers. The helpers belong to the renderer rather than either source format.

One image representation locates each row by an offset relative to the packed alpha blob; another stores absolute row pointers. Variants can also apply a source color key, a global opacity, or two alpha streams.

Separate entry points implement luminance-ramp recoloring, screen-style per-component composition, and saturating additive blending. The dispatcher selects paired RGB565 or RGB555 scalar loops, or an MMX implementation when the optimized path is active.

### Gradient-mask read past the encoded runs

The NPC session's `AlphaScreenPane` builds one constant-intensity run stream per row. For a pane `W` pixels wide and `H` pixels high, `ui_alpha_screen_pane_rebuild_gradient_mask` allocates `2 * W` bytes for each row, then encodes exactly `W` pixels at intensity `floor(32 * row / H)`. At width 640, the encoder writes three 16-bit tokens covering 255, 255, and 130 pixels. The remaining allocation is uninitialized.

`render_blit_pointer_rle_alpha_mmx` consumes four alpha values per group and always processes one final group after the complete groups. Even when the drawn width is divisible by four, its zero destination-selection mask does not prevent the alpha reads. A full-width draw therefore consumes all 640 encoded values, then starts reading uninitialized tokens. A zero run count makes it keep fetching tokens, with no stream-end check. This can become an access violation after leaving the allocation.

The defect concerns the encoded length, not an allocation smaller than the six bytes initially written. Encoding four additional pixels would cover the alpha reads for this pane width, but the MMX tail also loads source and destination pixels. Padding the alpha stream alone does not establish that every access in the tail is safe. See the [instruction evidence and validation limits](../appendix/client-crash-faults.md#gradient-mask-over-read).

The [bounded-tail runtime patch](../appendix/runtime-patches/client-crash-fixes.md#alpha-tail) skips the unused tail for a width divisible by four and processes the final 1 through 3 pixels with word-sized accesses. Guarded x86 emulation checks its pixels and buffer boundaries; Windows integration remains a separate [VM test](../appendix/runtime-patches/client-crash-tests.md#prove-the-alpha-boundary-in-the-vm).

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
