# Use Spell (`CUseSpell`)

| Item | Value |
| --- | --- |
| Direction | Client to server |
| Command | `0x0F` (15) |
| Encoding | session key |
| Name provenance | The class name comes from related class vocabulary matched to the locally confirmed builder behavior. |

## Purpose

The client sends this message for **use spell**.

## Sent by

Known static callers lead to:

- `BatchJob::BulletinBangUserBatchJob`

## Body

```text
packet CUseSpell {
    u8      opcode                    // 0x0F
    ...                         // fields pending
}
```

Field order, variants, state effects, and paired packets remain to be traced.
