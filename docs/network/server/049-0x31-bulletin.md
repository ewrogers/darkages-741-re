# Bulletin (`SBulletin`)

`SBulletin` carries the server side of the board, article, and mail UI. It is the response family paired with [`CBulletin`](../client/059-0x3b-bulletin.md).

| Item | Value |
| --- | --- |
| Direction | Server to client |
| Opcode | `0x31` |
| Transform | `derived` |
| Name provenance | Project-owner protocol name |
| RTTI | No concrete server-packet RTTI class |
| UI owner | Exact RTTI `BulletinSession` |

## Body

```text
packet SBulletin {
    u8 opcode                    // 0x31
    u8 response_type

    if response_type == 1 {
        string8 heading
        u8 board_count

        repeat board_count {
            u16 board_id
            string8 board_name
        }
    }

    if response_type == 2 {
        u8 permissions
        u16 board_id
        string8 heading
        u8 article_count

        repeat article_count {
            u8 flags
            u16 article_id
            string8 author
            u8 month
            u8 day
            string8 title
        }
    }

    if response_type == 3 {
        u8 navigation_flags
        u8 unknown_before_board_id
        u16 board_id
        string8 author
        u8 month
        u8 day
        string8 title
        string16 content
    }

    if response_type == 4 {
        u8 permissions
        u16 mailbox_id
        string8 heading
        u8 mail_count

        repeat mail_count {
            u8 flags
            u16 mail_id
            string8 author
            u8 month
            u8 day
            string8 title
        }
    }

    if response_type == 5 {
        u8 navigation_flags
        u8 unknown_before_mailbox_id
        u16 mailbox_id
        string8 author
        u8 month
        u8 day
        string8 title
        string16 content
    }

    if response_type == 7 {
        u8 status
        string8 message
    }

    if response_type == 8 {
        u8 status
    }
}
```

The field roles called `permissions`, `flags`, and `navigation_flags` are inferred from which controls they enable. Their bit meanings are not yet mapped.

Response `7` is an operation reply accepted by article-list, article, mail-list, and mail dialogs. Each handler consumes `status` and displays `message`; the local branches do not use the status value to choose whether the message appears. Article and mail deletion reach this path. The parent mail UI can also accept it after a send, but the exact server-side action pairing is not proven by this client alone.

Response `8` is accepted only by `ArticleListDialog`. Status `1` refreshes the list directly. Any other value first opens a generic alert and then performs the same refresh. Its position in the compose flow supports an article-post reply, but the status values beyond `1` remain unknown.

## UI routing

The decoded body bypasses the server packet factory. The world dispatcher creates exact RTTI `BulletinSession`, which routes response types as follows:

| Type | Exact RTTI dialog | Layout |
| ---: | --- | --- |
| `1` | `BoardListDialog` | `_nbdlist.txt` |
| `2` | `ArticleListDialog` | `_narlist.txt` |
| `3` | `ArticleDialog` | `_narti.txt` |
| `4` | `MailListDialog` | `_nmaill.txt` |
| `5` | `MailDialog` | `_nmailr.txt` |

Responses `7` and `8` do not create another child dialog. They are delivered to the active article or mail dialog. Response `7` opens a reply alert from the supplied message. Response `8` refreshes the current article list by sending another [`CBulletin`](../client/059-0x3b-bulletin.md) action `2` request.

`BulletinSession` keeps a bounded history of ten dialog pointers. Opening a board, article, mail, or compose view prunes any forward history, attaches the new dialog, and activates it. Back and forward actions close the current view before activating the adjacent entry. Network-backed actions place a mode-5 `ScreenDimmer` over the UI until the matching response removes it.

The board chooser opens and closes through three vertical steps at 100 ms per step. Article and mail list panes keep their rows ordered by signed identifier and request older pages from the final loaded identifier minus one. Article lists also maintain a fixed-capacity integer selection set for privileged multi-select delete and highlight operations.

When no bulletin session exists, the outer handler also requires bit 0 of the first payload byte to be clear before constructing one. The purpose of that admission check remains unresolved.

## Privileged article controls

Any nonzero [`SStatus`](008-0x08-status.md#privilege-behavior) privilege changes `ArticleListDialog`. The constructor adds the optional control spelled `Hilight` in `_narlist.txt`. The list pane also allocates multi-selection state, honors modifier-based range and toggle selection, colors selected rows differently, and applies delete or highlight to every selected article. Without privilege, delete and highlight operate only on the current row.

This is a simple nonzero test. Privilege values `1`, `2`, and `3` receive the same bulletin behavior.
