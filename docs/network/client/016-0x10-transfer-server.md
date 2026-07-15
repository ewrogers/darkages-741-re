# Transfer Server (`CTransferServer`)

| Field | Value |
| --- | --- |
| Direction | Client to server |
| Opcode | `0x10` (16) |
| Common transform | raw |
| Representative builder | `0x004B9510` |
| Name provenance | The class name comes from related class vocabulary matched to the locally confirmed builder behavior. |

## Current evidence

The representative builder at `0x004B9510` writes opcode `0x10` as body byte 0 and reaches `net_submit_client_packet`.

No concrete derived client packet RTTI class exists in this binary. The display name is therefore kept separate from the locally verified opcode evidence.

## Known send sites

- `0x4B8C55` in `net_dispatch_main_menu_events`; nearest RTTI owner not yet identified.

## Plaintext body

```text
opcode:u8
... fields pending
```

Field order, variants, state effects, and paired packets remain to be traced.
