# Block Listen (`CBlockListen?`)

| Field | Value |
| --- | --- |
| Direction | Client to server |
| Opcode | `0x0D` (13) |
| Common transform | derived |
| Representative builder | `0x00550AA0` |
| Name provenance | The opcode and builder are locally confirmed. The class spelling is reconstructed from behavior and related terminology. |

## Current evidence

The representative builder at `0x00550AA0` writes opcode `0x0D` as body byte 0 and reaches `net_submit_client_packet`.

No concrete derived client packet RTTI class exists in this binary. The display name is therefore kept separate from the locally verified opcode evidence.

## Known send sites

- `0x550896` in `sub_550860`, reachable from `CharInputPane::BlockListenInputPane`.

## Plaintext body

```text
opcode:u8
... fields pending
```

Field order, variants, state effects, and paired packets remain to be traced.
