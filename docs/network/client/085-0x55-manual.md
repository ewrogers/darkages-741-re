# Manual (`CManual`)

| Item | Value |
| --- | --- |
| Direction | Client to server |
| Command | `0x55` (85) |
| Encoding | session key |
| Name provenance | Project-owner protocol name, confirmed by `ManufactureDialogPane` and `SManual` |

## Purpose

The client sends this message for **manual**.

All known calls belong to the manufacture interface. This confirms a crafting or manufacture role and supports pairing the client request with server [`SManual`](../server/080-0x50-manual.md). The previous `CBlackSmith` reconstruction came only from related vocabulary and has been removed.

The client has no derived packet RTTI for this name.

## Sent by

Known static callers lead to:

- `DialogPane::ManufactureDialogPane`
- UI or subsystem owner not known yet

## Body

```text
packet CManual {
    u8      opcode                    // 0x55
    u8      dialog_value_0
    u8      dialog_value_1
    u8      reserved                  // 0
    u8      action
}
```
