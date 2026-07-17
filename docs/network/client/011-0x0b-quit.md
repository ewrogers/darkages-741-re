# Quit (`CQuit`)

| Item | Value |
| --- | --- |
| Direction | Client to server |
| Command | `0x0B` (11) |
| Encoding | startup key |
| Name provenance | The class name comes from related class vocabulary matched to the locally confirmed builder behavior. |

## Purpose

The client sends this message for **quit**.

## Sent by

Known static callers lead to:

- `Pane::MainMenuPane`
- UI or subsystem owner not known yet
- `DialogPane::AgreementDialogPane`

## Body

```text
packet CQuit {
    u8      opcode                    // 0x0B
    ...                         // fields pending
}
```

Field order, variants, state effects, and paired packets remain to be traced.
