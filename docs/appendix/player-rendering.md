# Player rendering evidence

The [player rendering chapter](../rendering/players.md) explains composition and animation. This reference keeps the static lookup locations and verification details separate from that flow.

All addresses below are static virtual addresses in the matching x86 executable, with preferred image base `0x00400000`. They identify analysis locations, not stable runtime pointers. The inspected file is 3,112,960 bytes with SHA-256 `054a5d6adc56099c6bfd9d2a58675aff62dc788b63209a3d906492f5b89e96c6`.

## Parts and placement

| Function | Static address | Direct evidence |
| --- | --- | --- |
| `render_select_human_part_sprite` | `0x005FD8D0` | Appearance selectors for categories 0-20; overcoat suppression |
| `render_format_human_part_filename` | `0x005FDA90` | Category-specific M exceptions, extended IDs, numeric or alphabetic suffix |
| `file_select_character_archive` | `0x00473880` | Lowercased M/W resource routing by second-letter range |
| `file_load_image_frame` | `0x0048B530` | Signed EPF bounds and cropped row pitch; zero pixmap on missing/out-of-range frames |
| `render_load_human_part_frame` | `0x005FDC90` | Final-frame position-table lookup, fallback anchors and palette assignment |
| `render_build_human_frame_layers` | `0x005FE3A0` | Direction order, body-5 exceptions, anchor subtraction and bounding union |
| `render_draw_human_part` | `0x005FED60` | Negates and exchanges horizontal rectangle edges when mirrored |
| `render_draw_human_frame_layers` | `0x005FEE70` | 21 ordered draws; emotion insertion immediately before category 4 |

Disassembly confirms the EPF signed loads, the two 16-bit companion reads, and the mirrored edge exchange. EPF bounds are runtime `top,left,bottom,right`. The human default-anchor table stores vertical then horizontal 32-bit integers. The file companion reverses that order to X then Y and writes only the low 16 bits of each runtime integer.

`render_blit_pixmap` (`0x0044FB80`) computes the primary source as `pixels + row * pitch + column`. Its indexed mode-1 loop at `0x0045048C` skips index zero, looks up one palette entry per byte, and advances the row pointer by the pixmap pitch. The mirrored loop writes destination columns backward. `render_get_effect_frame_image` independently reads the same dense primary EPF rows when converting an EPF effect into a 16-bit image.

| Static data | Address | Shape |
| --- | --- | --- |
| Normal part letters | `0x0068C284` | 21 category characters plus terminator |
| Extended part letters | `0x0068C29C` | 21 category characters plus terminator |
| Default part order | `0x0068C380` | Four consecutive 21-byte direction rows |
| Alternate part order | `0x0068C3D8` | Byte-identical to default in this target |
| Body-5 part order | `0x0068C430` | Four consecutive 21-byte direction rows |
| Default anchors | `0x0068C488` | 21 pairs of 32-bit `(y,x)` values; Y=70 throughout, X=55 for categories 8-15 and 28 otherwise |

The selector's shield-255 omission is at `0x005FE636`. Body-5 main weapon's absolute frame-zero override is at `0x005FE678`. Its category-18 motion replacement, when arms are zero, is at `0x005FE6A5`.

Palette selection remains per part. Body 1/5 and face use the direct skin palette; ordinary equipment uses its resource family and optional appearance recoloring. Body IDs at least 7 also receive the hair-color remap flag in `render_build_human_frame_layers`. The transform-table flag selects part blend mode 3 only on the ordinary palette path; the explicit recolor path calls its own palette blitter. Do not apply one global dye or alpha value to the whole equipment stack.

## Walk and idle execution

| Function | Static address | Role |
| --- | --- | --- |
| `world_living_start_move_animation` | `0x005E0610` | Chooses movement sequence and immediately invokes the actor timer callback |
| `world_living_handle_timer_event` | `0x005E1800` | Accepts timer `0x02000001` only for the current revision |
| `world_living_advance_animation_timer` | `0x005E0E20` | Advances a sample, requeues timer, refreshes image and displacement |
| `render_human_walk_sequence_ctor` | `0x005FFCD0` | Builds finite shared motion-0 descriptors with a five-frame view stride |
| `render_human_walk_get_interval` | `0x005FFF30` | Returns each sample's stored delay |
| `render_human_walk_build_frame` | `0x005FFF70` | Copies a sample and applies direction |
| `render_human_walk_get_displacement` | `0x005FFFE0` | Returns cumulative `(y,x)` sample displacement |
| `render_human_select_walk_sequence` | `0x00602CA0` | Remote, local coarse or local smooth selector |
| `render_human_image_session_advance_frame` | `0x006026D0` | Builds the current sample, applies direction signs and increments the counter |
| `render_human_advance_or_return_to_stand` | `0x00602640` | On exhaustion selects standing and immediately builds sample zero |
| `render_human_select_stand_sequence` | `0x006029E0` | Resets standing counter and returns 300 ms |
| `render_human_stand_initialize_parts` | `0x006002F0` | Probes each category's `04.epf`, retaining floor(frame_count/2) per view |
| `render_human_stand_build_frame` | `0x00600150` | Shared standing counter modulo each enabled category's own frame count |
| `world_living_finish_position_transition` | `0x005E0DD0` | Clears displacement and commits the staged tile for the applicable object policy |

