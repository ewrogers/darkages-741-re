# Mercenary (`CMercenary`)

| Item | Value |
| --- | --- |
| Direction | Client to server |
| Command | `0x54` (84) |
| Encoding | session key |
| Name provenance | Project-owner protocol name, confirmed against `EmployeeDialogPane` |

## Purpose

The client sends this message for **mercenary**.

A helper initializes command `0x54` and the first fields. The builder appends an action byte and a four-byte big-endian value before submitting a 12-byte body. The owner is `EmployeeDialogPane`, which supports the mercenary interpretation and distinguishes it from merchant menus.

The client has no derived packet RTTI for this name.

## Sent by

Known static callers lead to:

- UI or subsystem owner not known yet

## Body

```text
packet CMercenary {
    u8 opcode                 // 0x54
    u8 subtype                // 1 in the initializer
    u32be employee_id
    u8 initializer_value
    u8 action
    u32be value
}
```

The final field roles remain to be verified.
