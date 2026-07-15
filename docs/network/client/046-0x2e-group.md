# Group (`CGroup`)

| Field | Value |
| --- | --- |
| Direction | Client to server |
| Opcode | `0x2E` (46) |
| Common transform | derived |
| Representative builder | `net_send_group` at `0x00462DC0` |
| Name provenance | Project-owner protocol name, confirmed against the User Look dialog path |

## Current evidence

The builder writes opcode `0x2E`, action `2`, and a length-prefixed user name taken from the owning dialog. This protocol uses “group,” not “party.”

The client has no derived packet RTTI for this name.

## Known send sites

- `0x00461F91` in `sub_461F40`, a virtual method of `DialogPane::UserLookPane`.

## Plaintext body

```text
opcode:u8                 // 0x2E
action:u8                 // 2 in this builder
name_length:u8
name:u8[name_length]
```
