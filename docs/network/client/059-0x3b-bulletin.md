# Bulletin (`CBulletin`)

| Field | Value |
| --- | --- |
| Direction | Client to server |
| Opcode | `0x3B` (59) |
| Common transform | derived |
| Representative builder | `0x0041CBC0` |
| Name provenance | The class name comes from related class vocabulary matched to the locally confirmed builder behavior. |

## Current evidence

The representative builder at `0x0041CBC0` writes opcode `0x3B` as body byte 0 and reaches `net_submit_client_packet`.

No concrete derived client packet RTTI class exists in this binary. The display name is therefore kept separate from the locally verified opcode evidence.

## Known send sites

- `0x41C3BD` in `sub_41c280`, reachable from `Pane::BtmButtonsPane_A`, `BtmButtonsPane_A::GUIBackPane::_BtmButtonsPane`.

## Plaintext body

```text
opcode:u8
... fields pending
```

Field order, variants, state effects, and paired packets remain to be traced.
