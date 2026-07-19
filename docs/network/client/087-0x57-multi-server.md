# Multi Server (`CMulti`)

| Item | Value |
| --- | --- |
| Direction | Client to server |
| Command | `0x57` (87) |
| Transform | `static` |
| Behavioral alias | `CMultiServer` |
| Name provenance | Project-owner protocol name; server-selection behavior confirmed locally |

## Purpose

This packet either requests a replacement server list or submits the server ID selected in `ServerSelectDialogPane`.

The exact client protocol name is `CMulti`. The more descriptive `CMultiServer` alias is supported by the caller, which selects a server record from configuration, and by the `ServerSelectDialogPane` RTTI owner. Server opcode `0x56` has the exact RTTI name [`SMulti`](../server/086-0x56-multi.md).

The client has no derived packet RTTI for `CMulti` itself. The paired names are preserved as recovered instead of being forced to match a constructed `SMultiServer` name.

## Operations

Operation `0` submits a selection. The dialog sends it when the player chooses a row. [`SVersionCheck`](../server/000-0x00-version-check.md) and [`SMulti`](../server/086-0x56-multi.md) also reach the same path automatically when the active server list contains exactly one record.

Operation `1` requests the replacement list carried by `SMulti`. `SVersionCheck` constructs the dialog in this mode when the local list is empty or its CRC differs from the server's value.

## Body

```text
packet CMulti {
    u8      opcode                    // 0x57
    u8      operation

    if operation == 0 {
        u8      server_id             // selected record ID, not row number
        u8      reserved_0            // 0
    }

    if operation == 1 {
        u8      uninitialized_request_byte
    }

    u8      terminator                // 0, appended by net_submit_client_packet
}
```

For operation `0`, `net_send_multi_server_selection` supplies `57 00 <server_id> 00`; the common submission layer appends a fifth zero before the static transform. The supplied decoded trace omits this common trailing terminator.

The operation-`1` builder supplies three bytes before the common terminator. It writes `57 01`, then appears intended to clear the third byte. The actual instruction clears a dword at local-buffer offset `8` while submitting only offsets `0` through `2`. The submitted third byte therefore retains previous stack data, and the appended fourth byte is zero. No client code derives meaning from that retained byte; the request purpose follows directly from the CRC-mismatch constructor path and the `SMulti` response handler.
