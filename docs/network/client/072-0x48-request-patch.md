# Request Patch (`CRequestPatch`)

| Field | Value |
| --- | --- |
| Direction | Client to server |
| Opcode | `0x48` (72) |
| Common transform | raw |
| Representative builder | Not yet isolated |
| Name provenance | Project-owner protocol name; local evidence currently confirms the raw opcode policy |

## Current evidence

`net_send_client_packet` includes opcode `0x48` in its raw-policy branch. A fixed local builder and its send sites have not yet been isolated. Server opcode `0x40`, [`SSendPatch`](../server/064-0x40-send-patch.md), is the expected counterpart, but the request/response flow still needs a local control-flow trace.

The client has no derived packet RTTI for this name.

## Known send sites

No concrete send site has been isolated yet. The current address evidence is the raw-policy branch at `0x0056492A`.

## Plaintext body

```text
opcode:u8                 // 0x48
... fields pending
```
