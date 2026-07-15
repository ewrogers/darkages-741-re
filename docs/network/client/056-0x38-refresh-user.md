# Refresh User (`CRefreshUser`)

| Field | Value |
| --- | --- |
| Direction | Client to server |
| Opcode | `0x38` (56) |
| Common transform | derived |
| Representative builder | `net_send_refresh_user` at `0x005F4640` |
| Name provenance | Project-owner protocol name, confirmed against the world pane paths |

## Current evidence

The builder submits a one-byte body containing only opcode `0x38`.

The client has no derived packet RTTI for this name.

## Known send sites

- `0x005F14B4` and `0x005F14E5` in `sub_5F1480`, a virtual method shared by `WorldControllerPane::WorldPane` and `WorldPane::WorldPane_Impl`.
- `0x005F306B` in `sub_5F2FC0`; owner not yet identified.

## Plaintext body

```text
opcode:u8                 // 0x38
```
