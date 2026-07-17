# Attack (`CAttack`)

| Item | Value |
| --- | --- |
| Direction | Client to server |
| Command | `0x13` (19) |
| Encoding | session key |
| Name provenance | The class name comes from related class vocabulary matched to the locally confirmed builder behavior. |

## Purpose

The client sends this message for **attack**.

## Sent by

Known static callers lead to:

- `WorldControllerPane::WorldPane, WorldPane::WorldPane_Impl, TimerHandler::WorldPane, and 1 other RTTI owner`
- `WorldControllerPane::WorldPane, WorldPane::WorldPane_Impl`

## Body

```text
packet CAttack {
    u8      opcode                    // 0x13
    ...                         // fields pending
}
```

Field order, variants, state effects, and paired packets remain to be traced.
