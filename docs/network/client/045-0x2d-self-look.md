# Self Look (`CSelfLook`)

| Field | Value |
| --- | --- |
| Direction | Client to server |
| Opcode | `0x2D` (45) |
| Common transform | static |
| Representative builder | `0x0041B840` |
| Name provenance | The class name comes from related class vocabulary matched to the locally confirmed builder behavior. |

## Current evidence

The representative builder at `0x0041B840` writes opcode `0x2D` as body byte 0 and reaches `net_submit_client_packet`.

No concrete derived client packet RTTI class exists in this binary. The display name is therefore kept separate from the locally verified opcode evidence.

## Known send sites

- `0x41BEF7` in `sub_41be30`, reachable from `Pane::BtmButtonsPane_A`, `BtmButtonsPane_A::GUIBackPane::_BtmButtonsPane`.
- `0x41B1D1` in `sub_41b040`; nearest RTTI owner not yet identified.
- `0x41B7F5` in `sub_41b710`, reachable from `TimerHandler::BtmButtonsPane_A`, `TimerHandler::GUIBackPane::_BtmButtonsPane`.

## Plaintext body

```text
opcode:u8
... fields pending
```

Field order, variants, state effects, and paired packets remain to be traced.
