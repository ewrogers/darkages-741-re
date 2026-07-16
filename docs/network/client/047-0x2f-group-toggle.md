# Group Toggle (`CGroupToggle`)

| Item | Value |
| --- | --- |
| Direction | Client to server |
| Command | `0x2F` (47) |
| Encoding | session key |
| Name provenance | Verified project protocol name; the command and local builder are confirmed. |

## Purpose

The client sends this message for **group toggle**.

## Sent by

Known static callers lead to:

- `Pane::BtmButtonsPane_A, BtmButtonsPane_A::GUIBackPane::_BtmButtonsPane`

## Body

```text
packet CGroupToggle {
    u8 opcode                 // 0x2F
    ...                         // fields pending
}
```

Field order, variants, state effects, and paired packets remain to be traced.
