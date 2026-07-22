# Renderer lifecycle

The renderer is created during normal application startup and released after the pane and asset systems shut down.

## Setup

`render_probe_display_capabilities` runs early. It asks DirectDraw about the current display and rejects unsupported display settings.

Later, `render_video_system_initialize` builds the live renderer:

1. Create and initialize the DirectDraw wrapper.
2. Create the main 16-bit memory canvas.
3. Create an output canvas used for conversion or scaling.
4. Build color conversion and software blend tables.
5. Remember the window, logical size, output format, and scale.

The main canvas is where the game draws. The output canvas adapts that result to the selected display path. This keeps most game drawing independent of the final Windows surface format.

## Logical resolution and 2x output

The game's native logical resolution is 640 by 480. Startup keeps those logical dimensions in both display modes.

`render_probe_display_capabilities` accepts 16-bit and 32-bit desktop color. A desktop at least 1280 by 960 selects the 2x mode; a smaller supported desktop selects 1x. The 2x path expands the completed 640 by 480 image to 1280 by 960 by copying each source pixel into a 2 by 2 block.

This is presentation scaling, not a larger game view. Pane geometry, input coordinates, the main canvas, and world rendering remain in the 640 by 480 logical coordinate system. The scaler uses nearest-neighbor copies with no smoothing or filtering.

## Canvas access

A canvas may own memory or wrap a DirectDraw surface. Drawing code calls `render_canvas_begin` before touching pixels and `render_canvas_end` afterward. These calls also lock or unlock a wrapped surface when needed.

Memory canvases use 16-bit pixels and an aligned row pitch. The logical width and row pitch are therefore related, but they are not always the same value.

Subcanvases do not own another pixel buffer. `render_canvas_resolve_backing` walks their parent chain, accumulates each local origin, and resolves the memory buffer or DirectDraw surface that owns the pixels. Clipping follows the same chain. `render_canvas_get_absolute_clip_rect` intersects every local clip rectangle before mapping drawing coordinates into the shared backing.

`render_canvas_lock_pixels` hides the backing difference from software drawing. Heap canvases return their stored pointer and pitch. Surface canvases call DirectDraw `Lock` and cache the returned pointer and pitch until `render_canvas_unlock_pixels`. If an unlock reports a lost surface, the client restores it and retries.

The client can also construct a top-down 16-bit `DIBitmap`. Its decoder expands an archive image to RGB555 and copies aligned rows into a GDI DIB section. This is a conversion boundary, not the main sprite drawing path.

## Redraw and presentation cadence

The root `ScreenPane` starts timer ID `0` during application setup. `render_screen_timer_tick` calls `render_screen_tree_frame`, then requeues itself for 10 ms after the current `timeGetTime()` value.

Each check walks the screen hierarchy, but drawing remains dirty-region based. A forced redraw or dirty pane-tree entry marks the root screen for presentation. If nothing changed, the client does not send an identical completed canvas to the output backend.

This makes 100 Hz the maximum scheduled redraw-check rate, not a fixed visible frame rate. The timer is requeued after the callback rather than from its previous due time, so a delayed callback shifts the following check instead of producing catch-up redraws.

## Presenting a frame

`render_present_frame` has two output paths:

- The DirectDraw path copies to the primary surface with `DDBLT_WAIT` or flips an attached backbuffer with `DDFLIP_WAIT`.
- The window DC path converts the canvas for GDI and uses `BitBlt`.

The wait flags allow DirectDraw to block until the operation can complete. The client does not compile a separate monitor refresh rate into this path. The output backend and display can therefore make the visible presentation rate lower than the 10 ms redraw-check cadence.

The output path applies the selected 1x or 2x presentation scale before the frame reaches the window or display surface.

The DirectDraw wrapper owns the display-mode transition. Entering full-screen mode selects exclusive cooperative access, applies the retained width, height, and bit depth, then restores its surfaces. Leaving full-screen mode restores the desktop display mode and normal cooperative level. Its smaller helpers copy between a surface-backed canvas and the primary surface with `Blt` or `BltFast`.

## Cleanup

The confirmed shutdown order is:

```text
panes and event objects
        |
        v
image and tile libraries
        |
        v
main canvas and blend helpers
        |
        v
VideoSystem object
        |
        v
DirectDraw surfaces and interface
```

`render_video_system_shutdown` releases the main canvas and software lookup tables. Deleting the `VideoSystem` then runs `render_video_system_dtor`, which releases DirectDraw surfaces, restores the display mode when needed, and releases the DirectDraw interface.

The mapped normal shutdown path does not explicitly delete the conversion canvas or call the separate effect-image-pool destroy helper. The process still reclaims that memory on exit, but these objects should not be treated as explicitly released without more runtime evidence.
