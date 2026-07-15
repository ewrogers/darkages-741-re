# Drop Gold (`CDropGold?`)

| Field | Value |
| --- | --- |
| Direction | Client to server |
| Opcode | `0x24` (36) |
| Common transform | derived |
| Representative builder | `0x004975C0` |
| Name provenance | The opcode and builder are locally confirmed. The class spelling is reconstructed from behavior and related terminology. |

## Current evidence

The representative builder at `0x004975C0` writes opcode `0x24` as body byte 0 and reaches `net_submit_client_packet`.

No concrete derived client packet RTTI class exists in this binary. The display name is therefore kept separate from the locally verified opcode evidence.

## Known send sites

- `0x497580` in `sub_497560`, reachable from `DialogPane::DropGoldDialogPane`.

## Plaintext body

```text
opcode:u8
... fields pending
```

Field order, variants, state effects, and paired packets remain to be traced.
