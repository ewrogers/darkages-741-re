# Player rendering

An aisling is drawn as one temporary composite image made from as many as 21 body and equipment parts. The world renderer does not draw armor, hair, and weapons as independent world objects. `HumanObjectImageSession` selects their frames, palettes, and order, builds the composite, and `render_living_object` places that result into the world.

Both the local character and other visible users use this path. Their appearance normally comes from [`SDrawHumanObjects`](../network/server/051-0x33-draw-human-objects.md). A head sprite of `0xFFFF` selects the separate monster-disguise path.

For an implementation, keep three inputs separate: the appearance chooses resources, the current motion chooses frames, and each frame's bounds and anchor place its pixels. Walking moves the completed image through the world. A spell effect attached to the character is a separate world object with its own clock.

The [player rendering evidence](../appendix/player-rendering.md) records the Binary Ninja functions, static tables, and local asset checks behind this page.

## Two stored views and four directions

The client stores two directional frame groups per human-part motion. It mirrors each group to obtain the paired direction.

| Direction | Value | Stored frame group | Mirror horizontally |
| --- | ---: | ---: | --- |
| left | 0 | 0 | no |
| down | 1 | 1 | no |
| right | 2 | 1 | yes |
| up | 3 | 0 | yes |

This is close to a front-and-back model, but the safest description is two isometric direction groups. Left and up share one group. Down and right share the other.

Motion descriptors supply the number of frames per view. Walking and the ordinary standing fallback use a fixed stride of five. Optional standing-animation resources use half their declared frame count, rounded down:

```c
view_frame = motion_frame + direction_group * frames_per_view;
mirror = direction == RIGHT || direction == UP;
```

The mirror is applied by the final pixmap draw. It changes both the horizontal bounds and the pixel traversal.

## Appearance record

The packet parser converts its fields into a stable 0x30-byte `HumanAppearanceRecord`. The record retains the resource prefix, head and body choices, skin, hair color, clothing, armor, weapon, shield, accessories, overcoat, rest pose, translucent state, and face.

The packed body byte combines two fields. The high nibble selects the body form. The low nibble becomes `pants_color`, and any nonzero value also enables pants sprite 1.

```c
body_form = (packed_body & 0xF0) >> 4;
pants_color = packed_body & 0x0F;
pants_sprite = pants_color != 0 ? 1 : 0;
```

## Male, female, and special bodies

The M or W prefix is part of the asset lookup, not only character metadata. Normal male and female forms both use body sprite 1, but resolve through different first-letter resource families. The same prefix choice applies to most clothing and appearance categories, so a female aisling is not produced by recoloring or mirroring the male composite.

| Packed high bits | Protocol name | Client prefix | Body sprite | Confirmed client behavior |
| ---: | --- | --- | ---: | --- |
| `0x00` | `None` | M | 0 | No base-body resource |
| `0x10` | `Male` | M | 1 | Normal male form |
| `0x20` | `Female` | W | 1 | Normal female form |
| `0x30` | `MaleGhost` | M | 2 | Nonblocking ghost form |
| `0x40` | `FemaleGhost` | W | 2 | Nonblocking ghost form |
| `0x50` | `MaleInvisible` | M | 1 | Normal male parts, forced translucent |
| `0x60` | `FemaleInvisible` | W | 1 | Normal female parts, forced translucent |
| `0x70` | `MaleJester` | M | 4 | Jester body, no additional state flag |
| `0x80` | `MaleHead` | M | 5 | Head-only male form used by the observed swimming appearance |
| `0x90` | `FemaleHead` | W | 5 | Head-only female form used by the observed swimming appearance |
| `0xA0` | `MaleBlank` | M | 10 | Raw body ID 10 |
| `0xB0` | `FemaleBlank` | M default | 11 | Raw body ID 11 |

The friendly names are project-owner protocol vocabulary, not strings recovered from the executable. The first ten selectors have explicit switch cases in client 741. Values `0xA` and `0xB` take the switch's greater-than-9 path: the parser keeps raw body IDs 10 and 11, while the zero-filled resource-prefix field remains M for both. `FemaleBlank` is therefore distinguished by body ID 11 rather than a W prefix in this client.

`MaleInvisible` and `FemaleInvisible` are renderer-visible translucent forms. They keep body 1 and the normal equipment stack, then force `is_translucent = 1`. They are different from the all-zero appearance record used when an entity should contribute no visible sprite at all.

