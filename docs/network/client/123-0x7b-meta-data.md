# Meta Data (`CMetaData`)

| Field | Value |
| --- | --- |
| Direction | Client to server |
| Opcode | `0x7B` (123) |
| Common transform | static |
| Representative builder | `0x004E52F0` |
| Name provenance | The class name comes from related class vocabulary matched to the locally confirmed builder behavior. |

## Current evidence

The representative builder at `0x004E52F0` writes opcode `0x7B` as body byte 0 and reaches `net_submit_client_packet`.

No concrete derived client packet RTTI class exists in this binary. The display name is therefore kept separate from the locally verified opcode evidence.

## Known send sites

- `0x4E4AB1` in `sub_4e4a90`, reachable from `TimerHandler::NPCIllustFileMan`, `TimerHandler::MetaOptions`, `TimerHandler::DeniedItemList`, and 2 other RTTI owners.
- `0x4E4A74` in `sub_4e4a50`, reachable from `TimerHandler::MetaTableManager`.

## Plaintext body

```text
opcode:u8
... fields pending
```

Remaining fields, variants, and state effects remain to be traced.

The paired response is [Meta Data (`SMetaData`)](../server/111-0x6f-meta-data.md).
