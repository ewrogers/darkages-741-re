# Reply CRC (`CReplyCRC`)

| Field | Value |
| --- | --- |
| Direction | Client to server |
| Opcode | `0x45` (69) |
| Common transform | derived |
| Representative builder | `0x005F2CF0` |
| Name provenance | The class name comes from related class vocabulary matched to the locally confirmed builder behavior. |

## Current evidence

The representative builder at `0x005F2CF0` writes opcode `0x45` as body byte 0 and reaches `net_submit_client_packet`.

No concrete derived client packet RTTI class exists in this binary. The display name is therefore kept separate from the locally verified opcode evidence.

## Known send sites

- `0x5EDD5C` in `net_dispatch_server_packet`; nearest RTTI owner not yet identified.

## Plaintext body

```text
opcode:u8
... fields pending
```

Field order, variants, state effects, and paired packets remain to be traced.
