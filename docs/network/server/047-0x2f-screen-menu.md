# Screen Menu (`SScreenMenu`)

`SScreenMenu` opens the server-driven merchant, inventory, skill, and spell dialogs. The server chooses both the dialog family and the values that the client later returns in [`CMerchant`](../client/057-0x39-merchant.md).

| Item | Value |
| --- | --- |
| Direction | Server to client |
| Command | `0x2F` (47) |
| Transform | `derived` |
| Name provenance | Microsoft C++ RTTI in the target |
| Main owner | `NPCSession` |

## Common body

```text
packet SScreenMenu {
    u8       opcode                         // 0x2F
    u8       menu_type
    u8       target_type
    u32      target_id
    u8       ignored_unknown
    u16      speaker_sprite
    u8       speaker_color
    bytes    ignored_secondary_group[4]
    u8       show_graphic
    string8  speaker_name
    string16 content

    if menu_type == 0 or menu_type == 1 {
        if menu_type == 1 {
            string8 server_argument
        }
        u8 choice_count
        repeat choice_count {
            string8 choice_text
            u16     pursuit_id
        }
    }

    if menu_type == 2 or menu_type == 3 {
        if menu_type == 3 {
            string8 server_argument
        }
        u16 pursuit_id
    }

    if menu_type == 4 or menu_type == 10 {
        u16 pursuit_id
        u16 item_count
        if pursuit_id != 0x004B {
            repeat item_count {
                u16     sprite
                u8      color
                u32     display_value
                string8 name
                string8 description
            }
        }
        if pursuit_id == 0x004B {
            repeat item_count {
                u32     record_id
                u16     sprite
                u8      color
                u32     price
                u8      available_quantity
                string8 name
                u8      has_description
                if has_description == 1 {
                    string8 description
                }
                u32 progress_current
                u32 progress_limit
            }
        }
    }

    if menu_type == 5 or menu_type == 11 {
        u16 pursuit_id
        u8  slot_count
        repeat slot_count {
            u8 inventory_slot
            if pursuit_id == 0x004E {
                u32 display_value
            }
        }
    }

    if menu_type == 6 or menu_type == 7 {
        u16 pursuit_id
        u16 choice_count
        repeat choice_count {
            u8      graphic_type
            u16     sprite
            u8      color
            string8 name
        }
    }

    if menu_type == 8 or menu_type == 9 {
        u16 pursuit_id
        if bytes_remaining > 0 {
            u8 slot_count
            repeat slot_count {
                u8 book_slot
            }
        }
    }
}
```

All multibyte values are big-endian. The common deserializer deliberately skips `ignored_unknown` and the four-byte secondary group. The 7.41 client neither splits nor uses those bytes.

## Menu types

| Type | Client dialog | Server-supplied tail | Selection returned by `CMerchant` |
| ---: | --- | --- | --- |
| `0` | Text menu | Choice text and a `pursuit_id` per row | Chosen `pursuit_id` |
| `1` | Argumented text menu | Argument, then the type-0 list | Chosen `pursuit_id`, then the same argument |
| `2` | Text input | One `pursuit_id` | `pursuit_id`, then entered text |
| `3` | Argumented text input | Argument and `pursuit_id` | Argument, then entered text |
| `4` | Server item list | Item records | Item name, or the `0x004B` binary selection |
| `5` | Local inventory list | One-based inventory slots | Slot, or the `0x004E` three-byte selection |
| `6` | Server spell choices | Graphic records | Selected name |
| `7` | Server skill choices | Graphic records | Selected name |
| `8` | Local spell book | Optional slot whitelist | Selected book slot |
| `9` | Local skill book | Optional slot whitelist | Selected book slot |
| `10` | Second server item-list mode | Same parser as type 4 | Same forms as type 4 |
| `11` | Second local inventory mode | Same parser as type 5 | Same forms as type 5 |

Types 10 and 11 are handled explicitly by the binary. Their gameplay distinction is not encoded in either local parser, so their friendly names remain unresolved.

A compiled `MerchantDialogPane::FaceMenuDialog` is not another stock menu type. It belongs to an older dormant merchant family, its opener has no recovered reference, and neither the live nor legacy subtype switch assigns it a value. The optional [Appearance editor runtime patch](../../appendix/runtime-patches/appearance-editor.md) reserves type 12 and defines its own shorter body.

For types 8 and 9, an absent or zero slot list means all learned entries in local book slots 1 through 89. A nonzero list restricts the dialog to those server-selected slots.

### Player-owned choices

Types 5, 8, 9, and 11 do not carry complete display records. They tell the client which local inventory, spell-book, or skill-book slots may be selected. The client resolves each slot against current player state and copies the active entry's icon and name into a temporary scrollable NPC list.

