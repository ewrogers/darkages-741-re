# Self Look (`CSelfLook`)

| Item | Value |
| --- | --- |
| Direction | Client to server |
| Command | `0x2D` (45) |
| Encoding | startup key |
| Name provenance | The class name comes from related class vocabulary matched to the locally confirmed builder behavior. |

## Purpose

The client sends this message for **self look**.

## Sent by

Known static callers lead to:

- `Pane::BtmButtonsPane_A, BtmButtonsPane_A::GUIBackPane::_BtmButtonsPane`
- UI or subsystem owner not known yet
- `TimerHandler::BtmButtonsPane_A, TimerHandler::GUIBackPane::_BtmButtonsPane`

## Body

```text
packet CSelfLook {
    u8 opcode                 // 0x2D
    ...                         // fields pending
}
```

Field order, variants, state effects, and paired packets remain to be traced.
