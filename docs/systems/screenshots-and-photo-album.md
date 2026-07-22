# Screenshots and the photo album

The client has two separate picture systems. The screenshot button saves the whole game window as a BMP. The portrait capture command renders only the local character into `album.dat`, where the User Info album can preview, save, remove, and reorder portraits.

| Action | Owner | Result |
| --- | --- | --- |
| Screenshot button | `GUIBackPane` | Numbered `lodNNN.bmp` file |
| Portrait capture | `WorldPane_Impl` | New record in `album.dat` |
| Album Save | `UserInfoPane_ForUser` | Extensionless JFIF portrait file |
| Album Remove | `UserInfoPane_ForUser` | Cleared `album.dat` record |

These paths do not send a packet. A saved portrait is uploaded only after the server sends [`SRequestPortrait`](../network/server/073-0x49-request-portrait.md).

## Full-window screenshots

The GUI layout names the button `BTN_SCREENSHOT`. `ui_gui_back_activate_action` maps bottom action 4 to `render_write_screenshot_bmp`.

The writer captures the completed client canvas and saves an uncompressed 16-bit Windows bitmap in the working directory. It starts with `lod001.bmp`, scans upward for the first missing filename, and stops before `lod1000.bmp`. The normal 640 by 480 client canvas produces `0x96000` bytes of pixel data.

The writer contains an optional stamp-selection path. Any nonzero `SStatus` privilege while Shift is held skips that path. The feature gate is a constant false stub in this exact binary, so no stamp is selected for ordinary users either and the privilege branch produces no visible difference.

This is unrelated to the RTTI packet named `SScreenShot`. That server packet opens a keyed town map. It does not invoke either local capture path.

## Capturing an album portrait

`ui_world_capture_self_portrait_to_album` calls `ui_capture_self_portrait_to_album` in normal mode. The capture flow is:

```text
render local player into a 48 by 56 canvas
    -> copy the 16-bit pixels
    -> find the first free album slot
    -> zlib-compress the pixels
    -> use the current time as the caption
    -> rewrite album.dat
```

The album holds 100 slots. A full album leaves the file unchanged and reports the failure in the game message area.

### One-hour cooldown

The normal capture path reads the last successful capture time from the `album.dat` header. It refuses another capture while:

```text
last_capture_time + 3600 > time(NULL)
```

The remaining time is shown in minutes. This is entirely client-side. No request or server reply participates. An internal nonzero capture argument bypasses the check, which gives a narrow runtime patch point without changing the file format or server traffic.

## Album panes

The current User Info album and the older album view share the same `album.dat` store and JPEG writer.

| RTTI class | Layout | Role |
| --- | --- | --- |
| `nui_AlbumPane` | `_nui_al.txt` | Current album tab, page controls, and 100 tile owners |
| `AlbumPicDialogPane` | `_nui_alb.txt` | One picture tile with Save and Remove controls |
| `AlbumInfoPane` | code-built | Older album owner |
| `AlbumViewPane` | `llalbum.txt` | Older scrollable list with Portrait, Del, and Save regions |

`ui_nui_album_pane_ctor` creates 100 `AlbumPicDialogPane` objects. Twelve records are visible at once as two adjacent six-item pages. Previous and Next move by two page numbers. The final view shows pages 16 and 17.

Inside each picture dialog, controls are attached in this order:

1. `SAVE`, action 0
2. `REMOVE`, action 1

`ui_user_info_handle_album_action` opens a confirmation. Confirmed Save uses timer event `0x1242`; confirmed Remove uses `0x1243`.

## Save and Remove

Save copies the selected 48 by 56 portrait, fills transparent pixels from `_nportbk.spf`, and writes the character's extensionless portrait file. If that file already exists, the client copies it to `<character>.bak` first.

The output is always JFIF JPEG. `file_write_jpeg_from_rgb16` uses the bundled IJG version 62 defaults:

- Quality 75
- Baseline tables
- YCbCr with 2 by 2 luma and 1 by 1 chroma sampling, also called 4:2:0

The writer also adds a JPEG COM marker containing `gen-<hex>-`. The hexadecimal value is derived from the bitwise complement of the current CRT time value. It is metadata inside the JPEG, not part of the portrait filename.

There is no Save branch for EPF or PCX. The older `AlbumViewPane` reaches the same JPEG writer. The uploader can read an existing portrait-sized EPF, but it does not convert album pixels into one. See [Portraits and profiles](portraits-and-profiles.md).

Remove clears the selected active record, rewrites `album.dat`, and refreshes the tiles. It does not delete the exported extensionless portrait or its `.bak` file.

## Extension options

A narrow patch can bypass the capture cooldown. Separate JPEG patches can raise the default quality and change the sampling to 4:4:4. Higher quality must still remain below the uploader's 8,000-byte JPEG limit. Exact bytes and scope are in [Photo album quality-of-life patches](../appendix/runtime-patches/photo-album.md).

Saving EPF requires new behavior rather than selecting a dormant client branch. The album stores rendered 16-bit pixels, while portrait EPF stores palette indexes resolved through `legend.pal`. An EPF exporter therefore needs a verified writer plus color quantization or another way to recover palette indexes.

The on-disk store is documented in [Album.dat](../file-formats/album.md).
