# Version (`CVersion`)

| Field | Value |
| --- | --- |
| Direction | Client to server |
| Opcode | `0x00` (0) |
| Common transform | raw |
| Representative builder | `0x00579090` |
| Name provenance | The class name comes from related class vocabulary matched to the locally confirmed builder behavior. |

## Current evidence

The representative builder at `0x00579090` writes opcode `0x00` as body byte 0 and reaches `net_submit_client_packet`.

No concrete derived client packet RTTI class exists in this binary. The display name is therefore kept separate from the locally verified opcode evidence.

## Known send sites

- `0x00579090` is an indirect virtual send method referenced by `Pane::TerminalPane2` at `0x685BB4`.

## Plaintext body

```text
opcode:u8
... fields pending
```

Remaining fields, variants, and state effects remain to be traced.

The paired response is [Version Check (`SVersionCheck`)](../server/000-0x00-version-check.md).
