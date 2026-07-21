# Packet interaction flows

Many game actions are conversations rather than single packets. The client asks for something, the server supplies state, the player acts on that state, and the server decides whether the interaction continues or closes.

This page follows four of those conversations in order. The individual packet pages remain the source of truth for complete body layouts and uncertain fields.

## Reading the examples

Each example shows the decoded plaintext packet body. Framing, sequence bytes, transforms, and the dialog-response inner wrapper are omitted. Those layers are described in [Network transport](transport.md) and [Packet transforms](packet-transforms.md).

All multibyte integers are big-endian. Values such as names, IDs, and messages are illustrative, not captured traffic. `string8("Ari")` means a one-byte length followed by the three text bytes. `string16` uses a two-byte length.

```text
C -> S    client sends to server
S -> C    server sends to client
```

Direction matters. Opcode `0x2F`, for example, is [`CGroupToggle`](client/047-0x2f-group-toggle.md) from the client and [`SScreenMenu`](server/047-0x2f-screen-menu.md) from the server.

## Bulletin conversation

The bulletin flow moves through a stack of server-owned views. Opening the feature asks for its top-level board list. Selecting a board asks for one page of entries, and selecting an entry asks for its content.

```text
open bulletin
    |
    v
request board list <------+
    |                      |
    v                      |
select board -> list page -+
                    |
                    v
               open entry
```

The client uses [`CBulletin`](client/059-0x3b-bulletin.md) opcode `0x3B` for every request. The server uses [`SBulletin`](server/049-0x31-bulletin.md) opcode `0x31` for every view and operation result.

### Browse a board and open an article

Opening `BulletinSession` immediately sends action `1`:

```text
C -> S  RequestBoardList
3B 01
```

The server returns response type `1`. This creates `BoardListDialog`:

```text
S -> C  BoardList
opcode        = 31
response_type = 01
heading       = string8("Boards")
board_count   = 02
boards        = [
    { board_id = 000A, board_name = string8("Public") },
    { board_id = 000B, board_name = string8("Help") }
]
```

Selecting board `0x000A` asks for its first list page. Every recovered caller uses list direction `0xF0`:

```text
C -> S  RequestListPage
3B 02 000A 0000 F0
      |    |    +-- list_direction
      |    +------- before_entry_id
      +------------ board_id
```

The server's response type `2` creates `ArticleListDialog`:

```text
S -> C  ArticleList
opcode        = 31
response_type = 02
permissions   = 00
board_id      = 000A
heading       = string8("Public")
article_count = 01
articles      = [
    {
        flags      = 00,
        article_id = 002A,
        author     = string8("Ari"),
        month      = 07,
        day        = 15,
        title      = string8("Hello")
    }
]
```

Opening article `0x002A` sends action `3`. The final byte is the requested navigation operation used by View, Previous, and Next:

```text
C -> S  RequestEntry
3B 03 000A 002A 00
```

Response type `3` creates `ArticleDialog` and carries the article body:

```text
S -> C  Article
opcode                  = 31
response_type           = 03
navigation_flags        = 00
unknown_before_board_id = 00
board_id                = 000A
author                  = string8("Ari")
month                   = 07
day                     = 15
title                   = string8("Hello")
content                 = string16("Welcome!")
```

The client treats permission, entry, and navigation flags as UI controls. Their individual bit meanings are not yet mapped.

### Post an article

The compose dialog sends action `4`:

```text
C -> S  PostArticle
opcode   = 3B
action   = 04
board_id = 000A
title    = string8("Meeting")
content  = string16("Meet at the inn.")
```

The client accepts response type `8` as the post result. Status `1` refreshes the current list immediately. Other status values show a generic alert first, then make the same refresh request.

```text
S -> C  PostResult
31 08 01

C -> S  RequestListPage
3B 02 000A 0000 F0
```

The post-result pairing is supported by the compose flow. Meanings for status values other than `1` remain unknown.

### Mail, delete, and highlight branches

The same session also routes mailbox views and operation replies:

| Client action | Likely next server response | Result in the client |
| --- | --- | --- |
| `2` for a mailbox | Type `4` | Open `MailListDialog` |
| `3` for a mail entry | Type `5` | Open `MailDialog` |
| `5` delete entry | Type `7` | Show the server's message in the active dialog |
| `6` send mail | Type `7` can be accepted by the parent mail UI | Exact server pairing is not proven |
| `7` highlight article | Not established | No response pairing is claimed |

Article posting is the unusual branch: response type `8` causes the client itself to send the next action `2` refresh. Response type `7` only displays the supplied message.

## Player exchange conversation

