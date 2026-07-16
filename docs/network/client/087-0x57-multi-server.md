# Multi Server (`CMulti`)

| Item | Value |
| --- | --- |
| Direction | Client to server |
| Command | `0x57` (87) |
| Transform | `static` |
| Behavioral alias | `CMultiServer` |
| Name provenance | Project-owner protocol name; server-selection behavior confirmed locally |

## Purpose

The client sends this message for **multi server**.

The exact client protocol name is `CMulti`. The more descriptive `CMultiServer` alias is supported by the caller, which selects a server record from configuration, and by the `ServerSelectDialogPane` RTTI owner. Server opcode `0x56` has the exact RTTI name [`SMulti`](../server/086-0x56-multi.md).

The client has no derived packet RTTI for `CMulti` itself. The paired names are preserved as recovered instead of being forced to match a constructed `SMultiServer` name.

## Sent by

The server-selection dialog sends this when the player chooses a row. `SVersionCheck` also reaches the same selection path automatically when the local server table has a matching CRC and contains exactly one entry. That automatic path produced the observed builder fields `57 00 00 00`; the common submission terminator follows them on the wire.

## Body

```text
packet CMulti {
    u8 opcode                 // 0x57
    u8 reserved_0             // 0
    u8 server_id              // first byte of the selected server record
    u8 reserved_1             // 0
    u8 terminator             // 0, appended by net_submit_client_packet
}
```

The dialog row selects a local record, but the packet carries that record's stored ID. It is not necessarily the row number. The builder supplies four bytes; the common submission layer adds the fifth zero before the static transform. The supplied decoded trace omits this common trailing terminator.
