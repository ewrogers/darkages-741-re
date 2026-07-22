# Asset loading and lifetime

The client keeps its asset archives open for most of the process, then builds only the runtime form that each subsystem needs. Startup opens the required DAT archives and prepares shared palette state. Ordinary images, effects, fonts, layouts, map art, and sound then follow separate loading and cache rules.

There is no single universal asset pool. The client has several singleton libraries and managers, but a class named `ImageLib` is not necessarily a cache.

```text
startup
  -> open and map DAT archives
  -> construct asset managers
  -> load and pack palette families

runtime request
  -> find archive entry
  -> borrow an entry handle
  -> create a view or decode owned pixels
  -> keep the result according to the subsystem

shutdown
  -> release asset consumers and managers
  -> close and unmap DAT archives
```

## Archive lifetime

Each DAT has its own archive object and global accessor. The accessor constructs the object on first use. Application startup calls the required accessors and opens these archives:

| Archive | Main use |
| --- | --- |
| `Legend.dat`, with `DarkAges.dat` fallback | Shared game art, tables, and sound effects |
| `seo.dat` | Map tiles and their palettes and animation tables |
| `khanpal.dat` | Shared character palettes |
| `khanmad.dat` through `khanmtz.dat` | Male character resources split by the second filename letter |
| `khanwad.dat` through `khanwtz.dat` | Female character resources split by the second filename letter |
| `misc.dat` | Global same-name overlay for other archives |
| `setoa.dat` | UI layouts, ordinary pane art, and field-map resources |
| `national.dat` | Localized tables, fonts, and regional data |
| `ia.dat` | Static-tile art, flags, palettes, and animation tables |
| `roh.dat` | Effect art, palettes, frame tables, and motion-effect data |
| `hades.dat` | A separate asset family whose remaining consumers are still being named |

The main archive tries `Legend.dat` first and `DarkAges.dat` second. A missing required archive follows startup's failure path.

Two other singleton slots are not opened by normal startup. `file_get_transform_table_archive` is supplied to the `trans_a.tbl` through `trans_z.tbl` readers, but the matching archive identity is not yet confirmed. `HumanTileAttrList` reads positive numeric tokens from each file into one set selected by its `a` through `z` suffix. Human-part rendering queries those sets by category letter and tile attribute. `file_get_dormant_archive` has no normal asset consumer and is the slot used by the optional minigame asset patch.

`file_archive_open` opens an archive read-only, creates a read-only file mapping, and maps the complete file. The installed version 741 archives use the legacy layout, so an entry's data pointer refers directly to bytes in that mapping. The reader also supports an extended layout whose compressed blocks are expanded while the archive opens and retained until it closes, but the installed archives do not use that path.

An archive also has a small bounded pool of entry handles. `file_archive_find_entry` borrows one handle, records the entry pointer and size, and returns it to the caller. `file_archive_get_entry_data` exposes the stable mapped data. `file_archive_read_exact` and `file_archive_read` provide exact and partial sequential reads. The seek, tell, and size helpers keep positions relative to the selected entry rather than the whole DAT.

`file_archive_release_entry` returns only the temporary handle to the pool. It does not unload the entry bytes. `file_archive_close` releases the mapping, any expanded-layout storage, the handle pool, and the operating-system handles together.

The startup calls request 20 handle slots per archive. This pool limits simultaneous open entry descriptions. It is not an asset cache.

## `misc.dat` is a global overlay

The client checks `misc.dat` before the archive requested by the caller. When `file_archive_find_entry` receives any other archive object, it first asks the `misc.dat` archive whether it contains the requested name. If it does, the function returns the `misc.dat` entry instead of looking in the original archive.

This makes `misc.dat` a small patch archive. A same-named entry can replace an archived UI layout, image, palette, or other asset without rebuilding the DAT that normally owns it. The match is by archive-entry name and ignores ASCII letter case, just like an ordinary DAT lookup.

The override applies only to requests that pass through this archive lookup path. It does not replace loose files, map files opened directly from disk, or formats handled by unrelated readers. A bad replacement is also global: every caller requesting that name receives the `misc.dat` copy.

## FileUpdater extracts installed components

The RTTI class `FileUpdater` is a local DAT-to-filesystem installer, not a network downloader. It selects an entry in an already open archive, resolves a destination under the current directory, Windows directory, System directory, or Program Files, and can compare an existing file before replacing it.

`file_update_ahnlab_security_components` uses this helper with `national.dat`. It verifies or extracts `MFSVC.DLL`, four AhnLab MFGS DLLs, and `XUPDATE.EXE`. The Program Files mode creates the configured `Ahnlab\MFGS` subdirectories as needed. No HTTP or socket work occurs in `FileUpdater`; any archive refresh must happen elsewhere.

## Loading is synchronous

The active paths perform archive lookup, parsing, decompression, palette conversion, and middleware setup in the calling path. No background asset worker or asynchronous completion queue was found.

This means an asset requested while a pane is being constructed or an effect is advancing is loaded before that call returns. The client reduces repeated work with subsystem caches, but it does not hide a cache miss behind another frame.

## Ordinary EPF and SPF images

`ImageLib` is a small RTTI-backed singleton facade. It does not contain a filename dictionary or a decoded-frame collection. Callers such as `render_load_main_archive_pixmap` pass a filename, frame number, and destination pixmap to `file_load_image_frame` each time they need a view.

For an ordinary EPF frame, the loader fills geometry and plane fields in the caller's pixmap and points its primary and optional secondary planes into the mapped DAT entry. It does not allocate a Windows bitmap, upload a texture, or convert the whole frame to screen pixels.

