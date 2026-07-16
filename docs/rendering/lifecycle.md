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

## Canvas access

A canvas may own memory or wrap a DirectDraw surface. Drawing code calls `render_canvas_begin` before touching pixels and `render_canvas_end` afterward. These calls also lock or unlock a wrapped surface when needed.

Memory canvases use 16-bit pixels and an aligned row pitch. The logical width and row pitch are therefore related, but they are not always the same value.

## Presenting a frame

`render_present_frame` has two output paths:

- The DirectDraw path copies to the primary surface or flips an attached backbuffer.
- The window DC path converts the canvas for GDI and uses `BitBlt`.

The output path can also double pixels for a 2x nearest-neighbor scale. It does not smooth or filter the image.

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
