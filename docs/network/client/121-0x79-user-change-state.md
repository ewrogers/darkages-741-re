# User Change State (`CUserChangeState?`)

| Field | Value |
| --- | --- |
| Direction | Client to server |
| Opcode | `0x79` (121) |
| Common transform | derived |
| Representative builder | `0x005FC790` |
| Name provenance | The opcode and builder are locally confirmed. The class spelling is reconstructed from behavior and related terminology. |

## Current evidence

The representative builder at `0x005FC790` writes opcode `0x79` as body byte 0 and reaches `net_submit_client_packet`.

No concrete derived client packet RTTI class exists in this binary. The display name is therefore kept separate from the locally verified opcode evidence.

## Known send sites

- `0x5F9E39` in `sub_5f9e20`, reachable from `MapUserInterface::WorldPane_Impl`.

## Plaintext body

```text
opcode:u8
... fields pending
```

Field order, variants, state effects, and paired packets remain to be traced.
