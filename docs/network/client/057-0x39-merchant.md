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

Project-owner behavior identifies local selling and ability-forgetting conversations as uses of the player-owned selection families. The packet does not label either action and does not include the item's properties, ability name, or learned level. It returns the chosen local slot, while the active `SScreenMenu` conversation and `pursuit_id` tell the server how to interpret it. See [Player-owned selection lists](../../systems/npc-dialogs.md#player-owned-selection-lists).

Argumented menus treat `server_argument` as opaque. The client does not display or reinterpret it; it returns the same bytes when the user submits.

Every confirmed nested-menu submitter asks `NPCSession` to enter response-pending after queuing `CMerchant`. This deactivates the current nested menu. A continuing interaction needs another server packet to refresh the session and pane.

For supplied choices or text, call the current response model's subtype-specific native producer instead of constructing this contextual body directly. The model resolves a displayed row to its retained pursuit value, name, record ID, or local slot and preserves the optional server argument. See [Invoking an NPC response](../../systems/npc-dialogs.md#invoking-a-response-without-pointer-input).

### Categorized item activation

The active `NPCServerItemMenuDialog` handles category and item-page changes locally. A single left click selects an item. Double clicking it or pressing the activation button resolves the selected visible entry back to its original `u16` model row and calls `net_send_merchant_server_item_selection`, after a quantity prompt when required. See [From an item click to a packet](../../systems/npc-dialogs.md#from-an-item-click-to-a-packet).

For an ordinary server-item menu, the complete meaningful plaintext is:

```text
packet CMerchant {
    u8      opcode                     // 0x39
    u8      target_type
    u32     target_id
    u16     pursuit_id                 // not 0x004B
    string8 selected_item_name
}
```

Its builder length is `9 + name_byte_count`. The name comes from the selected retained server record, not from a category label or a new inventory lookup. An ordinary item response contains no quantity field.

For pursuit `0x004B`, the complete meaningful plaintext is 14 bytes:

```text
packet CMerchant {
    u8  opcode                         // 0x39
    u8  target_type
    u32 target_id
    u16 pursuit_id                     // 0x004B
    u8  marker                         // literal 1
    u32 record_id
    u8  quantity
}
```

The builder takes `record_id` from the selected model row. It does not send the item name, displayed price, category, page, or row index in this form. The target fields come from the current `NPCSession`, and the pursuit comes from the current model. The server's conversation gives the selection its banking or shop meaning.

For programmatic observation, the input to `net_submit_client_packet` is the useful boundary for copying these meaningful fields. The outgoing network bytes have additional protection: submission applies the dialog-response inner wrapper and queues communications command `6`; `net_send_client_packet` takes the `derived` branch for opcode `0x39`, then builds the binary TCP frame as `0xAA`, a big-endian transformed-body length, and the transformed body before calling Winsock `send`. The negotiated printable-framing alternative is described in [Transport](../transport.md). The body schemas above are not already-encrypted wire bytes.

The selection builder enters response-pending after submission. That is a local state transition, not proof that the server accepted the item action. This trace is confirmed from the matching binary; a particular bank's target, pursuit, selected name or record ID, and resulting server response require that live conversation.

## UI producers

The current `NPCSession` family has separate builders for text menus, input, server items, local inventory, server skill/spell records, and local books. An older compiled `MerchantDialogPane` family produces the same normal, argumented, item-name, `0x004B`, and `0x004E` forms. This agreement is useful confirmation that they are protocol variants rather than accidental object layouts.

The exact RTTI class `MerchantDialogPane::FaceMenuDialog` emits a distinct nine-byte appearance form:

```text
record merchant_face_menu_body {
    u8  opcode                         // 0x39
    u8  target_type
    u32 target_id
    u8  hair_style
    u8  gender                         // 1 male, 2 female
    u8  hair_color
}
```

Its action handler lets the player adjust gender, hair style, hair color, and a preview-only direction. Submission truncates the first three results to the bytes above and does not send the direction. The matching opener and the older raw merchant entry are both unreferenced in version 741, so no stock `SScreenMenu` parameter selects this form. The optional [Appearance editor runtime patch](../../appendix/runtime-patches/appearance-editor.md) supplies a private activation path and sample exchange. This body must not be parsed as the normal `u16 pursuit_id` header.

## Inner wrapper

Before the ordinary `derived` transform, `net_submit_client_packet` replaces the body with the random-header, CRC16, and incrementing-XOR wrapper shared only with `CPursuit`. The CRC covers the original bytes after the opcode. See [Dialog-response inner wrapper](../packet-transforms.md#dialog-response-inner-wrapper) for the exact byte layout.

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
