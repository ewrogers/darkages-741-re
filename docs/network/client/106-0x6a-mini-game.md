# Mini Game (`CMiniGame`)

| Field | Value |
| --- | --- |
| Direction | Client to server |
| Opcode | `0x6A` (106) |
| Common transform | derived |
| Representative builder | `0x0050C600` |
| Name provenance | The class name comes from related class vocabulary matched to the locally confirmed builder behavior. |

## Current evidence

The representative builder at `0x0050C600` writes opcode `0x6A` as body byte 0 and reaches `net_submit_client_packet`.

No concrete derived client packet RTTI class exists in this binary. The display name is therefore kept separate from the locally verified opcode evidence.

## Known send sites

- `0x50D128` in `sub_50d0f0`; nearest RTTI owner not yet identified.
- `0x4EC2D7` in `sub_4ec1f0`, reachable from `Pane::FindFarmpet::FindFarmpetPane`.

## Plaintext body

```text
opcode:u8
... fields pending
```

Field order, variants, state effects, and paired packets remain to be traced.
