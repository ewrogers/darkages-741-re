# Request Object Info (`CRequestObjectInfo`)

`CRequestObjectInfo` asks the server for another world object's user-info view.

| Item | Value |
| --- | --- |
| Direction | Client to server |
| Opcode | `0x43` |
| Transform | `static` |
| Name provenance | Project-owner protocol name, confirmed against merchant menu object-selection paths |
| UI owner | World-object click and merchant object-selection paths |

The builder sends opcode `0x43`, literal subtype `1`, and a four-byte big-endian object identifier.

The client has no derived packet RTTI for this name.

The matching server response is the provisional owner-named [`SObjectInfo`](../server/052-0x34-object-info.md). That response resolves this `object_id` to a living world object and opens exact RTTI `UserInfoPane_ForOthers`.

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
