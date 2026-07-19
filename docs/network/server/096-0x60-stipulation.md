# Stipulation (`SStipulation`)

| Item | Value |
| --- | --- |
| Direction | Server to client |
| Command | `0x60` (96) |
| Transform | `static` |
| Name provenance | Microsoft C++ RTTI in the target |

## Purpose

This packet keeps the selected server greeting in sync. The local greeting is stored in `mServer.tbl`.

Before either handler processes the greeting, it checks whether the homepage URL is cached. If not, it sends [`CRequestHomepage`](../client/104-0x68-request-homepage.md). This is why the observed mode-0 stipulation is followed immediately by `68 01`.

## Body

```text
packet SStipulation {
    u8      opcode                    // 0x60
    u8      mode

    if mode == 0 {
        u32     greeting_crc32
    }

    if mode == 1 {
        u16     compressed_size
        bytes   zlib_data[compressed_size]
    }
}
```

Mode 0 compares the received CRC32 with the decoded local greeting. A match displays the greeting. A mismatch sends an empty [`CStipulation`](../client/075-0x4b-stipulation.md) request.

The observed mode-0 body carries CRC32 `0xE5DC1439`.

Mode 1 inflates the replacement into a buffer capped at 10,000 bytes, saves the updated server table, and displays the new greeting.

## Agreement pane and main-menu input

After a matching mode-0 check or a successful mode-1 replacement, the normal US path constructs `AgreementDialogPane` from `_nagree.txt`. The pane's OK action only closes and unregisters the pane. It sends no acknowledgement packet.

`MainMenuPane +0x500` is the local input gate. Its pointer and keyboard handlers consume input immediately while this value is nonzero. Both successful stipulation paths clear it to zero after the agreement decision, which restores normal menu input and makes the Continue button clickable.

The Japan distribution path already skips constructing the agreement pane and still reaches that same gate-clearing code. The [Hide stipulation](../../appendix/runtime-patches/hide-stipulation.md) runtime patch makes the two successful paths follow this existing branch for every distribution. CRC comparison, table replacement, homepage requesting, and the main-menu state transition are left intact.

The separate [Early Continue](../../appendix/runtime-patches/early-continue.md) patch lets pointer clicks enter normal title-menu hit testing before the gate clears. It does not change the keyboard gate or stipulation processing.

## Handlers

- `net_handle_stipulation_raw` at `0x004B8570` parses a decoded packet buffer directly.
- `net_handle_stipulation` at `0x004B8890` handles the RTTI-backed packet object.

The constructor and packet factory also confirm opcode `0x60` for the `SStipulation` class. See [Server list and greeting](../server-tables.md).
