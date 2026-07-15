# Emotion (`CEmotion`)

| Field | Value |
| --- | --- |
| Direction | Client to server |
| Opcode | `0x1D` (29) |
| Common transform | derived |
| Representative builder | `0x005F46C0` |
| Name provenance | The class name comes from related class vocabulary matched to the locally confirmed builder behavior. |

## Current evidence

The representative builder at `0x005F46C0` writes opcode `0x1D` as body byte 0 and reaches `net_submit_client_packet`.

No concrete derived client packet RTTI class exists in this binary. The display name is therefore kept separate from the locally verified opcode evidence.

## Known send sites

- `0x5F1421` in `sub_5f0d20`, reachable from `WorldControllerPane::WorldPane`, `WorldPane::WorldPane_Impl`.
- `0x5F9AD5` in `sub_5f9ac0`, reachable from `MapInterface::WorldPane_Impl`.

## Plaintext body

```text
opcode:u8
... fields pending
```

Field order, variants, state effects, and paired packets remain to be traced.
