# NPC dialogs

NPC conversations are a server-driven UI system with two related protocols. A screen menu asks for one merchant-style value. A pursuit message represents one step in a navigable conversation. Both enter `NPCSession`, create ordinary client panes, and return a specialized packet when the player acts.

## Mental model

```text
screen-menu exchange
    server SScreenMenu 0x2F
        -> NPCSession state 1
        -> merchant message pane plus subtype controls
        -> player selects or enters a value
        -> client CMerchant 0x39

pursuit exchange
    server SPursuitMessage 0x30
        -> NPCSession state 2
        -> pursuit message pane plus optional question/input controls
        -> player navigates, selects, enters text, or closes
        -> client CPursuit 0x3A
        -> server sends the requested step or close type 10
```

The server supplies data, not a serialized pane tree. The client chooses a compiled dialog class for the packet type, loads named geometry from its layout files, attaches controls in a fixed order, and binds each control action to a packet builder.

## Entry through `NPCSession`

`ui_npc_session_handle_network_event` recognizes the exact RTTI packet classes `SScreenMenu` and `SPursuitMessage`.

For `SScreenMenu`, `ui_npc_session_open_screen_menu` copies the common fields into the session, sets state 1, refreshes speaker art, and constructs `NPC_Merchant_MessageDialog`.

For `SPursuitMessage`, `ui_npc_session_open_pursuit_message` handles type 10 as an immediate close. Other types are copied into session state 2. Type 6 skips the normal speaker-art refresh; the other types refresh it before constructing `NPC_Pursuit_MessageDialog`.

The stored session state lets the outer pane and the nested answer model read the same target ID, speaker presentation, pursuit ID, and current step without retaining the server packet object.

### Target identity

Both protocols carry `target_type` and `target_id`, and both client responses echo them. The local dialog builders do not decode that byte, and the screen-menu code contains a separate `target_type > 0x0C` behavior. A complete 7.41 target-type enum remains unresolved.

## Pane composition

The two protocols share an outer message pane and add a nested control pane only when needed:

```text
NPCMessageDialog
    speaker name
    formatted content
    content up/down
    protocol-specific navigation or close buttons

    optional NPCMenuDialog
        text-choice buttons
        or text input
        or item rows and details
        or skill/spell rows
        or protected account fields
```

`NPCMessageDialog` uses `lnpcd.txt`. It is a `DialogPane`, so the controls are real event targets rather than text drawn directly into the outer pane.

### Screen-menu classes

`ui_npc_dispatch_screen_menu_type` chooses these locally recovered models:

| Types | Model | Visible control family |
| --- | --- | --- |
| `0`, `1` | `NPC_Merchant_TextMenu` | `NPCTextMenuDialog` |
| `2`, `3` | `NPC_Merchant_TextInputMenu` | `NPCTextInputMenuDialog` |
| `4`, `10` | `NPCServerItemMenu` | `NPCServerItemMenuDialog` |
| `5`, `11` | `NPCClientItemMenu` | Local-inventory list |
| `6`, `7` | `NPCServerSkillSpellMenu` | `NPCListMenuDialog` |
| `8` | `NPCClientSpellMenu` | Local spell list |
| `9` | `NPCClientSkillMenu` | Local skill list |

The type model parses the remaining packet bytes. The visible dialog then builds rows or controls from that model. This is why the common server-packet deserializer can keep the subtype tail opaque.

### Pursuit classes

The outer exact class is `NPC_Pursuit_MessageDialog`. `ui_npc_pursuit_build_subtype` adds one of these answer models:

| Type | Exact class | Nested pane |
| ---: | --- | --- |
| `2` | `NPC_Pursuit_MenuQuestionMessage` | Text menu |
| `3` | `NPC_Pursuit_SimpleMenuQuestionMessage` | Text menu |
| `4` | `NPC_Pursuit_TextMessage` | Text input |
| `5` | `NPC_Pursuit_SimpleTextMessage` | Text input |
| `6` | `NPC_Pursuit_QuestionMessageFace` | Text menu |
| `9` | `NPC_Pursuit_NexonclubIdTextMessage` | Protected ID/password input and manager-gated result |

Types 0 and 1 need no nested answer pane. Type 10 closes the active NPC UI before a new pane is constructed.

## Layout contracts

The layouts are skin and geometry contracts. Their `NAME` fields must match the constructor's lookups.

| File | Controls | Main named regions used by this system |
| --- | ---: | --- |
| `lnpcd.txt` | 13 | `MessageDialog`, `NPCTile`, `MenuDialog`, `Name`, `Text`, `UpArrow`, `DownArrow`, `PrevBtn`, `NextBtn`, `TopBtn`, `CloseBtn` |
| `lnpcd2.txt` | 9 | `Content`, `TextMenu`, `TextMenuButton`, `TextMenuMin`, `TextInputContent`, `ExtraStatic`, `Text`, `Btn1` |
| `lnpcd3.txt` | 18 | `Tab0`, `Tab1`, tab paging, item icons and names, class/level/weight/description, money, page controls |
| `lnpcd4.txt` | 6 | `Content`, `Prolog`, `TextInput`, `Epilog`, `Btn1` |
| `lnpcnid.txt` | 10 | `Content`, `Prolog`, `Id`, masked `Password`, `Epilog`, `Btn1`, `Btn2` |

