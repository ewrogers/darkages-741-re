# Request Object Info (`CRequestObjectInfo`)

| Field | Value |
| --- | --- |
| Direction | Client to server |
| Opcode | `0x43` (67) |
| Common transform | static |
| Representative builder | `net_request_object_info` at `0x004CD350` |
| Name provenance | Project-owner protocol name, confirmed against merchant menu object-selection paths |

## Current evidence

The builder sends opcode `0x43`, literal subtype `1`, and a four-byte big-endian object identifier.

The client has no derived packet RTTI for this name.

## Known send sites

- `0x004CE246` in `sub_4CE220`. It is shared by RTTI-backed merchant task, text, item, spell, skill, face, and input menu dialogs.

## Plaintext body

```text
opcode:u8                 // 0x43
subtype:u8                // 1 in this builder
object_id:u32be
```
