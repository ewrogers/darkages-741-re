# Use Spell (`CUseSpell`)

| Field | Value |
| --- | --- |
| Direction | Client to server |
| Opcode | `0x0F` (15) |
| Common transform | derived |
| Representative builder | `0x00428690` |
| Name provenance | The class name comes from related class vocabulary matched to the locally confirmed builder behavior. |

## Current evidence

The representative builder at `0x00428690` writes opcode `0x0F` as body byte 0 and reaches `net_submit_client_packet`.

No concrete derived client packet RTTI class exists in this binary. The display name is therefore kept separate from the locally verified opcode evidence.

## Known send sites

- `0x428B70` in `sub_428b30`, reachable from `BatchJob::BulletinBangUserBatchJob`.

## Plaintext body

```text
opcode:u8
... fields pending
```

Field order, variants, state effects, and paired packets remain to be traced.
