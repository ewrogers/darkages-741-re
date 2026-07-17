# Request Object Info (`CRequestObjectInfo`)

| Item | Value |
| --- | --- |
| Direction | Client to server |
| Command | `0x43` (67) |
| Encoding | startup key |
| Name provenance | Project-owner protocol name, confirmed against merchant menu object-selection paths |

## Purpose

The client sends this message for **request object info**.

The builder sends opcode `0x43`, literal subtype `1`, and a four-byte big-endian object identifier.

The client has no derived packet RTTI for this name.

## Sent by

Known static callers lead to:

- merchant object-selection paths
- the world-object click handler

For clicked user objects, the local `UserClickMode` setting can suppress this request. Other object categories continue through their normal click paths.

## Body

```text
packet CRequestObjectInfo {
    u8      opcode                    // 0x43
    u8      subtype                   // 1 in this builder
    u32     object_id
}
```
