# Remove Equipment (`CRemoveEquipment`)

| Field | Value |
| --- | --- |
| Direction | Client to server |
| Opcode | `0x44` (68) |
| Common transform | derived |
| Representative builder | `0x00460330` |
| Name provenance | The class name comes from related class vocabulary matched to the locally confirmed builder behavior. |

## Current evidence

The representative builder at `0x00460330` writes opcode `0x44` as body byte 0 and reaches `net_submit_client_packet`.

No concrete derived client packet RTTI class exists in this binary. The display name is therefore kept separate from the locally verified opcode evidence.

## Known send sites

- `0x45F35C` in `sub_45f260`, reachable from `DialogPane::EquipPane`.
- `0x45FDAC` in `sub_45fda0`; nearest RTTI owner not yet identified.
- `0x45FDB6` in `sub_45fda0`; nearest RTTI owner not yet identified.

## Plaintext body

```text
opcode:u8
... fields pending
```

Field order, variants, state effects, and paired packets remain to be traced.
