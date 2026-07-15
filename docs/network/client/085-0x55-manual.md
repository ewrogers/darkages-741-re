# Manual (`CManual`)

| Field | Value |
| --- | --- |
| Direction | Client to server |
| Opcode | `0x55` (85) |
| Common transform | derived |
| Representative builder | `net_send_manual_action` at `0x004C26D0` |
| Name provenance | Project-owner protocol name, confirmed by `ManufactureDialogPane` and `SManual` |

## Current evidence

All known calls belong to the manufacture interface. This confirms a crafting or manufacture role and supports pairing the client request with server [`SManual`](../server/080-0x50-manual.md). The previous `CBlackSmith` reconstruction came only from related vocabulary and has been removed.

The client has no derived packet RTTI for this name.

## Known send sites

- `0x004C2C78` in `sub_4C2BC0`, reachable from `DialogPane::ManufactureDialogPane`.
- `0x004C2AAC` in `sub_4C2990`; owner not yet identified independently.
- `0x004C30E6`, `0x004C3131`, `0x004C3191`, and `0x004C3211` in `sub_4C30A0`, a `ManufactureDialogPane` virtual method.
- `0x004C3295` and `0x004C32C8` in `sub_4C3230`, another `ManufactureDialogPane` virtual method.

## Plaintext body

```text
opcode:u8                 // 0x55
dialog_value_0:u8
dialog_value_1:u8
reserved:u8               // 0
action:u8
```
