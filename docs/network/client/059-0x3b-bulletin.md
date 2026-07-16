# Bulletin (`CBulletin`)

| Item | Value |
| --- | --- |
| Direction | Client to server |
| Command | `0x3B` (59) |
| Encoding | session key |
| Name provenance | The class name comes from related class vocabulary matched to the locally confirmed builder behavior. |

## Purpose

The client sends this message for **bulletin**.

## Sent by

Known static callers lead to:

- `Pane::BtmButtonsPane_A, BtmButtonsPane_A::GUIBackPane::_BtmButtonsPane`

## Body

```text
packet CBulletin {
    u8 opcode                 // 0x3B
    ...                         // fields pending
}
```

Field order, variants, state effects, and paired packets remain to be traced.
