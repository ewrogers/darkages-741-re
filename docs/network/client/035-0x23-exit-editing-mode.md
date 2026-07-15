# Exit Editing Mode (`CExitEditingMode?`)

| Field | Value |
| --- | --- |
| Direction | Client to server |
| Opcode | `0x23` (35) |
| Common transform | derived |
| Representative builder | `0x0054A7D0` |
| Name provenance | The opcode and builder are locally confirmed. The class spelling is reconstructed from behavior and related terminology. |

## Current evidence

The representative builder at `0x0054A7D0` writes opcode `0x23` as body byte 0 and reaches `net_submit_client_packet`.

No concrete derived client packet RTTI class exists in this binary. The display name is therefore kept separate from the locally verified opcode evidence.

## Known send sites

- `0x54A9D6` in `sub_54a9b0`, reachable from `DialogPane::EditablePaperPane`.

## Plaintext body

```text
opcode:u8
... fields pending
```

Field order, variants, state effects, and paired packets remain to be traced.