The three walk objects are constructed by `0x00668320`, `0x00668340`, and `0x00668360`, with `(sample_count, local)` arguments `(4,0)`, `(4,1)`, and `(8,1)`. Their pointer globals are `0x006D3ABC`, `0x006D3AC0`, and `0x006D3AC4`. The normal standing fallback descriptor is initialized at `0x00668230` to motion 0, frame 0, stride 5, variant -1. It is replaced per category only when an eligible standing resource exists.

Each table below is an array of nine signed 32-bit entries per row, addressed as `base + sample_count * 36 + step * 4`. The constructor reads steps 1 through sample_count. Row element zero is not the first displayed walk sample.

| Table | Base | Four-step row, entries 1-4 | Eight-step row, entries 1-8 |
| --- | --- | --- | --- |
| Horizontal increments | `0x006D3D00` | 6,8,6,8 | 2,4,4,4,2,4,4,4 |
| Vertical increments | `0x006D3E48` | 3,4,3,4 | 1,2,2,2,1,2,2,2 |
| Pose index | `0x006D3F90` | 1,2,3,4 | 1,1,2,2,3,3,4,4 |
| Remote delay, ms | `0x006D40D8` | 100,100,100,100 | 50,50,50,50,50,50,50,50 |
| Local delay, ms | `0x006D4220` | 114,114,114,114 | 57,57,57,57,57,57,57,57 |

The remote eight-step row exists in the table but is not one of the three constructed walk objects. Horizontal signs at `0x006D4388` are `+1,+1,-1,-1`; vertical signs at `0x006D4398` are `-1,+1,+1,-1` for directions 0-3.

## Effect geometry

`file_decode_efa_frame` (`0x00457030`) returns header blend selector at +0x0C and flags at +0x10, frame X/Y anchors at +0x28/+0x2A, and X-first unsigned bounds/crop words. `render_get_effect_frame_image` (`0x00457FD0`) stores the crop and anchors in the frame cache. `render_effect_image_session_get_frame_info` (`0x00458630`) returns that crop, the two pivots, and flags bit 0.

`render_effect_prepare_frame_geometry` (`0x005DCFC0`) converts pivots for captured-direction X/Y flips, then rebases them against the actual attached image bounds. `render_effect_object` (`0x005DD380`) subtracts that adjustment from the image rectangle and adds the collected object origin. These steps reduce to the crop-minus-pivot formula on the [EFA page](../file-formats/efa.md#frame-position-and-direction).

`world_object_effect_ctor` (`0x005DD620`) selects layer 13, parent-relative position mode 1, local displacement zero, and nonlooping playback. `world_create_object_attached_effect` (`0x005CB590`) captures a living target's facing direction when constructing it. `render_collect_world_objects` (`0x005D3740`) adds parent origins before collecting the effect's draw entry. Facing is not reread on every effect tick in these paths.

## Reproducible checks and limits

Run `python3 binaryninja/scripts/verify_player_rendering.py --client-root client` from the repository root. It checks the executable fingerprint, static order/anchor/walk tables, selected instruction encodings, and the documented resource geometry against the private installation. It reads private data but emits only metadata, never pixels or extracted files.

The local `MM00101`, `WM00101`, `MU00101`, `MW00101`, and `MS00101` resources in their routed split archives have ten frames. The documented body and weapon placement example uses frame 1 from `khanmim.dat` and `khanmtz.dat`. Empty and negative-bound accessory frames also exist. The archive scan found no M/W-prefixed `.tbl` companions in the ten split character archives, while animated `04.epf` resources include differing and odd frame counts.

These are static-code and local-asset findings, not measured display timestamps or a pixel-perfect video comparison. Timer congestion can change actual presentation times. A particular cosmetic's full behavior requires its appearance selectors and resources; nonzero rest poses, riding previews and monster disguises take separate paths. Unknown EFA modes and secondary EPF payloads remain subject to the limits on their format pages.
