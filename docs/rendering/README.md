# Rendering system

The client uses a software renderer. Game art is drawn into 16-bit memory canvases first. DirectDraw is mainly the last step that puts the finished frame on screen.

This is the frame path at a glance:

```text
map tiles and image frames
            |
            v
     software blitters
            |
            v
   world pane and UI panes
            |
            v
      root screen canvas
            |
            v
 DirectDraw or window DC present
```

The main work happens in four layers:

1. `render_screen_tree_frame` starts a visual frame.
2. `render_screen_subtree` walks the visible pane tree with clipping.
3. Each pane draws its own content, then copies that content to its parent canvas.
4. `render_present_frame` copies or flips the completed canvas to the window.

The world view is part of the pane system. `WorldPane` has its own content hook, just like other panes. That hook calls `render_world_frame`, which draws the map and world objects before the pane is combined with the rest of the UI.

DirectDraw does not appear to be the sprite engine. Sprites, tiles, effects, transparency, and color blends are handled by client code before presentation.

## Read next

- [Renderer lifecycle](lifecycle.md) covers setup, presentation, and cleanup.
- [Text and fonts](text.md) covers bitmap glyphs, ANSI and DBCS decoding, IME input, and regional font selection.
- [World rendering](world.md) covers tiles, sprites, layers, and effects.
- [Map lighting](lighting.md) covers server time steps, ambient light profiles, and HEA masks.
- [Snow and weather](weather.md) separates snowy map art from particle overlays.
- [Walls and occlusion](walls-and-occlusion.md) covers SOTP blend flags and runtime visibility hooks.
- [Blending](blending.md) covers transparent pixels and software alpha.
- [File formats](../file-formats/README.md) covers the asset data consumed by these systems.

Function addresses are kept in the [function reference](../appendix/functions.md).
