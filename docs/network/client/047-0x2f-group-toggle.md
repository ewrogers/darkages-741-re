# Group Toggle (`CGroupToggle?`)

| Field | Value |
| --- | --- |
| Direction | Client to server |
| Opcode | `0x2F` (47) |
| Common transform | derived |
| Representative builder | `0x0041B8E0` |
| Name provenance | The opcode and builder are locally confirmed. The class spelling is reconstructed from behavior and related terminology. |

## Current evidence

The representative builder at `0x0041B8E0` writes opcode `0x2F` as body byte 0 and reaches `net_submit_client_packet`.

No concrete derived client packet RTTI class exists in this binary. The display name is therefore kept separate from the locally verified opcode evidence.

## Known send sites

- `0x41BEEF` in `sub_41be30`, reachable from `Pane::BtmButtonsPane_A`, `BtmButtonsPane_A::GUIBackPane::_BtmButtonsPane`.

## Plaintext body

```text
opcode:u8
... fields pending
```

Field order, variants, state effects, and paired packets remain to be traced.
