# Meta Data (`CMetaData`)

| Item | Value |
| --- | --- |
| Direction | Client to server |
| Command | `0x7B` (123) |
| Encoding | startup key |
| Name provenance | The class name comes from related class vocabulary matched to the locally confirmed builder behavior. |

## Purpose

The client sends this message for **meta data**.

## Sent by

Known static callers lead to:

- `TimerHandler::NPCIllustFileMan, TimerHandler::MetaOptions, TimerHandler::DeniedItemList, and 2 other RTTI owners`
- `TimerHandler::MetaTableManager`

## Body

```text
packet CMetaData {
    u8 opcode                 // 0x7B
    ...                         // fields pending
}
```

Remaining fields, variants, and state effects remain to be traced.

The paired response is [Meta Data (`SMetaData`)](../server/111-0x6f-meta-data.md).