```text
mapped EPF bytes
  -> lightweight PixMap view
  -> indexed pixel selected at draw time
  -> packed palette lookup
  -> 16-bit software canvas
  -> DirectDraw or GDI presentation
```

The software pixmap blitter performs transparency, palette lookup, and blending while it draws. The final pixels exist in the 16-bit canvas, not as a permanently prerendered EPF bitmap.

SPF follows the same broad ownership model. Its loader builds a frame view over the mapped resource and selects the display-dependent source plane when required.

Destroying a pane, world object, or other owner discards its small pixmap description. The underlying image bytes remain available because the DAT mapping remains open.

## How an EPF gets its palette

An EPF stores palette indexes, but it does not name its PAL file. The caller supplies or derives a palette selector.

Examples include:

- palette zero for common `legend.pal` art;
- item and icon range tables for item sprites;
- static, map-tile, field, monster, and effect palette tables for those asset families;
- packet-supplied monster palette selectors applied through resource-defined color ranges.

`PaletteMan` is constructed during startup. It loads `legend.pal` and enumerates the installed monster, effect, map-tile, static, GUI, item, and human palette families. Each 768-byte RGB palette is immediately converted to 256 packed RGB565 or RGB555 values, a 512-byte runtime table.

A runtime palette selector encodes a family in bits 24 through 30 and a palette number in its low 24 bits. Bit 31 is ignored by this lookup. A family grows its pointer array in blocks of 16. The first request for a missing number allocates one 512-byte table. No per-palette eviction path was found. The tables are released with the palette manager.

Some focused UI paths may load a named palette into this manager when the pane is created. That is still a synchronous load into the same packed-table model.

## Caches are subsystem specific

| Subsystem | First load | Runtime form | Retention |
| --- | --- | --- | --- |
| Ordinary EPF and SPF art | When a pane, object, or loader asks for a frame | Indexed pixmap view into mapped DAT bytes | The view follows its owner; archive bytes remain mapped |
| Palettes | Mostly during startup | 256 packed 16-bit colors per selector | Kept by `PaletteMan`; no individual eviction found |
| Effects | Effect session on first effect ID, frame on first frame request | Owned 16-bit `Image` for converted EPF or inflated EFA pixels | Cached by effect ID and frame |
| UI layouts | First layout request | Parsed named control and geometry records | Kept in the separate UI layout cache |
| Fonts | Font library startup | Mapped LFT glyph records plus temporary draw masks | Font data remains; a glyph mask is rebuilt when drawn |
| Sound effects | First play of a sound ID | Miles sample handle with archive-supplied MP3 or WAV data | Reused until audio shutdown |
| Ground and static map art | When a tile is needed | Decoded tile or cached visible layer | Explicitly invalidated by bank and animation changes |

The RTTI-backed `HumanImageLib`, `MonsterImageLib`, and `IconImageLib` singletons provide asset naming and construction paths for their domains. Their presence does not make every requested EPF a globally shared decoded bitmap. `render_icon_load_pixmap`, for example, derives an icon file and frame, fills the caller's pixmap through the ordinary image loader, then attaches the item palette selector.

## Effect images are different

`EffectImagePool` holds a pointer array indexed by effect ID. `render_effect_image_pool_get_frame` constructs one `EffectImageSession` the first time that ID is requested. The session then keeps one frame-cache record for each available frame.

`render_get_effect_frame_image` returns immediately when a frame is already present. On a miss:

- an EPF effect frame is read as indexed pixels, palette-converted once into an owned 16-bit `Image`, and cached;
- an EFA frame is inflated from zlib data into owned image storage and cached.

Each session also keeps a bounded set of live user pointers. Acquiring an existing user refreshes the same activity timestamp as adding a new one. Removing a user swaps the last pointer into its slot, so removal does not preserve user order.

`EffectImagePool` schedules a repeating 30-second cleanup. `render_effect_image_pool_prune_inactive` deletes a retained session when its activity timestamp is nonzero and more than 30 seconds old. This is age-based cache cleanup, not memory-pressure or least-recently-used eviction.

The pool also has a full clear routine that destroys every retained session, and each session destroys its decoded frames. That clear routine is reached through the pool destructor. The mapped normal shutdown path does not explicitly invoke the separate effect-pool destroy helper, but inactive sessions can still disappear during normal play through the cleanup timer.

## What is actually unloaded

The client uses several meanings of release:

- Closing an archive entry returns a short-lived handle slot. It does not unmap data.
- Destroying an ordinary pixmap owner drops a view. It does not free the mapped EPF bytes.
- Clearing a tile cache discards decoded tile results so the next draw rebuilds them.
- Destroying an effect session releases its owned decoded images. The effect pool may do this after 30 seconds without retained activity.
- Audio shutdown releases the cached Miles handles.
- `app_shutdown` closes and unmaps the archive objects after their consumers have been torn down.

No general memory-pressure eviction or least-recently-used list was found. Most subsystems rely on mapped views or long-lived caches. The effect-image pool is the confirmed exception with its own periodic age-based cleanup.

## File formats and rendering

This page describes runtime ownership and lifetime. The bytes on disk remain documented separately:

- [DAT archives](../file-formats/dat-archives.md)
- [EPF images](../file-formats/epf.md)
- [SPF images](../file-formats/spf.md)
- [EFA effects](../file-formats/efa.md)
- [PAL color palettes](../file-formats/pal.md)
- [Rendering system](../rendering/README.md)
- [Function reference](../appendix/functions.md)
