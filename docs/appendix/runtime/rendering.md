# Rendering objects

The renderer draws into software canvases before presenting the completed frame through DirectDraw. These layouts keep only the fields confirmed by the mapped drawing and presentation paths.

## Video system fields

```text
struct VideoSystemFields {
    bool initialized           // +0x10
    s32 logical_width          // +0x1C
    s32 logical_height         // +0x20
    Canvas *main_canvas        // +0x24
    Canvas *output_canvas      // +0x28
    u32 display_format         // +0x2C
    u32 output_pixel_size      // +0x30
    u32 scale                  // +0x38
    HWND window                // +0x3C
}
```

The main canvas uses 16-bit software pixels. The output canvas is used when the final Windows surface needs conversion or scaling.

## DirectDraw wrapper fields

```text
struct DirectDrawFields {
    bool initialized                // +0x0C
    s32 width                       // +0x10
    s32 height                      // +0x14
    u32 mode                        // +0x24
    IDirectDraw *direct_draw        // +0x28
    IDirectDrawSurface *primary     // +0x2C
    IDirectDrawSurface *backbuffer  // +0x30, optional
    IDirectDrawClipper *clipper     // +0x34, optional
}
```

DirectDraw presents the completed canvas. Sprite and effect blends happen before these surfaces receive the frame.

## Canvas fields

```text
struct CanvasFields {
    u32 storage_mode       // +0x6C, memory or wrapped surface kind
    void *pixel_allocation // +0x98, owned memory in storage mode 4
    s32 row_pitch          // +0x9C, bytes between pixel rows
    bool drawing_active    // +0xD4, set by begin and cleared by end
    s32 logical_width      // +0xE8
    s32 logical_height     // +0xEC
    s32 storage_width      // +0xF0, aligned to four pixels for memory canvases
    s32 storage_height     // +0xF4
}
```
