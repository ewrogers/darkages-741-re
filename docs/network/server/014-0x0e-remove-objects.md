# Remove Objects (`SRemoveObjects`)

<a id="purpose"></a>

`SRemoveObjects` is a registered server message whose name suggests object removal. Its fields and gameplay effects remain untraced, including which objects it can remove.

| Item | Value |
| --- | --- |
| Direction | Server to client |
| Command | `0x0E` (14) |
| Transform | `derived` |
| Name provenance | Microsoft C++ RTTI in the target |

## Body

```text
packet SRemoveObjects {
    u8      opcode                    // 0x0E
    ...                         // fields pending
}
```

The class deserializer, field layout, gameplay handler, state effects, and paired client packet remain to be traced.

## Name evidence

The constructor calls `net_server_packet_base_ctor` with opcode `0x0E` and installs the `SRemoveObjects` vtable. `net_server_packet_factory_ctor` registers the same opcode with this constructor.
