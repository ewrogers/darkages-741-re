# Web Board (`CWebBoard`)

| Field | Value |
| --- | --- |
| Direction | Client to server |
| Opcode | `0x73` (115) |
| Common transform | static |
| Representative builder | `0x004160A0` |
| Name provenance | The class name comes from related class vocabulary matched to the locally confirmed builder behavior. |

## Current evidence

The representative builder at `0x004160A0` writes opcode `0x73` as body byte 0 and reaches `net_submit_client_packet`.

No concrete derived client packet RTTI class exists in this binary. The display name is therefore kept separate from the locally verified opcode evidence.

## Known send sites

- `0x415F7A` in `sub_415cb0`; nearest RTTI owner not yet identified.

## Plaintext body

```text
opcode:u8
... fields pending
```

Field order, variants, state effects, and paired packets remain to be traced.
