# Request Patch (`CRequestPatch`)

| Item | Value |
| --- | --- |
| Direction | Client to server |
| Command | `0x48` (72) |
| Encoding | none |
| Name provenance | Project-owner protocol name; local evidence currently confirms the raw opcode policy |

## Purpose

The client sends this message for **request patch**.

`net_send_client_packet` includes opcode `0x48` in its raw-policy branch. A fixed local builder and its send sites have not yet been isolated. Server opcode `0x40`, [`SSendPatch`](../server/064-0x40-send-patch.md), is the expected counterpart, but the request/response flow still needs a local control-flow trace.

The client has no derived packet RTTI for this name.

## Body

```text
packet CRequestPatch {
    u8 opcode                 // 0x48
    ...                         // fields pending
}
```
