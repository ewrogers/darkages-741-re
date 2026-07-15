# Send Patch (`SSendPatch`)

| Field | Value |
| --- | --- |
| Direction | Server to client |
| Opcode | `0x40` (64) |
| Common transform | raw |
| Registered server packet class | None found |
| Name provenance | Project-owner protocol name |
| Local evidence | Inbound transform-policy switch in `net_receive_frames` |

## Current evidence

The opcode has an explicit raw policy in `net_receive_frames`, but `net_server_packet_factory_ctor` does not register a concrete RTTI class for it. The protocol name is `SSendPatch`; its special parser and relationship to client [`CRequestPatch`](../client/072-0x48-request-patch.md) remain to be located.

`SSendPatch` is therefore preserved as protocol vocabulary, not claimed as a compiler-recovered class name.

## Plaintext body

```text
opcode:u8                 // 0x40
... fields unknown
```
