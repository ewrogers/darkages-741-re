# Bulletin (`CBulletin`)

`CBulletin` drives the complete board, article, and mail workflow. The client has 15 concrete builders for seven action values. Board browsing, article reading, mail reading, posting, deletion, and the optional `Hilight` control all reuse this one opcode.

| Item | Value |
| --- | --- |
| Direction | Client to server |
| Opcode | `0x3B` |
| Transform | `derived` |
| Name provenance | Project-owner protocol name, paired with the locally confirmed `SBulletin` UI |
| UI owner | Exact RTTI `BulletinSession` and its child dialogs |

The action names below are local behavioral names. The client does not contain a recovered action enum.

## Body

```text
packet CBulletin {
    u8 opcode                    // 0x3B
    u8 action

    if action == 2 {
        u16 section_id           // board ID or mailbox ID
        u16 before_entry_id
        u8 list_direction        // 0xF0 in every local caller
    }

    if action == 3 {
        u16 section_id           // board ID or mailbox ID
        u16 entry_id             // article ID or mail ID
        u8 navigation
    }

    if action == 4 {
        u16 board_id
        string8 title
        string16 content
    }

    if action == 5 {
        u16 section_id           // board ID or mailbox ID
        u16 entry_id             // article ID or mail ID

        if sent_from_mail_list {
            u8 reserved_zero     // always 0
        }
    }

    if action == 6 {
        u16 mailbox_id
        string8 receiver
        string8 title
        string16 content
    }

    if action == 7 {
        u16 board_id
        u16 article_id
    }
}
```

Action `1` has no fields after the action byte. The mail-list form of action `5` is the only deletion builder that appends `reserved_zero`; article deletion and deletion from an open mail dialog end after `entry_id`.

## Actions

| Action | Local name | Length | Client trigger |
| ---: | --- | ---: | --- |
| `1` | `RequestBoardList` | 2 | `BulletinSession` opens |
| `2` | `RequestListPage` | 7 | A board or mailbox is selected, or a list asks for older entries |
| `3` | `RequestEntry` | 7 | View, Previous, or Next in an article or mail dialog |
| `4` | `PostArticle` | Variable | Send in exact RTTI `NewArticleDialog` |
| `5` | `DeleteEntry` | 6 or 7 | Delete confirmation for an article or mail entry |
| `6` | `SendMail` | Variable | Send in exact RTTI `NewMailDialog`, including reply mode |
| `7` | `HighlightArticle` | 6 | Optional article-list control named `Hilight` in the layout |

No direct builder in this client emits action `0` or a value above `7`.

## Listing and entry navigation

Action `1` is the two-byte opening request:

```text
3B 01
```

Action `2` serves both article lists and mail lists. An initial request uses `before_entry_id = 0x7FFF`. When the list needs an older page, the client uses one less than the last visible entry ID, clamped to `1..0x7FFF`. Every local action `2` caller writes `list_direction = 0xF0`.

Action `3` also shares one shape between articles and mail. Direct selection uses `navigation = 0`. Previous uses the current entry ID minus one and `navigation = 0xFF`; Next uses the ID plus one and `navigation = 1`. The requested ID is clamped to `1..0x7FFF`.

The selected board ID determines whether the server answers action `2` with an article list or a mail list. There is no separate client action for opening the mailbox.

## Posting and mail

`NewArticleDialog` reads title control `3` and content control `4`. The builder can copy at most 255 title bytes and 4095 content bytes. The live content control applies its own lower input limit, so these builder bounds are not promises about what the stock UI lets a player type.

`NewMailDialog` reads receiver control `2`, title control `3`, and content control `4`, with the same 255, 255, and 4095-byte builder limits. Reply mode replaces the editable receiver with the selected sender's name, then sends the same action `6` body.

## Delete and highlight

Article-list deletion can operate on multiple selected rows. After confirmation, the client sends one action `5` packet per article. Article-detail and mail-detail deletion send the six-byte form. Mail-list deletion sends a seven-byte form with a trailing zero.

The shared `ConfirmDeleteAlert` keeps both its owner kind and list/detail mode. Accepting it dispatches to exactly one of the article-list, article-detail, mail-list, or mail-detail deletion paths, so the confirmation pane does not need four separate implementations.

The optional `Hilight` control is attached as action ID `6` in `ArticleListDialog`. It sends action `7`, one packet per selected article, without a confirmation dialog. The layout spelling is preserved here because it is direct client evidence. The exact server-side effect and permission rule still need runtime confirmation.

## Server replies

The paired [`SBulletin`](../server/049-0x31-bulletin.md) response routes through the active bulletin dialog.

| Client action | Expected response path |
| ---: | --- |
| `1` | Response `1`, board list |
| `2` | Response `2`, article list, or response `4`, mail list |
| `3` | Response `3`, article, or response `5`, mail |
| `4` | Article-list response `8` carries a status byte and refreshes the list |
| `5` | Response `7` carries a status byte and a message displayed by the dialog |
| `6` | The parent mail UI accepts response `7`, but the exact server pairing is not proven statically |
| `7` | The exact server reply remains unresolved |

Response pairings for actions `1` through `5` follow the receiving dialog and UI transition. The action `6` and `7` rows are intentionally narrower because the local client does not prove which server branch produces the reply.