Body 1 and body 5 use the special `MM001` or `WM001` and `MM005` or `WM005` body families. Other body IDs use the ordinary body part letter. Ghosts therefore resolve through `MB002` or `WB002`, Jester through `MB004`, and Blank through `MB010` or `MB011`, followed by the motion suffix.

Skin tone is not applied uniformly to every base body. Category 1 uses the direct `skin_color` palette only for body sprites 1 and 5. Ghost body 2, Jester body 4, and Blank bodies 10 and 11 keep the palette resolved from their own resources. The face category still uses `skin_color` when a face part is present.

### Special bodies and equipment

The renderer has no `body == 2` rule that removes armor from `MaleGhost` or `FemaleGhost`. `render_human_stand_initialize_parts` loops through every category from 0 through 20 for every body. `render_select_human_part_sprite` returns the armor, arms, pants, weapon, shield, and accessory selectors independently of the body sprite. Its only confirmed clothing-wide suppression is an overcoat, which removes pants, armor, and arms.

Ghost body 2 and Jester body 4 use the default direction-dependent part order. Head body 5 is the only special body with a distinct order table, and only for down and right, where it moves the main weapon behind the body.

This makes the observed unarmored ghost appearance data-driven. The server can send zero armor and equipment selectors with the Ghost body, and zero selectors produce no part resources. A missing compatible frame also omits a visual layer. The client code itself does not silently clear armor because `MaleGhost` or `FemaleGhost` was selected. The installed character archives are available for resource checks; a particular server appearance is still needed to explain a particular ghost's missing equipment.

## Part categories

`render_select_human_part_sprite` resolves these 21 categories. Some equipment has two draw categories because it can contribute a front and a rear layer.

The default anchor is written here as `(x, y)` in pixels. A companion position table replaces it for the selected frame. The category number is a rendering slot, not an inventory equipment-slot ID.

| Category | Part | Letter, normal / extended | Default anchor | Selector and omission rule |
| ---: | --- | --- | --- | --- |
| 0 | shield | S / S | (28, 70) | Shield selector; forced M prefix; selector 255 is omitted |
| 1 | body | B / B | (28, 70) | Body selector; IDs 1 and 5 use M as the part letter |
| 2 | pants | N / N | (28, 70) | Pants selector; omitted with overcoat |
| 3 | boots | L / L | (28, 70) | Boots selector and color |
| 4 | head or hair | H / H | (28, 70) | Head selector and hair color |
| 5 | armor | U / I | (28, 70) | Armor selector; omitted with overcoat |
| 6 | internal clothing | D / D | (28, 70) | Internal selector; zero in this packet path |
| 7 | arms | A / J | (28, 70) | Arms selector; omitted with overcoat |
| 8 | main weapon | W / W | (55, 70) | Weapon selector |
| 9 | accessory 1 front | C / C | (55, 70) | Accessory 1 selector and color |
| 10 | accessory 1 rear | G / G | (55, 70) | Same accessory 1 selector and color |
| 11 | accessory 2 front | C / C | (55, 70) | Accessory 2 selector and color |
| 12 | accessory 2 rear | G / G | (55, 70) | Same accessory 2 selector and color |
| 13 | accessory 3 front | C / C | (55, 70) | Accessory 3 selector and color |
| 14 | accessory 3 rear | G / G | (55, 70) | Same accessory 3 selector and color |
| 15 | alternate weapon | P / P | (55, 70) | Same weapon selector |
| 16 | alternate head | E / E | (28, 70) | Same head selector and hair color |
| 17 | rear head | F / F | (28, 70) | Same head selector and hair color |
| 18 | overcoat clothing | U / I | (28, 70) | Overcoat selector and color |
| 19 | overcoat arms | A / J | (28, 70) | Same overcoat selector and color |
| 20 | face | O / O | (28, 70) | Face selector and skin palette |

Zero selectors generate no filename. A missing resource, invalid frame index, or empty frame contributes no pixels. A two-layer accessory therefore need not show both layers in both stored views. The three accessory positions all use the C/G families; their rendering slots determine their relative order when they overlap.

Body sprites 1 and 5 in category 1, plus the face in category 20, use the selected skin palette directly. Hair, boots, pants, accessories, and overcoat use their corresponding color selectors. The armor palette selector comes from the internal record field at `+0x16`; this packet path sets it to zero.

Category 1 with a body ID of at least 7 also receives the hair-color remap. Keep a part's resource palette and its optional recoloring separate; the final composite blend is another operation. Indexed zero leaves previously drawn pixels intact. See [Blending](blending.md) for palette and transparency behavior.

