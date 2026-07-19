# NPC dialog illustrations

NPC dialogs can replace the small world sprite with a large speaker illustration. The server supplies the NPC name, the client maps that name to an image in `npc/npcbase.dat`, and `NPCIllustPane` draws the decoded image beside the dialog. If any step fails, the normal NPC tile remains visible instead.

## Flow

```text
SScreenMenu 0x2F or SPursuitMessage 0x30
    -> NPCSession reads speaker name and illustration index
    -> NPCIllustFileMan resolves name to an archive entry
    -> common image loader opens frame 0 of the SPF
    -> NPCIllustPane sizes itself to the frame and draws it

lookup or decode failure
    -> hide NPCIllustPane
    -> show NPCTilePane
```

`ui_npc_session_handle_network_event` accepts both server packet classes. `ui_npc_session_update_speaker_art` extracts the layout-specific speaker fields and calls `ui_npc_illustration_pane_set_image`. The two packet layouts place the name at different offsets, but the later lookup and drawing path is shared.

## Name mapping

`NPCIllustFileMan` opens `npc/npcbase.dat` and first loads its `npci.tbl` entry. It also subscribes to the server-managed metadata table named `NPCIllust`. A metadata update adds or replaces mappings in the same runtime lookup.

The lookup uses the complete NPC name as its key. No case folding, trimming, or partial matching was found. The `npci.tbl` loader can attach a list of image filenames to one name, and the packet's illustration index selects one entry from that list.

The inspected `metafile/NPCIllust` cache inflates to 170 name groups. Every group contains exactly one value, so the working index is zero for those rows. The values reference 26 distinct SPF files in `npcbase.dat`. For example, several named shamans map to `shaman.spf`, while many merchant names share `bank.spf`. The metadata is a shared-art lookup, not an image container.

See [Metadata files](../file-formats/metadata.md) for the zlib and group container and [DAT archives](../file-formats/dat-archives.md) for `npcbase.dat`.

## Illustration pixels

All 26 SPF files referenced by the inspected metadata use the same simple representation:

- one frame;
- `pixel_mode = 0` and `palette_mode = 0`;
- a 256-entry RGB565 palette followed by a 256-entry RGB555 palette;
- one uncompressed byte per pixel in row-major order;
- a row pitch equal to the frame width;
- palette index zero as transparent.

The observed frames range from 162 to 339 pixels wide and 299 to 365 pixels high. The frame record supplies `left`, `top`, `right`, and `bottom` bounds. Width is `right - left`; height is `bottom - top`.

At draw time, `render_blit_pixmap` reads each nonzero source byte, selects the palette table matching the active 16-bit pixel format, and writes the packed color into the software canvas. There is no SPF decompression, run-length coding, or per-pixel scrambling in this path. `NPCIllustPane` uses normal transparent blitting, so background pixels remain visible wherever the source index is zero.

See [SPF images](../file-formats/spf.md) for the complete container layout.

## Known limits

The generic SPF reader supports other pixel modes, multiple frames, optional frame values, and a direct 16-bit pixel path. None of those variants occurs in the 26 illustration files selected by this installation's cached metadata.

The metadata update handler clears a name's current list before it appends each supplied value. If a metadata group contains several values, only its final value survives. The inspected cache supplies one value per name, so this behavior does not lose any current entry and only index zero is exercised. A multi-entry mapping can still come from `npci.tbl`.
