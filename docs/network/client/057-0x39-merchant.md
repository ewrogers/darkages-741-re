# Merchant (`CMerchant`)

`CMerchant` returns a choice, text value, inventory slot, or item record from an [`SScreenMenu`](../server/047-0x2f-screen-menu.md) dialog. Normal screen-menu responses begin with an eight-byte target and pursuit header; the dialog subtype decides the optional tail. A separate compiled face-menu form is documented below.

| Item | Value |
| --- | --- |
| Direction | Client to server |
| Command | `0x39` (57) |
| Transform | Dialog-response inner wrapper, then `derived` |
| Name provenance | Project-owner protocol vocabulary; behavior confirmed by local UI builders and RTTI |

The client has no derived packet RTTI class for `CMerchant`.

## Common body

```text
packet CMerchant {
    u8  opcode                         // 0x39
    u8  target_type
    u32 target_id
    u16 pursuit_id
    bytes response[remaining]
}
```

All multibyte values are big-endian. `net_build_merchant_response_header` writes the eight-byte common body. The optional response is contextual because `CMerchant` does not repeat `SScreenMenu.menu_type`.

`target_type` and `target_id` echo the server values. `pursuit_id` is either the value attached to the chosen text row or the single value supplied before another menu's records.

## Response variants

| Source screen-menu type | Response bytes after `pursuit_id` |
| --- | --- |
| `0` text menu | None |
| `1` argumented text menu | `string8 server_argument` |
| `2` text input | `string8 entered_text` |
| `3` argumented text input | `string8 server_argument`, then `string8 entered_text` |
| `4` or `10`, ordinary server item | `string8 selected_item_name` |
| `4` or `10`, pursuit `0x004B` | `u8 1`, `u32 record_id`, `u8 quantity` |
| `5` or `11`, ordinary local item | `u8 inventory_slot` |
| `5` or `11`, pursuit `0x004E` | `u8 1`, `u8 inventory_slot`, `u8 1` |
| `6` or `7`, server skill/spell | `string8 selected_name` |
| `8` or `9`, local skill/spell | `u8 book_slot` |

The two fixed `1` bytes in the `0x004E` form are literal client constants. Their meanings are unresolved. Inventory and book slots are one-based.

Argumented menus treat `server_argument` as opaque. The client does not display or reinterpret it; it returns the same bytes when the user submits.

Every confirmed nested-menu submitter asks `NPCSession` to close the active dialog immediately after queuing `CMerchant`. A continuing interaction therefore needs another server packet to construct the next pane.

## UI producers

The current `NPCSession` family has separate builders for text menus, input, server items, local inventory, server skill/spell records, and local books. An older compiled `MerchantDialogPane` family produces the same normal, argumented, item-name, `0x004B`, and `0x004E` forms. This agreement is useful confirmation that they are protocol variants rather than accidental object layouts.

The exact RTTI class `MerchantDialogPane::FaceMenuDialog` emits a distinct nine-byte form:

```text
record merchant_face_menu_body {
    u8  opcode                         // 0x39
    u8  target_type
    u32 target_id
    u8  selector_b
    u8  selector_a_class              // 1 if selector A is zero, otherwise 2
    u8  selector_c
}
```

Its action handler lets the player adjust three word-sized selectors and a fourth visual value in five-step increments. Submission truncates three selector results to the bytes above and does not send the fourth value. The live server trigger and gameplay meanings have not been established. This body must not be parsed as the normal `u16 pursuit_id` header.

## Inner wrapper

Before the ordinary session-key transform, `net_submit_client_packet` replaces the body with the random-header, CRC16, and incrementing-XOR wrapper shared only with `CPursuit`. The CRC covers the original bytes after the opcode. See [Dialog-response inner wrapper](../packet-transforms.md#dialog-response-inner-wrapper) for the exact byte layout.

The order is important:

```text
CMerchant body
    -> dialog-response inner wrapper
    -> normal derived transform for opcode 0x39
    -> frame
```

## Paired packet and UI

The server creates every confirmed normal variant with [`SScreenMenu`](../server/047-0x2f-screen-menu.md). [NPC dialogs](../../systems/npc-dialogs.md) maps each server subtype to its controls and submitter.

The outer pane's Close action does not send `CMerchant`. Its Top action sends [`CRequestObjectInfo`](067-0x43-request-object-info.md) subtype 1 with the target ID and then closes the NPC session.

## Known limits

- The local target field is passed through as a byte. A complete 7.41 target-type enum remains unresolved.
- The client does not attach a generic action code. Servers must interpret the response from the active dialog and its `pursuit_id`.
- The compiled face-menu form is documented separately because its first eight bytes only superficially resemble the common form.
