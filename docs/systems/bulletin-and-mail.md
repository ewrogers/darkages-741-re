# Bulletin boards and mail

The board and mailbox UI can be inspected without replaying mouse input. A live `BulletinSession` owns the current dialog, each list dialog owns a native list pane, and article or mail detail dialogs expose their displayed fields through attached controls. Observing the decoded `SBulletin` body as it enters the session preserves the exact server text and date fields.

## Detect the active view

`ui_bulletin_session_ptr` is null when no bulletin session exists. A live session keeps a history of at most ten `BulletinDialogPane` pointers:

```c
struct BulletinSessionState {
    u8 history_count;                    // +0x190
    s8 current_index;                    // +0x191, -1 means none
    BulletinDialogPane *history[10];     // +0x194
    ScreenDimmer *pending_dimmer;        // +0x1BC
    u16 current_section_id;              // +0x1C2
};
```

Read `history[current_index]` on the client main thread, then identify the complete object by its exact RTTI. Do not keep the dialog or control pointer across dispatcher ticks.

| Exact RTTI | Meaning |
| --- | --- |
| `BoardListDialog` | List of available boards |
| `ArticleListDialog` | Posts in `current_section_id` |
| `ArticleDialog` | One article detail |
| `MailListDialog` | Mail in `current_section_id` |
| `MailDialog` | One mail detail |
| `NewArticleDialog` | Composing an article |
| `NewMailDialog` | Composing new mail or a reply |

A nonnull `pending_dimmer` means a network-backed action is waiting for its reply and the bulletin UI is blocked. History membership alone is not proof that an older retained dialog is visible. Use the current history entry and normal pane registration or presentation state.

## Read board and message lists

The dialog control collection begins at `dialog + 0x594`. Its native indexed lookup returns the attached control; a scrollable control contains its list pane at control offset `+0x19C`.

| View | Scrollable control ID | Row model |
| --- | ---: | --- |
| `BoardListDialog` | `2` | `s16 board_id`, followed by a 256-byte NUL-terminated name |
| `ArticleListDialog` | `5` | `BulletinListRow` |
| `MailListDialog` | `6` | `BulletinListRow` |

Use `ui_list_pane_get_item_count` and `ui_list_pane_item_at` to enumerate the rows. The selected row index is the list pane's signed field at `+0x1C0`; `-1` means no current selection.

```c
struct BulletinListRow {       // size 0x206
    s16 entry_id;              // +0x000
    u8 flags;                  // +0x002
    u8 month;                  // +0x003
    u8 day;                    // +0x004
    char author[256];          // +0x005
    char title[257];           // +0x105
};
```

Rows are maintained in descending signed entry-ID order. The `flags` byte changes row styling and read state, but its individual bits are not yet mapped. A privileged article list may also contain a multi-selection object at list offset `+0x1D0`; the ordinary current row remains at `+0x1C0`.

## Pagination and the `0x7FFF` loop

Article and mail lists use the same pagination rule. The initial request sends `before_entry_id = 0x7FFF` and `list_direction = 0xF0`. This asks for the newest page. At the loaded end, the client reads the final row, subtracts one from its signed 16-bit entry ID, and requests that cursor when it remains greater than zero.

```c
cursor = 0x7FFF;
if (list.count > 0)
    cursor = list[list.count - 1].entry_id - 1;

if (cursor > 0)
    request_list_page(section_id, cursor, 0xF0);
```

The scroll trigger is broader than a transition into the bottom. After the base scrollable-pane handler consumes a pointer event, the article and mail overrides compare the current scroll position with the maximum. Equality immediately calls the older-page helper. They do not record that the bottom was already reached.

Consumed keyboard events can also call the same helper when the pane's row-count conditions indicate that more rows may be needed. These paths share the same cursor calculation and lack of pagination state.

This produces a confirmed client-side repeat condition:

1. The list is empty, so both scroll positions compare equal at zero.
2. A consumed pointer event calls the older-page helper.
3. The empty-list fallback sends cursor `0x7FFF`, producing bytes `7F FF` in the packet.
4. A zero-row server reply inserts nothing and records no end-of-list state.
5. Another consumed pointer event at the bottom sends the same request again.

There is no pagination request-in-flight flag, end-of-list flag, repeated-cursor check, or requirement that the scroll position changed. A nonempty list can similarly repeat its final cursor after a zero-row or duplicate-only reply, although that cursor will normally be the final loaded entry ID minus one rather than `0x7FFF`.

An external controller should not copy this behavior literally. Keep one in-flight cursor per section, wait for the matching `SBulletin` list reply, and stop when the reply has zero rows or the minimum loaded entry ID does not decrease. Clear that state when the section changes or a newest-page refresh begins.

The [bulletin pagination runtime patch](../appendix/runtime-patches/bulletin-pagination.md) provides a narrow two-byte fix for each empty-list helper. It preserves initial list loading but does not add a general no-progress latch for nonempty lists.

## Read the current detail

`ArticleDialog + 0x63C` is the current article ID. `MailDialog + 0x63C` is the current mail ID. The board or mailbox ID remains separately in `BulletinSession + 0x1C2`.

| Field | Article control ID | Mail control ID |
| --- | ---: | ---: |
| Author | `6` | `7` |
| Subject | `7` | `8` |
| Body scrollable | `8` | `9` |
| Display date | `9` | `10` |

`ui_text_edit_control_copy_text` can copy simple control text such as author, subject, and date. The displayed date is formatted as `%2d/%2d`. The body has already passed through the formatted-text parser, so a decoded-packet observer is the more exact source for its original bytes and month/day fields.

The recommended detector copies each decoded opcode `0x31` body at `ui_bulletin_session_apply_server_body`, parses it according to [`SBulletin`](../network/server/049-0x31-bulletin.md), and caches details by `(current_section_id, entry_id)`. This also lets a detector reconstruct the exact current detail after the UI has converted its body for display. If observation starts after a detail is already open, the entry ID and visible text are still recoverable from the dialog.

## Compose and edit state

Exact RTTI `NewArticleDialog` or `NewMailDialog` is the positive signal that the bulletin UI is in compose mode. This is separate from the paper editor's `EditablePaperPane` and its enter-editing packet.

| Compose view | Recipient or author | Subject | Body |
| --- | ---: | ---: | ---: |
| `NewArticleDialog` | `2`, static author | `3` | `4` |
| `NewMailDialog` | `2` | `3` | `4` |

For mail, control `2` is an editable `TextEditControlPane` for a new message and a `StaticTextControlPane` for a fixed reply recipient. Both derive through the same text-control path, but their exact RTTI distinguishes the modes.

Article list and detail views expose a New action. Mail list and detail views expose New and Reply actions. Selection-dependent actions such as View, Reply, and Delete are disabled when there is no selected row. Compose availability should therefore be reported from the exact active view, selection state, control enabled state, and absence of the pending dimmer rather than from a hardcoded button table alone.

## Interaction boundary

For detection, read the UI-owned state because it tells you what the player can currently see and edit. For an automated choice, invoke the established bulletin packet producer on the main-thread dispatcher after validating that the matching session, section, entry, and compose state are still current. Sending a packet alone cannot tell an observer which retained dialog is presented or what unsent text is in an edit control.
