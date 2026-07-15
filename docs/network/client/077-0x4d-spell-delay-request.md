# Spell Delay Request (`CSpellDelayRequest?`)

| Field | Value |
| --- | --- |
| Direction | Client to server |
| Opcode | `0x4D` (77) |
| Common transform | derived |
| Representative builder | `0x0049BAB0` |
| Name provenance | The opcode and builder are locally confirmed. The class spelling is reconstructed from behavior and related terminology. |

## Current evidence

The representative builder at `0x0049BAB0` writes opcode `0x4D` as body byte 0 and reaches `net_submit_client_packet`.

No concrete derived client packet RTTI class exists in this binary. The display name is therefore kept separate from the locally verified opcode evidence.

## Known send sites

- `0x49B9F0` in `sub_49b900`, reachable from `LineInputPane::StringSpellInputPane`, `ArgsLineInputPane::NumberArgsSpellInputPane`.

## Plaintext body

```text
opcode:u8
... fields pending
```

Field order, variants, state effects, and paired packets remain to be traced.
