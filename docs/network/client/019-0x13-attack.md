# Attack (`CAttack`)

| Field | Value |
| --- | --- |
| Direction | Client to server |
| Opcode | `0x13` (19) |
| Common transform | derived |
| Representative builder | `0x005F44B0` |
| Name provenance | The class name comes from related class vocabulary matched to the locally confirmed builder behavior. |

## Current evidence

The representative builder at `0x005F44B0` writes opcode `0x13` as body byte 0 and reaches `net_submit_client_packet`.

No concrete derived client packet RTTI class exists in this binary. The display name is therefore kept separate from the locally verified opcode evidence.

## Known send sites

- `0x5F4D0E` in `sub_5f4a70`, reachable from `WorldControllerPane::WorldPane`, `WorldPane::WorldPane_Impl`, `TimerHandler::WorldPane`, and 1 other RTTI owner.
- `0x5F0C1E` in `sub_5f0bf0`, reachable from `WorldControllerPane::WorldPane`, `WorldPane::WorldPane_Impl`.

## Plaintext body

```text
opcode:u8
... fields pending
```

Field order, variants, state effects, and paired packets remain to be traced.