`lnpcd3.txt` supports category tabs, four visible item buttons, detail fields, paging, and a money display. It is more than a generic one-column list.

## Pointer, keyboard, and focus input

These dialogs use the normal `DialogPane` machinery:

1. Pointer input walks attached controls and tests their rectangles.
2. A hit is converted to control-local coordinates and dispatched to that child.
3. A completed control action returns its attachment-order index to the dialog handler.
4. A true return consumes the event and stops lower panes from receiving it.

Keyboard and IME events go to the focused edit control. Tab and reverse-Tab use the inherited wrapping focus traversal and skip controls that are disabled or not focusable.

For `NPC_Pursuit_MessageDialog`, outer action IDs 4, 5, and 6 are Previous, Next, and Close. IDs 0 through 3 belong to the base message controls. The menu row handler converts a zero-based control index to the one-based choice number sent on the wire.

For `NPC_Merchant_MessageDialog`, action 4 is Top and action 5 is Close. Top sends `CRequestObjectInfo` subtype 1 with the active target ID and then closes the NPC session. Close sends no packet. Only a nested menu selection or submission produces `CMerchant`.

The protected type-9 dialog has separate ID and masked-password edit controls. Its submit handler first calls the regional account manager and may wait, show a local error, or continue. Only the accepted state sends `CPursuit`, using a manager-produced nonempty result string. The two visible input buffers are not copied directly into the packet builder.

## Server and client round trips

### Screen menu

The server's `menu_type` determines how the response is interpreted. Text choices return their attached `pursuit_id`; input returns entered bytes; server records return a name or record ID; local lists return a slot. The server must remember the active menu because `CMerchant` does not echo `menu_type`.

The special item pursuits are part of the same flow:

- `0x004B` uses record IDs and a player-selected quantity.
- `0x004E` uses a three-byte local-slot response with literal marker bytes.

See [`SScreenMenu`](../network/server/047-0x2f-screen-menu.md) and [`CMerchant`](../network/client/057-0x39-merchant.md) for every body variant.

### Pursuit

The pursuit pane treats the server's `step_id` as the current page. Previous sends current minus one; Next and answers send current plus one; Close returns the current step. Menu and text arguments are explicitly tagged in `CPursuit`.

All confirmed merchant submissions and pursuit actions invoke `ui_npc_session_close_active_dialog` after queuing their response. The server does not mutate controls in place to continue. It sends the next `SScreenMenu` or `SPursuitMessage`, and `NPCSession` builds the next pane from that message.

Simple question and text modes also send `CSay` before their pursuit answer. The speech echo is an additional server-visible action, not a replacement for `CPursuit`.

See [`SPursuitMessage`](../network/server/048-0x30-pursuit-message.md) and [`CPursuit`](../network/client/058-0x3a-pursuit.md).

## Special response protection

`CMerchant` and `CPursuit` are the only client opcodes that enter the dialog-response inner-wrapper branch. That layer adds two random bytes, an encoded length, CRC16 over the original bytes after the opcode, an incrementing XOR, and a terminating zero. The result then enters the normal outer transform selected independently for each opcode.

This protection belongs to packet submission, not to any pane. New controls can safely reuse an existing client builder, but an external implementation must reproduce both layers. See [Packet transforms](../network/packet-transforms.md#dialog-response-inner-wrapper).

## Speaker presentation

The common server fields include a sprite, color, `show_graphic`, and speaker name. `NPCSession` can replace the small NPC tile with a large local illustration selected by the name. The art lookup and fallback are documented separately in [NPC dialog illustrations](npc-dialog-illustrations.md).

## Alternate compiled family

The executable also contains an older or parallel merchant and pursuit dialog family. Its exact RTTI includes `MerchantDialogPane::TextMenuDialogEx`, `MerchantDialogPane::FaceMenuDialog`, `QuestionMessageDialog`, `QuestionMessageFaceDialog`, `SimpleQuestionMessageDialog`, `TextMessageDialog`, and `SimpleTextMessageDialog`.

Its packet builders independently confirm the common headers, argument tags, step arithmetic, speech echoes, and special merchant tails. A complete live entry from the current `NPCSession` route to this family has not been established. It is evidence for the wire format, but not proof that every class is reachable in normal 7.41 play.

`FaceMenuDialog` is the exception to the normal merchant header. It sends target type and ID followed by three selector bytes, with no `u16 pursuit_id`. Its compiled action handler proves the body shape, but its server trigger and selector meanings remain unresolved.

## Extension points

The cleanest ways to extend the UI depend on the desired change:

- Reskinning, spacing, and repositioning can change the five layout files without changing packet behavior, as long as required control names remain present.
- Additional display-only information can be drawn while building an existing row.
- A new interactive action requires a control to be constructed, attached, handled by its attachment-order ID, and cleaned up with the pane.
- A new answer form should feed an existing `CMerchant` or `CPursuit` builder when its wire contract matches. Calling the general packet sender with only the plaintext body is sufficient inside the client because submission applies the inner wrapper automatically.

The subtype parsers trust many server-controlled counts and lengths. Extensions should preserve the existing bounded text controls and validate new data before constructing rows.
