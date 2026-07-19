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

For types 8 and 9, an absent or zero slot list means all learned entries in local book slots 1 through 89. A nonzero list restricts the dialog to those server-selected slots.

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

## UI flow

`net_deserialize_screen_menu_server_packet` reads the common fields and keeps the remaining bytes in an owned reader. `ui_npc_session_open_screen_menu` copies the packet state into `NPCSession`, refreshes the speaker art, and creates the exact RTTI class `NPC_Merchant_MessageDialog`. `ui_npc_dispatch_screen_menu_type` then constructs the subtype-specific model and controls.

The dialog uses `lnpcd.txt` for the speaker name, content, scrolling, top, and close controls. Its nested menu uses `lnpcd2.txt`; item lists use `lnpcd3.txt`. Input is ordinary `DialogPane` input: child hit testing turns clicks into attachment-order actions, the focused text control receives keyboard and IME events, and Tab moves focus.

The outer merchant pane attaches Top as action 4 and Close as action 5. Top sends [`CRequestObjectInfo`](../client/067-0x43-request-object-info.md) subtype 1 with this screen menu's `target_id`, then closes the NPC session. Close only closes locally. Neither outer action sends `CMerchant`.

See [NPC dialogs](../../systems/npc-dialogs.md) for the pane tree, control order, layouts, and full response flow. Speaker illustration lookup is described in [NPC dialog illustrations](../../systems/npc-dialog-illustrations.md).

## Client quirks and limits

- For a type-0 or type-1 list with exactly two choices, the client hides the second row when `target_type` is greater than `0x0C`. The reason is unresolved.
- Local inventory rows are resolved against current client inventory state. Inactive slots are omitted.
- Values outside 0 through 11 do not construct a known subtype model in the recovered dispatcher.
- The subtype parsers generally trust server counts and lengths. This page documents accepted structure, not safe server-side limits.
