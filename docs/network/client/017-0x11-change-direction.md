# Change Direction (`CChangeDirection`)

| Field | Value |
| --- | --- |
| Direction | Client to server |
| Opcode | `0x11` (17) |
| Common transform | derived |
| Representative builder | `net_send_change_direction` at `0x005F4510` |
| Name provenance | Project-owner protocol name, confirmed against the world input path |

## Current evidence

The builder writes opcode `0x11` followed by one direction byte and submits a two-byte body.

The client has no derived packet RTTI for this name.

## Known send sites

- `0x005F093F` in `sub_5F0900`. Its nearest confirmed RTTI owners are `WorldControllerPane::WorldPane`, `WorldPane::WorldPane_Impl`, and their timer handlers.

## Plaintext body

```text
opcode:u8                 // 0x11
direction:u8
```
