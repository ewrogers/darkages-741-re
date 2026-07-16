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

## Why DirectDraw is not doing the blend

The sprite loops read source pixels, test transparency, combine color components, and write the destination canvas directly. DirectDraw receives the completed canvas later. This means normal sprites and alpha effects behave the same across the DirectDraw and window DC presentation paths.