An overcoat is a replacement clothing set, not just another layer over ordinary clothes. Its presence suppresses pants, armor, and arms before composition.

## Asset selection

For ordinary IDs up to 999, the part-letter table is:

```text
SBNLHUDAWCGCGCGPEFUAO
```

For extended IDs above 999, the client subtracts 1000 and uses:

```text
SBNLHIDJWCGCGCGPEFIJO
```

The category indexes the string. Extended armor, arms, and overcoat therefore select different letter families.

The normal filename shape is:

```text
[M or W][part letter][three-digit sprite][two-digit motion].epf
```

The motion number written to the filename is the internal motion plus one. An alphabetic variant replaces the two-digit motion suffix with `a + variant`, rather than appending a letter to the digits. Walking uses internal motion 0, hence files ending in `01.epf`. Animated standing parts use internal motion 3, hence `04.epf`.

Shields always use M. Main weapon IDs 130 and 131, and category-4 head ID 103, also force M. This exception is category-specific: do not automatically apply the main weapon exception to its P layer or the H exception to E/F layers. Body 5 uses the `MM005` or `WM005` motion family.

`file_select_character_archive` lowercases the filename for routing. M resources go to `khanm{ad,eh,im,ns,tz}.dat`, and W resources to the matching `khanw` archives, according to second-letter ranges A-D, E-H, I-M, N-S, and T-Z. Use that selected archive, even when `khan.dat` or `Legend.dat` contains an older resource with the same name. See [Asset loading](../systems/asset-loading.md).

## Back-to-front part order

The renderer does not use one universal equipment order. It selects a 21-entry category list from the direction and body, then draws from the start of that list to the end.

| Case | Back-to-front category order |
| --- | --- |
| left or up | `0, 10, 12, 14, 1, 20, 2, 3, 5, 18, 6, 17, 8, 7, 19, 4, 16, 15, 9, 11, 13` |
| down or right | `17, 10, 12, 14, 1, 20, 2, 3, 4, 5, 18, 6, 8, 7, 19, 16, 15, 0, 9, 11, 13` |
| body 5, down or right | `17, 10, 12, 14, 8, 1, 20, 2, 3, 4, 5, 18, 6, 7, 19, 16, 15, 0, 9, 11, 13` |

The body-5 list moves the main weapon behind the body for down and right. The client contains a separately selected alternate table, but its bytes are identical to the default table in version 741.

The client keeps this order throughout a walk. The artwork changes the pose; the renderer does not move the shield or weapon to another slot halfway through the step. For left/up the shield is behind the body. For down/right it is in front of the ordinary equipment. C accessory layers finish the composite in accessory order 1, 2, 3, while their G layers precede the body.

An emotion image, when present, is inserted immediately before category 4, not after the whole character. It uses the `(28, 70)` anchor. The selected `emot02`, `emot03`, or `emot04` image can suppress accessory-1's C layer; `emot01` uses the skin palette. This insertion is separate from the face's O layer.

## Positioning each part

[EPF](../file-formats/epf.md) records its signed bounds in `top, left, bottom, right` order. Width is `right - left`; height is `bottom - top`. Bottom and right are exclusive. Header width and height are metadata, not a rectangle into which every frame must fit.

Treat every selected frame as a cropped image with its original placement retained. Subtract its anchor from its bounds before drawing. In conventional `(x, y)` coordinates, where `origin` is the character's common draw origin:

```c
left = frame.left - anchor.x;
right = frame.right - anchor.x;
top = frame.top - anchor.y;
if (mirror) {
    old_left = left;
    left = -right;
    right = -old_left;
}
draw_x = origin.x + left;
draw_y = origin.y + top;
// Draw cropped pixels, reversing each row when mirror is true.
```

Mirror around the common character origin after subtracting the anchor. Mirroring each crop in place leaves the weapon on the wrong side. In per-pixel terms, source column `u` lands at `origin.x - (frame.left - anchor.x + u) - 1` when mirrored. The final `-1` follows from integer pixels and exclusive rectangle edges.

For example, local `MM00101.epf` frame 1 has bounds `(25, 19, 76, 40)` in file order. With anchor `(28, 70)`, its 21 by 51 pixel crop starts at `(-9, -45)`. The same local pose in `MW00101.epf` has bounds `(41, 67, 53, 78)` and anchor `(55, 70)`, placing its 11 by 12 crop at `(12, -29)`. These are offsets from one shared origin, not from each other's crop corners. Neither needs an extra hand position or a body-height correction.

### Companion position records

