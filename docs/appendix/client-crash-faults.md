# Client crash faults

Several client crashes start with a resource lookup or packet value that is accepted farther than its consumer can safely handle. This reference separates the verified code paths from the runtime results reported by a contributor in *Dark Ages 7.41 Crash Fixes*. The report supplied investigation leads; its crash stacks, packet counts, heap contents, and post-fix endurance runs were not independently reproduced.

The private executable matches the [target fingerprint](../../contributing/research-policy.md#project-goal). The findings below were checked against the open Binary Ninja database, its decompiler and disassembly, and the original instruction bytes. All addresses are static virtual addresses at preferred image base `0x00400000`, not stable process addresses. Names are the existing project analysis names; `AlphaScreenPane`, `FieldMapBalloonPane`, and the packet class names have target RTTI provenance. The [function reference](functions.md) links each name to its durable source records.

| Reported fault | Binary-supported conclusion | Remaining limit |
| --- | --- | --- |
| Field-map changes exhaust archive handles, then dialog painting divides by zero | Confirmed lost palette handle and complete lookup-failure-to-division path | Exact cycle count depends on initial occupancy, other borrowers, overlay entries, and which image loads next |
| NPC-dialog gradient reads beyond its alpha runs | Confirmed producer length and unconditional MMX tail reads | Actual heap contents and the reported crashes were not reproduced |
| Status elements index beyond ten names | Confirmed unchecked indexes reaching string formatting | No offending packet was supplied |
| Off-map ground item crashes the draw-objects handler | Confirmed bounds rejection followed by a null dereference | The report's claim that cell insertion lacks a bounds check is incorrect; the source of invalid coordinates is unknown |

No executable bytes were changed. [Client crash fixes](runtime-patches/client-crash-fixes.md) now records exact hook bytes, stub bytes, and relocations with instruction-level emulation results. [Testing client crash fixes](runtime-patches/client-crash-tests.md) covers the remaining Windows and Arbiter checks. Emulation does not establish native-client integration.

## Field-map handle exhaustion

The runtime ownership model is explained in [Asset loading and lifetime](../systems/asset-loading.md#field-map-palette-handle-leaks).

| Evidence site | Verified behavior |
| --- | --- |
| `file_archive_open`, `0x00471E00` | Allocates a zeroed pool of `count * 0x14` bytes; stores its pointer at archive `+0x3C` and count at `+0x40` |
| `app_initialize`, `0x004AABDF..0x004AABEF` | Opens `setoa.dat` with a requested count of `0x14`, or 20 handles |
| `file_archive_find_entry`, `0x00472470` | Leases a free slot, or returns zero when none is free, including when the file exists; both legacy and extended indexes use the bounded pool |
| `file_archive_release_entry`, `0x00472760` | Clears an active slot's first 32-bit in-use flag; it does not unload mapped bytes |
| `ui_load_field_map_assets`, `0x00476F0B..0x00476F22` | Returns early when the name matches the last successfully loaded field map |
| Palette probe, `0x00476FCF` | Calls `file_archive_find_entry`; the result in `[ebp-0x10]` is only compared with zero and is never released |
| Palette loader, `0x00548730` | Performs its own lookup, reads the palette, and releases its own handle |
| Text lookup/release, `0x00477031` / `0x00477589` | Holds a separate metadata handle and returns it on normal completion |
| `file_provider_get_field_map_archive`, `0x00473A70`, and `file_provider_get_layout_archive`, `0x00473A50` | Both resolve to the `setoa.dat` singleton |

Each successful palette probe that reaches this path loses one slot. An unchanged map name does not execute the probe. A later metadata failure also does not undo a successful palette probe. `misc.dat` can redirect a same-name lookup, so the lost handle belongs to the archive that actually satisfies it.

The resulting dialog failure follows this chain:

1. `ui_dialog_draw_background` (`0x004463C0`) requests `DlgBack2.spf` when no background name is configured, then calls the tiler without checking that the pixmap has usable dimensions.
2. `file_load_image_pixmap` selects the layout archive for its null archive argument. `file_load_image_frame` (`0x0048B530`) clears the pixmap, including its rectangle, when the SPF lookup or frame selection fails.
3. `render_canvas_tile_pixmap` (`0x00453860`) computes tile counts by dividing the destination extent minus one by the source extent. `0x0045392E` is `idiv dword [ebp-0x44]`, the source-width division; `0x0045393F` divides by source height. Zero extents reach these instructions without a guard.

This establishes a client fault independent of the report's particular ten-round-trip observation. Twenty successful probes can fill an initially free 20-slot pool, but the next failing consumer and exact number of crossings are not universal constants. An internal slot leak also need not change operating-system handle counts.

The existence-only call can use `file_archive_contains` (`0x00472720`): it finds, releases, and returns 1 or 0. Both the original lookup and this helper accept the same `this` and one stack argument and return with `ret 4`; the caller uses only zero versus nonzero. This supports the reported call-retargeting idea statically. It does not independently validate the reported endurance result. Guarding empty pixmaps at the drawing boundary addresses a separate unchecked precondition.

## Gradient-mask over-read

See [Blending](../rendering/blending.md#gradient-mask-read-past-the-encoded-runs) for the rendering explanation.

`ui_alpha_screen_pane_rebuild_gradient_mask` (`0x00403FE0`) derives width as canvas `right - left` and height as `bottom - top`. It allocates a row-pointer table and one `2 * width` byte allocation per row. `render_alpha_runs_fill` (`0x004867C0`) receives the width as a 16-bit count and writes tokens with a maximum run of 255, low-six-bit intensity, and no end sentinel. Only the encoded tokens are initialized.

For width 640, each row has a 1280-byte allocation but only six initialized bytes. The runs are `255 + 255 + 130 = 640`. The row intensity is `floor(32 * row / height)`. This is a vertical gradient built from constant horizontal rows, correcting the earlier export's description of per-column buffers.

| Evidence site | Verified behavior |
| --- | --- |
| Row allocation, `0x0040406D..0x00404086` | Requests twice the width in bytes through the uninitialized allocation path |
| Encoder arguments, `0x004040AC..0x004040C6` | Passes the low 16 bits of width, not width plus a padding group |
| MMX group count, `0x00411A6A..0x00411A70` | Uses `draw_width >> 2` complete groups |
| Full-group exit, `0x00411B23..0x00411B25` | Always enters the tail at `0x00411C67` |
| Tail token fetch, `0x00411C8B..0x00411C9A` | If the remaining run count is zero, repeatedly loads `word [esi]` and advances by two until a nonzero count appears |
| Tail pixel loads, `0x00411D0E` / `0x00411D11` | Loads a four-pixel source and destination group before the final masked store |
| Remainder mask table, `0x006C429C` | Remainder zero selects an all-zero 64-bit destination-selection mask; it does not bypass token or pixel loads |

A full-width 640-pixel draw consumes all valid runs before the unconditional tail. The next token is already outside the initialized stream. Consecutive zero-count tokens can carry the read beyond the allocation and eventually fault at the reported `0x00411C94`. Nonzero uninitialized counts can stop that scan sooner; an immediate crash is not guaranteed.

The only direct caller of `render_canvas_set_alpha_mask_rows` in this analysis is the gradient builder. The two direct `AlphaScreenPane` constructor callers are the NPC screen-menu and pursuit-session constructors. These establish the dialog-overlay path. A generic blitter and indirect dispatch do not justify treating every crash in the MMX function as a proven crash from a specific NPC exchange.

Encoding `width + 4` pixels supplies enough alpha values for the final group at the normal pane width. This supports the report's padding idea for the alpha stream. It does not remove the tail's source/destination pixel loads or the encoder's 16-bit count limit. The documented [bounded-tail patch](runtime-patches/client-crash-fixes.md#alpha-tail) instead skips a zero remainder and processes partial groups with one-pixel accesses. Its guarded full-function emulation passes; no repair was installed in the Windows client here.

## Unchecked status elements

The [`SStatus` reference](../network/server/008-0x08-status.md#elements) owns the wire layout and valid element names.

`net_deserialize_status_server_packet` reads the attack byte at `0x0059C720` and defense byte at `0x0059C733`, zero-extends each, and stores them in packet fields `+0x6C` and `+0x6E`. `ui_extra_status_info_update_from_status_packet` (`0x00575FB0`) copies them to pane fields `+0x4FC` and `+0x4FE` without validation.

`ui_extra_status_info_format_values` (`0x00575AA0`) builds ten local pointers to narrow NUL-terminated strings stored at `0x00685564..0x006855AC`, then uses the two signed 16-bit pane values as indexes. The wire path supplies nonnegative values, but nothing restricts them to 0 through 9. The attack lookup precedes the formatting call at `0x00575B11`; the defense lookup is at `0x00575B23` before the call at `0x00575B3C`. Their return addresses are `0x00575B16` and `0x00575B41`, matching the reported stack sites.

The `%s` arguments are therefore arbitrary stack-derived pointers when the index leaves the local array. The formatter's output limit of `0x80` does not validate those input pointers. The report's `0x00647631` site is a byte-string scan, consistent with this failure, but no offending element value or original stack capture was supplied for independent validation. The target code proves the unsafe lookup, not whether the server, a transform error, or unrelated corruption supplied the value. Validate both element bytes before they reach the lookup.

## Rejected ground-item insertion

The [`SDrawObjects` reference](../network/server/007-0x07-draw-objects.md#rejected-ground-item-positions) owns the variable record layouts and current-map bounds.

| Evidence site | Verified behavior |
| --- | --- |
| `net_read_draw_object_record`, `0x00598B30` | Reads X and Y as big-endian `u16` values and widens them into temporary 32-bit coordinates |
| `world_object_list_insert`, `0x005E5D6F..0x005E5D93` | Rejects negative X/Y, X at or beyond width, or Y at or beyond height before selecting a cell |
| Dimension accessors, `0x005E6860` / `0x005E6880` | Read current `WorldObjectList` width at `+0x5C` and height at `+0x60` |
| `world_create_item_object`, `0x005CAC60` | Removes an old matching ID first; if insertion fails, releases the new item references and writes a null result |
| Item handler, `0x005F32D3..0x005F32F6` | Calls the item creator, then fetches its vtable without checking the result |
| Faulting dereference, `0x005F32F1` | `mov edx, dword [eax]`, with `eax` loaded from the returned item pointer |

The fault is failure handling after a checked insertion, not an unchecked coordinate write into the map array. The monster path tests its result before appearance updates; the item path invokes primary-vtable slot `+0x28` first and checks the pointer only during later reference cleanup.

An invalid coordinate can reproduce this control-flow condition even when below 255. For example, X equal to 40 is invalid on a map whose width is 40. The one-byte dimensions from `SMapSize` top out at 255, making 254 the largest possible valid coordinate on that axis. A test that rejects only values above 255 is incomplete. A client repair must handle a null creation result before calling the refresh method. This also covers other creation failures reaching the same result contract.

The contributor's packet/crash correlation supports investigating this path, but neither the claimed packet population nor the proposed wrong-key cause was independently validated. The binary establishes the deterministic rejection/null-use chain.

## Other reported leak candidates

| Function | Ownership result |
| --- | --- |
| `ui_field_map_balloon_pane_ctor`, `0x00474310` | Confirmed lost palette handle at lookup `0x004743E2`; the raw data view is consumed by `file_palette_load_rgb`, but the handle remains a local and is never released |
| `ui_field_map_balloon_pane_dtor`, `0x00474630` | Resets the two vtables and calls `ui_pane_dtor`; there is no retained palette handle to return |
| `audio_sfx_get_or_load`, `0x00568B60` | MP3 miss permits the WAV attempt; either successful lookup joins the release at `0x00568D8C`, including when Miles rejects the sample |
| `file_open_static_tile`, `0x005FD700` | The ordinary-art lookup occurs only after alternate-art lookup failure; a successful handle is released at `0x005FD7EC` after copying bytes and before decoding |

The balloon palette block runs only while its shared palette ID is negative. A successful allocation replaces that sentinel, so this is a guarded initialization leak, not evidence of one leak per balloon. Counting two lookup instructions and one release instruction is insufficient to diagnose ownership: mutually exclusive attempts can share a release, and a retained palette ID is not an archive-entry handle.

## Durable evidence and limits

[`client-crash-faults.yaml`](../../analysis/exports/client-crash-faults.yaml) preserves the verified function identities and instruction comments in the existing schema. The matching [analysis synchronization script](../../binaryninja/scripts/sync_user_analysis.py) imports and exports names and comments without applying executable patches. The corrected row-buffer description also updates the existing rendering export.

These are static client findings. They do not certify a launcher, reproduce Windows heap placement, validate the contributor's reported long runs, or identify the origin of malformed values. Those questions require separate runtime evidence.
