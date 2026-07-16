# Version (`CVersion`)

| Item | Value |
| --- | --- |
| Direction | Client to server |
| Command | `0x00` (0) |
| Encoding | none |
| Name provenance | The class name comes from related class vocabulary matched to the locally confirmed builder behavior. |

## Purpose

The client sends this message for **version**.

## Sent by

Known static callers lead to:

- UI or subsystem owner not known yet

## Body

```text
packet CVersion {
    u8 opcode                 // 0x00
    ...                         // fields pending
}
```

Remaining fields, variants, and state effects remain to be traced.

The paired response is [Version Check (`SVersionCheck`)](../server/000-0x00-version-check.md).