Exchange uses [`CExchange`](client/074-0x4a-exchange.md) opcode `0x4A` for player actions and [`SExchange`](server/066-0x42-exchange.md) opcode `0x42` for server-owned state. The dialog never assumes that a local click succeeded. It waits for a server event before updating or closing.

```text
CExchange Start
       |
       v
SExchange Started -> ExchangeDialog
                         |
                  item, gold, accept
                         |
                         v
                  CExchange action
                         |
                         v
                  SExchange event
```

### Start and keep the exchange ID

The start form carries the selected target value:

```text
C -> S  Start
4A 00 01020304
```

The static caller for this builder has not been recovered, so the normal live UI trigger remains unresolved. A successful server start supplies the value used by the rest of the conversation:

```text
S -> C  Started
opcode      = 42
event       = 00
exchange_id = 11223344
target_name = string8("Bryn")
```

`ExchangeDialog` stores `0x11223344`. Every later client action echoes it. The client does not prove whether the initial target value and returned exchange ID must be identical.

### Add an item

A drop from inventory slot 3 first asks to add one item:

```text
C -> S  AddOneItem
4A 01 11223344 03
```

For a stackable item, the server can ask for a quantity. The client then opens `AddItemWithCountDialog` and replies with action `2`:

```text
S -> C  QuantityPrompt
42 01 03

C -> S  AddStackableItem
4A 02 11223344 03 05
                   +-- quantity 5
```

The offer changes only when the server broadcasts event `2`:

```text
S -> C  ItemAdded
opcode              = 42
event               = 02
party               = 00
item_index          = 00
tagged_item_sprite  = 8001
item_color          = 00
item_name           = string8("Apple")
```

Party `0` means the local offer. Any nonzero party value means the other player's offer.

### Set gold and accept

Gold follows the same request-then-update pattern:

```text
C -> S  SetGold
4A 03 11223344 000003E8

S -> C  GoldAdded
42 03 00 000003E8
```

The OK button sends action `5`, but does not close the dialog or mark the player accepted on its own:

```text
C -> S  Accept
4A 05 11223344

S -> C  Accepted by local player
opcode  = 42
event   = 05
party   = 00
message = string8("Accepted")

S -> C  Accepted by other player
opcode  = 42
event   = 05
party   = 01
message = string8("Exchange complete")
```

The first accepted event updates one acknowledgement flag. The dialog closes only after both party flags are set. This makes the server authoritative for completion.

Cancellation uses action or event `4` depending on direction:

```text
C -> S  Cancel request
4A 04 11223344

S -> C  Cancelled
opcode  = 42
event   = 04
party   = 01
message = string8("Exchange cancelled")
```

Any Cancelled event displays its message and closes immediately. If a Started event arrives while local state blocks exchange, the client also sends action `4` and does not open the pane.

## Group conversations

Group traffic contains three related conversations: the ordinary request prompt, recruiting-group details, and the invitation toggle. [`CGroup`](client/046-0x2e-group.md) and [`SGroup`](server/099-0x63-group.md) do not form a simple mirrored action list.

### Ordinary group request

Suppose Ari asks to group with Bryn:

```text
Ari client -> server
opcode      = 2E
action      = 02                  // Request
target_name = string8("Bryn")

server -> Bryn client
opcode         = 63
action         = 01               // Ask
requester_name = string8("Ari")
```

Bryn's client opens the normal group prompt. Accepting it, or having a nonzero `GroupAnswer` setting, sends:

```text
Bryn client -> server
opcode      = 2E
action      = 03                  // Accept
target_name = string8("Ari")
```

Only the accept send is confirmed. This client does not provide an ordinary reject action in the recovered `CGroup` builders. It also does not use `SGroup` action `2` to populate a member list: the deserializer stops after that action byte and the handler does nothing.

### Recruiting group details and join

Publishing a recruiting box sends action `4`. The leader's own name is followed by the form values:

```text
C -> S  RecruitStart
opcode           = 2E
action           = 04
target_name      = string8("Ari")
group_name       = string8("Hunt")
note             = string8("Crypt run")
minimum_level    = 20
maximum_level    = 40
maximum_warriors = 02
maximum_wizards  = 01
maximum_rogues   = 01
maximum_priests  = 01
maximum_monks    = 01
```

A viewer requests one leader's details with action `5`. Server action `4` returns the form plus a current count beside each class maximum:

```text
C -> S  RecruitView
opcode      = 2E
action      = 05
target_name = string8("Ari")

S -> C  RecruitInfo
opcode           = 63
action           = 04
leader           = string8("Ari")
group_name       = string8("Hunt")
note             = string8("Crypt run")
minimum_level    = 20
maximum_level    = 40
warriors         = { maximum = 02, current = 01 }
wizards          = { maximum = 01, current = 00 }
rogues           = { maximum = 01, current = 01 }
priests          = { maximum = 01, current = 00 }
monks            = { maximum = 01, current = 00 }
```

