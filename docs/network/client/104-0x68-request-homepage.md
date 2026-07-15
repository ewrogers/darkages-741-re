# Request Homepage (`CRequestHomepage?`)

| Field | Value |
| --- | --- |
| Direction | Client to server |
| Opcode | `0x68` (104) |
| Common transform | static |
| Representative builder | `0x004BA0C0` |
| Name provenance | The opcode and builder are locally confirmed. The class spelling is reconstructed from behavior and related terminology. |

## Current evidence

The representative builder at `0x004BA0C0` writes opcode `0x68` as body byte 0 and reaches `net_submit_client_packet`.

No concrete derived client packet RTTI class exists in this binary. The display name is therefore kept separate from the locally verified opcode evidence.

## Known send sites

- `0x4B88C9` in `sub_4b8890`; nearest RTTI owner not yet identified.
- `0x4B85A9` in `sub_4b8570`; nearest RTTI owner not yet identified.

## Plaintext body

```text
opcode:u8
... fields pending
```

Field order, variants, state effects, and paired packets remain to be traced.
