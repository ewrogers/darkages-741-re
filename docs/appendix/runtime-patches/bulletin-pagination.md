# Bulletin pagination

This patch stops article and mail lists from repeatedly sending a newest-page cursor when scrolling an empty list. It changes only the empty-list branch in each older-page helper. Normal initial loading and pagination of a nonempty list remain intact.

The behavior and repeat condition are explained in [Bulletin boards and mail](../../systems/bulletin-and-mail.md#pagination-and-the-0x7fff-loop).

## In-place changes

The preferred image base is `0x00400000`. File offsets are reference information only. A launcher uses the loaded module base plus the RVA.

| List | Static address | RVA | File offset | Original | Replacement |
| --- | ---: | ---: | ---: | --- | --- |
| Articles | `0x00420748` | `0x00020748` | `0x0001FB48` | `7E 21` | `7E 46` |
| Mail | `0x00424608` | `0x00024608` | `0x00023A08` | `7E 21` | `7E 46` |

Both sites are the same instruction shape:

```diff
  83 7D F4 00 | cmp dword [ebp-0x0C], 0  ; loaded row count
- 7E 21       | jle empty_fallback        ; cursor = 0x7FFF
+ 7E 46       | jle function_epilogue     ; no older page exists
```

The replacement keeps the conditional `JLE` and changes only its signed one-byte displacement. When the row count is positive, execution still reads the final loaded row, subtracts one from its entry ID, and sends the normal older-page request.

When the row count is zero, the new target is the existing function epilogue. It avoids the block that assigns cursor `0x7FFF`, so pointer and keyboard handlers cannot turn an empty list into repeated `3B 02 section_id 7F FF F0` requests.

## Why initial loading still works

Opening a board or mailbox calls `net_send_bulletin_initial_list_request`, which writes cursor `0x7FFF` directly. Explicit newest-page refreshes use `ui_article_list_request_latest_page` or `ui_mail_list_request_latest_page`, which also write `0x7FFF` directly. None of those paths call the patched older-page helper with an empty list.

This patch does not add general pagination state. A nonempty list can still repeat its final cursor after a zero-row or duplicate-only response. That is less severe than the observed `0x7FFF` empty-list storm and requires an in-flight or no-progress latch rather than a safe two-byte branch change.

## Installation

Install both changes while the process is suspended:

1. Verify the complete executable fingerprint and preferred version.
2. Resolve each target as `loaded_module_base + RVA`.
3. Verify the original bytes `7E 21` and nearby `83 7D F4 00` comparison.
4. Temporarily make only the containing pages writable.
5. Write `7E 46` at both targets and read the bytes back.
6. Flush the instruction cache, restore the old page protections, and resume.

Fail closed if either target or original byte sequence differs. Do not install only one half unless intentionally fixing only article lists or only mail lists. The general checks in the [safe launcher workflow](safe-launcher.md) also apply.
