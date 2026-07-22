# Player rendering

An aisling is drawn as one temporary composite image made from as many as 21 body and equipment parts. The world renderer does not draw armor, hair, and weapons as independent world objects. `HumanObjectImageSession` selects their frames, palettes, and order, builds the composite, and `render_living_object` places that result into the world.

Both the local character and other visible users use this path. Their appearance normally comes from [`SDrawHumanObjects`](../network/server/051-0x33-draw-human-objects.md). A head sprite of `0xFFFF` selects the separate monster-disguise path.

## Two stored views and four directions

The client stores two directional frame groups per human-part motion. It mirrors each group to obtain the paired direction.

| Direction | Value | Stored frame group | Mirror horizontally |
| --- | ---: | ---: | --- |
| left | 0 | 0 | no |
| down | 1 | 1 | no |
| right | 2 | 1 | yes |
| up | 3 | 0 | yes |

This is close to a front-and-back model, but the safest description is two isometric direction groups. Left and up share one group. Down and right share the other.

Each part motion divides its frames equally between the two groups:

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

This makes the observed unarmored ghost appearance data-driven. The server can send zero armor and equipment selectors with the Ghost body, and zero selectors produce no part resources. A missing compatible frame in the private art could also omit a visual layer, but the required assets are not present here to test that possibility. The client code itself does not silently clear armor because `MaleGhost` or `FemaleGhost` was selected.

## Part categories

`render_select_human_part_sprite` resolves these 21 categories. Some equipment has two draw categories because it can contribute a front and a rear layer.

| Category | Part | Important rule |
| ---: | --- | --- |
| 0 | shield | Uses the male resource prefix |
| 1 | body | Supplies the base body |
| 2 | pants | Suppressed when an overcoat is present |
| 3 | boots | Uses the boots color |
| 4 | head or hair | Uses the hair color |
| 5 | armor | Suppressed when an overcoat is present |
| 6 | internal clothing layer | Source field is zero in `SDrawHumanObjects` |
| 7 | arms | Suppressed when an overcoat is present |
| 8 | weapon | Main weapon layer |
| 9, 10 | accessory 1 | Uses accessory 1 color |
| 11, 12 | accessory 2 | Uses accessory 2 color |
| 13, 14 | accessory 3 | Uses accessory 3 color |
| 15 | weapon | Alternate weapon layer |
| 16, 17 | head or hair | Alternate head layers, using hair color |
| 18, 19 | overcoat | Uses overcoat color |
| 20 | face | Uses the skin palette |

Body sprites 1 and 5 in category 1, plus the face in category 20, use the selected skin palette directly. Hair, boots, pants, accessories, and overcoat use their corresponding color selectors. The armor palette selector comes from the internal record field at `+0x16`; this packet path sets it to zero.

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

The motion number written to the filename is the internal motion plus one. A second branch appends a lowercase alphabetic variant. A few categories force special prefixes or sprite choices, including shields, certain weapons, and one head case. Body 5 uses the `MM005` or `WM005` motion family.

## Back-to-front part order

The renderer does not use one universal equipment order. It selects a 21-entry category list from the direction and body, then draws from the start of that list to the end.

| Case | Back-to-front category order |
| --- | --- |
| left or up | `0, 10, 12, 14, 1, 20, 2, 3, 5, 18, 6, 17, 8, 7, 19, 4, 16, 15, 9, 11, 13` |
| down or right | `17, 10, 12, 14, 1, 20, 2, 3, 4, 5, 18, 6, 8, 7, 19, 16, 15, 0, 9, 11, 13` |
| body 5, down or right | `17, 10, 12, 14, 8, 1, 20, 2, 3, 4, 5, 18, 6, 7, 19, 16, 15, 0, 9, 11, 13` |

The body-5 list moves the main weapon behind the body for down and right. The client contains a separately selected alternate table, but its bytes are identical to the default table in version 741.

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