Project-owner behavior identifies selling an item and forgetting a skill or spell as gameplay uses. The action itself is not encoded by `menu_type`: the active server conversation and `pursuit_id` give the returned slot its meaning. The local code therefore performs no sellability, forgettability, character-level, learned-level, stat, legend, or `SClass` requirement check. It only requires an active entry in the selected local slot.

The ability rows draw no separate learned-level value, and [`CMerchant`](../client/057-0x39-merchant.md) returns only the one-based book slot. See [Player-owned selection lists](../../systems/npc-dialogs.md#player-owned-selection-lists) for containment, fallback enumeration, and response-pending behavior.

## Item and graphic behavior

The ordinary server-item record displays `display_value` with the item. The client does not prove that every use of this field is a purchase price.

Pursuit ID `0x004B` selects a larger item record and a quantity-aware response. A zero `available_quantity` disables the row, one submits immediately, and a larger value opens a quantity prompt. `progress_current` and `progress_limit` are drawn as `current / limit` when the first value is positive and the limit is not `0xFFFFFFFF`; their game meaning is unresolved.

Pursuit ID `0x004E` selects the taller local-inventory row and adds one displayed `u32` per slot. Its response also changes shape.

Server spell and skill records use these locally confirmed graphic selectors:

| Value | Graphic path |
| ---: | --- |
| `0` | No graphic |
| `1` | Item icon |
| `2` | Spell icon |
| `3` | Skill icon |
| `4` | Monster art |

Other values use the blank or fallback path.

## Example decoded bodies

These examples are complete decoded packet bodies. They do not include the frame header, sequence, trailer, or session-key transform. A server must apply the ordinary derived transform for opcode `0x2F` before framing the packet.

Every example uses target type `1`, target ID `0x12345678`, speaker sprite `0x401E`, speaker name `Guide`, and content `Choose.`. `show_graphic` is zero so the examples do not depend on a matching local illustration. The skipped common-header bytes are also zero.

The response shown after each server body is the meaningful `CMerchant` body before the client applies the dialog-response inner wrapper, derived transform, and frame. The examples select `Buy`, submit `hello`, select the named server record, or select local slot 1 as appropriate.

### Type 0: text menu

```text
2F 00 01 12 34 56 78 00 40 1E 00 00 00 00 00 00
05 47 75 69 64 65 00 07 43 68 6F 6F 73 65 2E 02
03 42 75 79 01 01 05 4C 65 61 76 65 01 02
```

Decoded body length: 46 bytes. Selecting `Buy` returns:

```text
39 01 12 34 56 78 01 01
```

### Type 1: argumented text menu

```text
2F 01 01 12 34 56 78 00 40 1E 00 00 00 00 00 00
05 47 75 69 64 65 00 07 43 68 6F 6F 73 65 2E 05
74 6F 6B 65 6E 02 03 42 75 79 01 01 05 4C 65 61
76 65 01 02
```

Decoded body length: 52 bytes. Selecting `Buy` echoes the opaque argument `token`:

```text
39 01 12 34 56 78 01 01 05 74 6F 6B 65 6E
```

### Type 2: text input

```text
2F 02 01 12 34 56 78 00 40 1E 00 00 00 00 00 00
05 47 75 69 64 65 00 07 43 68 6F 6F 73 65 2E 02
01
```

Decoded body length: 33 bytes. Submitting `hello` returns:

```text
39 01 12 34 56 78 02 01 05 68 65 6C 6C 6F
```

### Type 3: argumented text input

```text
2F 03 01 12 34 56 78 00 40 1E 00 00 00 00 00 00
05 47 75 69 64 65 00 07 43 68 6F 6F 73 65 2E 05
74 6F 6B 65 6E 02 02
```

Decoded body length: 39 bytes. Submitting `hello` echoes `token` first:

```text
39 01 12 34 56 78 02 02 05 74 6F 6B 65 6E 05 68
65 6C 6C 6F
```

### Type 4: ordinary server item

```text
2F 04 01 12 34 56 78 00 40 1E 00 00 00 00 00 00
05 47 75 69 64 65 00 07 43 68 6F 6F 73 65 2E 03
01 00 01 00 01 00 00 00 00 64 06 50 6F 74 69 6F
6E 0B 52 65 73 74 6F 72 65 73 20 48 50
```

Decoded body length: 61 bytes. Selecting `Potion` returns its name:

```text
39 01 12 34 56 78 03 01 06 50 6F 74 69 6F 6E
```

### Type 5: local inventory

```text
2F 05 01 12 34 56 78 00 40 1E 00 00 00 00 00 00
05 47 75 69 64 65 00 07 43 68 6F 6F 73 65 2E 03
02 02 01 02
```

Decoded body length: 36 bytes. Selecting inventory slot 1 returns:

```text
39 01 12 34 56 78 03 02 01
```

The row appears only when the client currently has an active item in that slot.

### Type 6: server spell

```text
2F 06 01 12 34 56 78 00 40 1E 00 00 00 00 00 00
05 47 75 69 64 65 00 07 43 68 6F 6F 73 65 2E 04
01 00 01 02 00 01 00 04 48 65 61 6C
```

Decoded body length: 44 bytes. Selecting `Heal` returns:

```text
39 01 12 34 56 78 04 01 04 48 65 61 6C
```

### Type 7: server skill

```text
2F 07 01 12 34 56 78 00 40 1E 00 00 00 00 00 00
05 47 75 69 64 65 00 07 43 68 6F 6F 73 65 2E 04
02 00 01 03 00 01 00 06 41 73 73 61 69 6C
```

Decoded body length: 46 bytes. Selecting `Assail` returns:

```text
39 01 12 34 56 78 04 02 06 41 73 73 61 69 6C
```

### Type 8: local spell book

```text
2F 08 01 12 34 56 78 00 40 1E 00 00 00 00 00 00
05 47 75 69 64 65 00 07 43 68 6F 6F 73 65 2E 04
03 02 01 02
```

Decoded body length: 36 bytes. Selecting spell-book slot 1 returns:

```text
39 01 12 34 56 78 04 03 01
```

The row appears only when that client slot contains a learned spell.

### Type 9: local skill book

```text
2F 09 01 12 34 56 78 00 40 1E 00 00 00 00 00 00
05 47 75 69 64 65 00 07 43 68 6F 6F 73 65 2E 04
04 02 01 02
```

Decoded body length: 36 bytes. Selecting skill-book slot 1 returns:

```text
39 01 12 34 56 78 04 04 01
```

The row appears only when that client slot contains a learned skill.

### Type 10: quantity-aware server item

This example uses special pursuit ID `0x004B`, one record with ID `0x01020304`, and an available quantity of 5.

```text
2F 0A 01 12 34 56 78 00 40 1E 00 00 00 00 00 00
05 47 75 69 64 65 00 07 43 68 6F 6F 73 65 2E 00
4B 00 01 01 02 03 04 00 01 00 00 00 00 64 05 06
50 6F 74 69 6F 6E 01 0B 52 65 73 74 6F 72 65 73
20 48 50 00 00 00 00 FF FF FF FF
```

Decoded body length: 75 bytes. Selecting quantity 2 returns:

```text
39 01 12 34 56 78 00 4B 01 01 02 03 04 02
```

Types 4 and 10 can both use the ordinary or `0x004B` item layout. The examples show one form of each.

### Type 11: valued local inventory

This example uses special pursuit ID `0x004E`, slot 1, and display value 100.

```text
2F 0B 01 12 34 56 78 00 40 1E 00 00 00 00 00 00
05 47 75 69 64 65 00 07 43 68 6F 6F 73 65 2E 00
4E 01 01 00 00 00 64
```

Decoded body length: 39 bytes. Selecting slot 1 returns:

```text
39 01 12 34 56 78 00 4E 01 01 01
```

Types 5 and 11 can both use the ordinary or `0x004E` local-inventory layout. The examples show one form of each.

## UI flow

`net_deserialize_screen_menu_server_packet` reads the common fields and keeps the remaining bytes in an owned reader. `ui_npc_session_open_screen_menu` copies the packet state into `NPCSession`, refreshes the speaker art, and creates the exact RTTI class `NPC_Merchant_MessageDialog`. `ui_npc_dispatch_screen_menu_type` then constructs the subtype-specific model and controls.

The dialog uses `lnpcd.txt` for the speaker name, content, scrolling, top, and close controls. Generic nested menus, including the player-owned lists, use `lnpcd2.txt`. Server-item types 4 and 10 use the larger `lnpcd3.txt` item layout. Input is ordinary `DialogPane` input: child hit testing turns clicks into attachment-order actions, the focused text control receives keyboard and IME events, and Tab moves focus.

The outer merchant pane attaches Top as action 4 and Close as action 5. Top sends [`CRequestObjectInfo`](../client/067-0x43-request-object-info.md) subtype 1 with this screen menu's `target_id`, then closes the NPC session. Close only closes locally. Neither outer action sends `CMerchant`.

See [NPC dialogs](../../systems/npc-dialogs.md) for the pane tree, control order, layouts, and full response flow. Speaker illustration lookup is described in [NPC dialog illustrations](../../systems/npc-dialog-illustrations.md).

## Client quirks and limits

- For a type-0 or type-1 list with exactly two choices, the client hides the second row when `target_type` is greater than `0x0C`. The reason is unresolved.
- Local inventory rows are resolved against current client inventory state. Inactive slots are omitted.
- Values outside 0 through 11 do not construct a known subtype model in the recovered dispatcher.
- The subtype parsers generally trust server counts and lengths. This page documents accepted structure, not safe server-side limits.