`render_load_human_part_frame` replaces `.epf` with `.tbl` and searches the same selected archive. If found, it reads the four-byte record at `4 * selected_epf_frame`, including the direction-group offset. The record stores horizontal anchor first, then vertical anchor, as two little-endian 16-bit words. See [EPF position companions](../file-formats/epf.md#character-position-companions) for the reader's short-write limitation.

When the table is absent, use the slot defaults above. The inspected split character archives contain no M/W-prefixed `.tbl` entries, so the defaults apply to their current character art. This is a property of this installation, not a reason to discard support for the reader's companion-table path.

The renderer unions the placed, nonempty part rectangles to allocate or refresh its temporary canvas. Keep that union's origin when caching a crop. Replacing it with `(0, 0)` without saving the displacement makes animation frames jump as their bounds change.

## Walking frame selection

`render_human_walk_sequence_ctor` builds one shared descriptor for all 21 categories. Every part uses internal motion 0, variant -1, and a fixed direction stride of five. It does not derive the walk stride from an individual EPF's frame count.

| Stored group | Neutral frame | Four walk poses |
| ---: | ---: | --- |
| 0, left/up | 0 | 1, 2, 3, 4 |
| 1, down/right | 5 | 6, 7, 8, 9 |

This is why matching armor, weapon, shield, and body resources normally have ten frames. Frame 0 or 5 is the neutral fallback, not a fifth walking pose. A resource with fewer frames is not resampled or stretched to fit; the out-of-range image request produces no part.

The same descriptor selects `MM00101`, `MU...01`, `MA...01`, `MW...01`, `MP...01`, `MS...01`, and the matching accessory/head files. Walking does not continue an accessory's `04.epf` idle loop in parallel. Its `01.epf` art supplies the moving pose, using the same index as the body.

Body 5 has two composition exceptions. Main weapon category 8 in motion 0 is forced to absolute EPF frame 0, even after direction selection. When its arms selector is zero, overcoat category 18 in motion 0 instead loads motion 4, the `05.epf` family, retaining the selected frame index. Keep these exceptions separate from the body-5 order table.

## Walk timeline and world displacement

One accepted tile step creates a finite sequence. `world_living_start_move_animation` immediately calls the motion timer handler, selecting the first pose and first accumulated displacement. Each callback then schedules the next one. The last pose is held for one final interval before completion returns the image session to standing.

| Actor and setting | Samples | Interval | Pose sequence | Nominal completion |
| --- | ---: | ---: | --- | ---: |
| Remote human | 4 | 100 ms | 1, 2, 3, 4 | 400 ms |
| Local user, `ScrollLevel = 0` | 4 | 114 ms | 1, 2, 3, 4 | 456 ms |
| Local user, `ScrollLevel != 0` | 8 | 57 ms | 1, 1, 2, 2, 3, 3, 4, 4 | 456 ms |

The poses below are within a stored group. Add five for down/right. Displacement magnitudes are accumulated from the old tile's projected origin; apply direction signs afterward.

| Sample | Four-sample pose | Four-sample `(dx, dy)` | Eight-sample pose | Eight-sample `(dx, dy)` |
| ---: | ---: | --- | ---: | --- |
| 0 | 1 | (6, 3) | 1 | (2, 1) |
| 1 | 2 | (14, 7) | 1 | (6, 3) |
| 2 | 3 | (20, 10) | 2 | (10, 5) |
| 3 | 4 | (28, 14) | 2 | (14, 7) |
| 4 | complete | reset at committed tile | 3 | (16, 8) |
| 5 | | | 3 | (20, 10) |
| 6 | | | 4 | (24, 12) |
| 7 | | | 4 | (28, 14) |
| 8 | | | complete | reset at committed tile |

Sample `k` is nominally selected at `k * interval` after the immediate first callback. For example, local coarse walking selects poses at 0, 114, 228, and 342 ms, then finishes at 456 ms. Local smooth walking selects them at 0, 57, 114, 171, 228, 285, 342, and 399 ms, then finishes at 456 ms.

| Direction | Horizontal sign | Vertical sign |
| --- | ---: | ---: |
| left | +1 | -1 |
| down | +1 | +1 |
| right | -1 | +1 |
| up | -1 | -1 |

These are the client's protocol direction names, not Cartesian left and right arrows. Use the numeric direction mapping at the start of this page.

Move every equipment layer with this one displacement. Then apply the world's tile projection, parent origin, and camera displacement once. Attached world effects inherit their parent's draw origin through world-object collection. Local camera scrolling can keep the player near the same screen location even though its world displacement advances.

The actor owns timer ID `0x02000001`; its callback is `world_living_handle_timer_event`. A revision carried by each timer rejects stale events after a replacement motion. The callback advances one sample, requeues using the sample's interval, and uses 80 ms only if the selected interval is nonpositive. Walking counts callbacks, so delayed dispatch stretches its actual duration. It does not skip to an elapsed-time pose as ordinary spell effects do.

At sequence exhaustion the session starts standing at counter zero and supplies a 300 ms interval. The actor clears its movement offset and commits the staged tile according to its transition policy. See [Movement and swimming](../systems/movement-and-swimming.md#predicted-position-during-a-step) for interruption and replacement behavior, and [Game settings](../systems/game-settings.md#scroll-level-and-movement-timing) for `ScrollLevel`.

## Animated equipment while standing

Normal standing starts with the neutral `01.epf` frame, 0 or 5. For each nonzero part selector, `render_human_stand_initialize_parts` also probes that part's `04.epf`. A file with at least two frames enables an override for that category. With `n = floor(frame_count / 2)`, standing counter `k` selects:

```c
frame = (k % n) + direction_group * n;
```

All enabled parts see the same standing counter, advancing every 300 ms. Each takes its own modulo, so a 16-frame accessory cycles through eight poses per view in 2400 ms while a 24-frame weapon takes 3600 ms. Parts without an override retain their neutral `01.epf` frame. Odd frame counts are rounded down; the leftover final frame is unused by this standing rule. Local resources include both even and odd counts.

Starting walking replaces the standing motion. Returning to standing resets the counter, so an animated accessory begins again at its first standing frame rather than resuming a separate equipment clock. A nonzero rest-position selector uses another descriptor and bypasses this normal standing-resource initialization; do not apply the ordinary idle formula to every resting pose.

## Attached animated effects

Distinguish animated equipment art from an effect created by [`SEffectLayer`](../network/server/041-0x29-effect-layer.md). Equipment is drawn inside the human composite at its category position. A `WorldObject_ObjectEffect` is registered under its target and drawn in world layer 13, after humans in layer 7. It is not inserted between armor and a weapon. Static effects use layer 24, and static map art uses layer 16. The [late translucent local-player replay](walls-and-occlusion.md) is another pass after ordinary layers.

The effect ID selects an `Effect.tbl` frame sequence and an EFA or EPF resource. For numeric effects, resource lookup tries `EfctNNNm.efa`, `EfctNNNb.efa`, `EfctNNN.efa`, then the same three EPF suffixes, where NNN is the internal effect ID plus one. Do not infer body-equipment direction groups from those suffix letters.

An effect's frame pivot and crop position come from [EFA frame geometry](../file-formats/efa.md#frame-position-and-direction), or the EPF frame and its position companion. They are independent of the body's `(28, 70)` anchor. A direction-sensitive EFA can flip in either axis using the target direction captured when the effect is created. That is a different rule from the human part's horizontal-only mirroring.

The effect owns timer ID `0x01000001`. A nonzero resource interval overrides the packet fallback. For a positive effective interval it selects `floor((dispatcher_now - start) / interval)` in `Effect.tbl`, which can skip samples when dispatch is late. A zero interval increments once per callback. The sequence terminator ends an attached effect and detaches it; attached effects are constructed as nonlooping. Movement between two targets has its own path timer and is documented with the packet.

For matching playback, retain separate actor, standing, and effect state. Advancing all visible animation once per video frame or resetting a spell effect whenever the body walks produces different behavior.

## Composition flow

```text
HumanAppearanceRecord
        |
        v
select 21 sprite IDs and palette selectors
        |
        v
choose direction order and one frame per part
        |
        v
draw parts into a temporary human canvas
        |
        v
render_living_object draws the composite into WorldPane
```

Standing motion initializes all 21 resources. A motion update builds the current frame descriptors, caches the selected layers, and advances the animation. The final living-object draw applies the object's normal, highlighted, or translucent world blend to the completed composite.

The shared compositor can load and order as many as 23 part categories. For each active category it builds the asset filename from `HumanState`, reads the selected frame, applies the optional companion position table, resolves a palette, and then draws in direction-specific back-to-front order. Composed results can be retained by `HumanImageCache` for later draws.

Riding previews use a separate path. They select `m_r_###.spf` or `w_r_###.spf`, choose the direction-dependent frame, and draw that single sprite instead of assembling the normal body parts.

This separation is useful for another renderer: first reproduce the appearance record and per-part asset lookup, then reproduce direction grouping and part order, and only then place the completed aisling at its world position.