Choosing Join sends action `7` for the displayed leader. The server can then send action `5`, which makes the client produce an ordinary action `2` request for the supplied name:

```text
C -> S  RecruitJoin
2E 07 string8("Ari")

S -> C  RecruitJoin continuation
63 05 string8("Ari")

C -> S  ordinary Request generated by the client
2E 02 string8("Ari")
```

The final membership decision and roster state are server-owned. `SGroup` itself does not carry an active member-list body in this client.

### Toggle incoming invitations

[`CGroupToggle`](client/047-0x2f-group-toggle.md) is a separate one-byte request. Supplied runtime traces show the client following it with [`CSelfLook`](client/045-0x2d-self-look.md):

```text
C -> S  2F                    // CGroupToggle
C -> S  2D                    // CSelfLook
```

The observed response bundle is not one `SGroup` reply. It contains [`SStatus`](server/008-0x08-status.md), [`SMessage`](server/010-0x0a-message.md), and [`SSelfLook`](server/057-0x39-self-look.md). The changing state is:

| Result | `SMessage` setting row | `SSelfLook.is_group_open` |
| --- | --- | ---: |
| Invitations closed | `Join a group     :OFF` | `0` |
| Invitations open | `Join a group     :ON ` | `1` |

The accompanying `SStatus` combat-modifier body was identical in both captured cycles, so it does not carry the invitation state. One close trace also contained `SMotion`; because the open trace did not, that packet is not a required step in this conversation.

## NPC screen-menu conversation

An NPC screen menu is a server-driven form. [`SScreenMenu`](server/047-0x2f-screen-menu.md) describes the speaker, prompt, control type, and choices. The chosen value returns in [`CMerchant`](client/057-0x39-merchant.md).

```text
S -> C  SScreenMenu
            |
            v
      client builds controls
            |
       player chooses
            |
            v
C -> S  CMerchant
            |
            v
      wait for next server packet
```

The server must remember the active menu type. `CMerchant` echoes the target and pursuit IDs, but does not repeat `menu_type`.

### Text-choice example

This example asks the player to choose Buy or Sell:

```text
S -> C  Text menu
opcode                  = 2F
menu_type               = 00
target_type             = 01
target_id               = 01020304
ignored_unknown         = 00
speaker_sprite          = 0010
speaker_color           = 00
ignored_secondary_group = 00000000
show_graphic            = 01
speaker_name            = string8("Merchant")
content                 = string16("What do you need?")
choice_count            = 02
choices                 = [
    { choice_text = string8("Buy"),  pursuit_id = 0100 },
    { choice_text = string8("Sell"), pursuit_id = 0101 }
]
```

Choosing Sell returns the attached pursuit ID:

```text
C -> S  Text-menu selection
39 01 01020304 0101
|  |  |        +---- pursuit_id
|  |  +------------- target_id
|  +---------------- target_type
+------------------- opcode
```

After queuing this response, the client deactivates the nested menu and waits. Continuing the conversation requires another server packet, commonly another `SScreenMenu` with a new prompt or list.

### Other response shapes

The response bytes after the common `CMerchant` header depend on the server's active screen-menu type:

```text
type 2 text input
S -> C: pursuit_id = 0200
C -> S: 39 01 01020304 0200 string8("Ari")

type 4 ordinary server item
S -> C: pursuit_id = 0300, item name = string8("Apple")
C -> S: 39 01 01020304 0300 string8("Apple")

type 5 local inventory
S -> C: pursuit_id = 0400, allowed inventory slots = [03, 07]
C -> S: 39 01 01020304 0400 03
```

Argumented menus also echo the server's opaque argument. Pursuit `0x004B` uses a binary record ID and quantity instead of an item name. Pursuit `0x004E` uses a three-byte local-slot response. The canonical [`CMerchant` response table](client/057-0x39-merchant.md#response-variants) lists every confirmed form.

The normal `CMerchant` body then receives the dialog-response inner wrapper before its ordinary derived transform. A server implementation must remove both layers before reading the body shown here.

### Close, Top, and pursuit dialogs

Closing the outer screen-menu pane is local. It sends no `CMerchant`. Top sends [`CRequestObjectInfo`](client/067-0x43-request-object-info.md) subtype `1` for the target and closes the NPC session.

Screen menus are also distinct from pursuit dialogs. The pursuit conversation uses [`SPursuitMessage`](server/048-0x30-pursuit-message.md) and [`CPursuit`](client/058-0x3a-pursuit.md), even though both families share the surrounding `NPCSession` UI. See [NPC dialogs](../systems/npc-dialogs.md) for that pane flow and its separate close behavior.
