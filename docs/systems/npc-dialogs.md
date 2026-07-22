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

### Older `MerchantSession` path

The executable also retains an older full-screen `MerchantSession` implementation for the same `SScreenMenu` opcode `0x2F`. `net_handle_screen_menu_raw` constructs this pane directly from the decoded body. The session owns two nested dialog slots and `ui_merchant_session_dispatch_screen_menu` maps subtype values 0 through 11 to its compiled text, input, item, skill, and spell dialog families. A body beginning with opcode `0x30` closes the whole merchant session.

This path uses `lmerc.txt` for segmented menus, `lmerd.txt` for detail panes, and the dormant `lmerc2.txt` item-list variant. The layouts are loaded together, but `ui_is_server_item_menu_dialog3_enabled` always returns false in this build, so the newer `ServerItemMenuDialog3` branch is never selected.

The nested classes share `MerchantDialogPane`. Its common header contains target type, target ID, pursuit ID, content text, and seller text. A derived dialog may opt into one more trailing string. The base centers each pane, carries the owning session, sends target-information requests, and updates a shared screen origin while the player drags the dialog. Detail-style panes draw the fixed `lmerd` background; other styles can build a scalable frame from tiled 16-pixel edges and four corners.

The older subtype factory uses these exact RTTI classes:

| Types | Compiled dialog |
| --- | --- |
| `0` | `TextMenuDialog`, or `TextMenuDialogEx` above eight rows |
| `1` | `ArgumentedTextMenuDialog`, or `ArgumentedTextMenuDialogEx` above eight rows |
| `2` | `TextInputMenuDialog` |
| `3` | `ArgumentedTextInputMenuDialog` |
| `4`, `10` | `ServerItemMenuDialog` because the newer dialog is disabled |
| `5`, `11` | `ClientItemMenuDialog` |
| `6` | `ServerSpellMenuDialog` |
| `7` | `ServerSkillMenuDialog` |
| `8` | `ClientSpellMenuDialog` |
| `9` | `ClientSkillMenuDialog` |

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

The server-item family has a zero-delay queued hover path into the shared `DescPane`. The local-inventory list is a different control family and should not be assumed to use the same producer. See [Item and ability descriptions](item-and-ability-descriptions.md) for the confirmed paths and remaining shop and bank mapping limit.

### Player-owned selection lists

Some screen menus ask the player to choose from state the client already owns instead of drawing records supplied by the server. Project-owner behavior identifies selling an item and forgetting a skill or spell as uses of these pickers. Those action names belong to the active NPC conversation. The client has no `sell` or `forget` mode enum here, so the same picker can support another server-defined action.

| Type | Local source | Server restriction | Row and response |
| ---: | --- | --- | --- |
| `5`, `11` | Inventory | Required list of one-based slots | Local item icon and name; returns the inventory slot |
| `8` | Spell book | Optional list of one-based slots | Local spell icon and name; returns the spell slot |
| `9` | Skill book | Optional list of one-based slots | Local skill icon and name; returns the skill slot |

The outer `NPC_Merchant_MessageDialog` contains an `NPCListMenuDialog` for these modes. The nested pane uses the generic `lnpcd2.txt` geometry and contains a scrollable row list plus a separate default submit button. Selecting a row does not replace the normal player inventory or book pane. It selects a row in this temporary NPC-owned list.

`NPCClientItemMenu` receives an exact slot list from the packet. `ui_npc_client_item_menu_build_row` resolves each slot through the live inventory interface when the dialog is built. Only an active local item becomes a row. The row copies the local icon and name. Pursuit `0x004E` also draws the server's extra `u32` value and returns the special `1, slot, 1` response form. A zero item count produces an empty list.

`NPCClientSpellMenu` and `NPCClientSkillMenu` resolve the supplied slots through the live spell or skill book. A nonzero whitelist limits the candidates to those slots. If the list is absent or has count zero, the client scans slots 1 through 89 and collects every active learned entry. Spell rows use the spell icon bank; skill rows use the skill icon bank. Both show the retained ability name.

These row builders check only that the local slot currently contains an active item, spell, or skill. They do not apply `SClass` learnability requirements, inspect legend entries, compare stats, or perform a sellable or forgettable check. No separate learned-level field is drawn or returned. The server receives only the selected one-based slot through [`CMerchant`](../network/client/057-0x39-merchant.md) and decides whether the conversation action succeeds.

After submission, the nested menu enters response-pending and stops accepting another choice. The outer Close action still closes locally without sending `CMerchant`.

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

The constructor also registers action 6 as the dialog's cancel action. The inherited keyboard handler dispatches Escape through that action. Nested `NPCMenuDialog` panes return false for Escape instead of consuming it, so the event reaches the outer pursuit pane. The visible Close button and Escape therefore use the same `net_send_pursuit_close_current` path.

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

After queuing a navigation or answer, the client calls `ui_npc_session_set_response_pending`. The pursuit implementation deactivates the nested answer pane, disables Previous and Next, and clears the default action. It leaves Close available. The server continues by sending the next `SPursuitMessage`, which refreshes the session and pane. A type-10 message closes the session.

Close is different from an ordinary answer. Action 6 queues a ten-byte, no-argument `CPursuit` for the current step and then closes the NPC session locally.

Simple question and text modes also send `CSay` before their pursuit answer. The speech echo is an additional server-visible action, not a replacement for `CPursuit`.

See [`SPursuitMessage`](../network/server/048-0x30-pursuit-message.md) and [`CPursuit`](../network/client/058-0x3a-pursuit.md).

## Stale pursuit recovery

The project owner reports that a timed reactor can expire while its pursuit dialog is open. If the player answers afterward, the server can ignore the answer and later reject other actions with a "You're stuck" message. The client has no target-lifetime check. It only enters response-pending and waits for another `SPursuitMessage`.

The normal recovery already exists while the live pursuit pane receives input. Close or Escape sends the current-step `CPursuit` before closing locally. If that packet is absent in a reproduction, log these four points in order:

1. `ui_npc_pursuit_message_handle_action` receives action 6.
2. `net_send_pursuit_close_current` runs.
3. `net_submit_client_packet` receives an opcode-`0x3A`, ten-byte body.
4. The communications worker emits the wrapped and transformed packet.

This separates an input-routing failure from a builder, queue, or transport failure.

An injected fallback should recover only a known pending pursuit:

```text
on SPursuitMessage type != 10: cache target_type, target_id, pursuit_id, step_id
on non-close CPursuit:         arm this context as response-pending
on another SPursuitMessage:    update or clear the pending context
on map, session, or connection reset: clear the pending context

on Escape while pending and no native close was queued:
    queue the cached ten-byte close body on the main-thread dispatcher
```

The documented [Stale pursuit runtime patch](../appendix/runtime-patches/stale-pursuit.md) implements this boundary for version 741. It clears its pending marker on the native Close path or the next incoming pursuit message, keeps the full `u32 target_id`, and expires the patch-owned context after 30 seconds. After submitting the real Close, the fallback also passes decoded body `30 0A` to `net_post_decoded_server_packet_event` so the ordinary typed-packet and pane path clears client-side pursuit state.

Do not send a close automatically after a fixed timeout alone. A valid script may answer slowly or finish through another server message. A captured `SMessage` carrying the exact stuck response could become a stronger optional trigger, but its type and text bytes must be confirmed first.

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
