# Emotion (`CEmotion`)

| Item | Value |
| --- | --- |
| Direction | Client to server |
| Command | `0x1D` (29) |
| Encoding | session key |
| Name provenance | The class name comes from related class vocabulary matched to the locally confirmed builder behavior. |

## Purpose

The client sends this message for **emotion**.

## Sent by

Known static callers lead to:

- `WorldControllerPane::WorldPane, WorldPane::WorldPane_Impl`
- `MapInterface::WorldPane_Impl`

## Body

```text
packet CEmotion {
    u8      opcode                    // 0x1D
    ...                         // fields pending
}
```

Field order, variants, state effects, and paired packets remain to be traced.
