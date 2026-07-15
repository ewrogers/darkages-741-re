# Put Ground (`CPutGround`)

| Field | Value |
| --- | --- |
| Direction | Client to server |
| Opcode | `0x0C` (12) |
| Common transform | derived |
| Representative builder | `net_send_put_ground` at `0x005F4430` |
| Name provenance | Project-owner protocol name, confirmed against the local builder |

## Current evidence

The builder writes opcode `0x0C`, a four-byte big-endian value, and submits a five-byte body. The value's exact object or item role remains to be confirmed from its callers.

The client has no derived packet RTTI for this name.

## Known send sites

- `0x005F3E52` in `sub_5F3E00`; owner not yet identified.
- `0x005F3A39` in `sub_5F3930`; owner not yet identified.
- `0x005F3C0E` in `sub_5F3BB0`; owner not yet identified.

## Plaintext body

```text
opcode:u8                 // 0x0C
value:u32be
```
