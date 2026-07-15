# Mercenary (`CMercenary`)

| Field | Value |
| --- | --- |
| Direction | Client to server |
| Opcode | `0x54` (84) |
| Common transform | derived |
| Representative builder | `net_send_mercenary_action` at `0x0045C500` |
| Opcode initializer | `net_init_mercenary_packet` at `0x0045D550` |
| Name provenance | Project-owner protocol name, confirmed against `EmployeeDialogPane` |

## Current evidence

Helper `0x0045D550` initializes opcode `0x54` and the first fields. The builder appends an action byte and a four-byte big-endian value before submitting a 12-byte body. The owner is `EmployeeDialogPane`, which supports the mercenary interpretation and distinguishes it from merchant menus.

The client has no derived packet RTTI for this name.

## Known send sites

- `0x0045C22D` in `sub_45C200`, a `TimerHandler::EmployeeDialogPane` virtual method.

## Plaintext body

```text
opcode:u8                 // 0x54
subtype:u8                // 1 in the initializer
employee_id:u32be
initializer_value:u8
action:u8
value:u32be
```

The final field roles remain to be verified.
