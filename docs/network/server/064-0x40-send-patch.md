# Send Patch (`SSendPatch`)

| Item | Value |
| --- | --- |
| Direction | Server to client |
| Command | `0x40` (64) |
| Encoding | none |
| Packet class | None found |
| Name provenance | Project-owner protocol name |
| Local evidence | Inbound transform-policy switch in `net_receive_frames` |

## Purpose

The server sends this message for **send patch**.

The opcode has an explicit raw policy in `net_receive_frames`, but `net_server_packet_factory_ctor` does not register a concrete RTTI class for it. The protocol name is `SSendPatch`; its special parser and relationship to client [`CRequestPatch`](../client/072-0x48-request-patch.md) remain to be located.

`SSendPatch` is therefore preserved as protocol vocabulary, not claimed as a compiler-recovered class name.

This opcode is not on the verified `Patcher2.exe` launch path. The 7.41 client receives that notification through [`SVersionCheck`](000-0x00-version-check.md) subtype `2`. The purpose of this separate raw opcode remains unresolved.

## Body

```text
packet SSendPatch {
    u8 opcode                 // 0x40
    ... fields unknown
}
```
