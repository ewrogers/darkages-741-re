# Move Object (`SMoveObject`)

<a id="purpose"></a>

`SMoveObject` is a registered server message whose name suggests object movement. Its fields and gameplay effects remain untraced, so the name alone does not establish how it moves an object.

| Item | Value |
| --- | --- |
| Direction | Server to client |
| Command | `0x0C` (12) |
| Transform | `derived` |
| Name provenance | Microsoft C++ RTTI in the target |

## Body

```text
packet SMoveObject {
    u8      opcode                    // 0x0C
    ...                         // fields pending
}
```

The class deserializer, field layout, gameplay handler, state effects, and paired client packet remain to be traced.

## Name evidence

The constructor calls `net_server_packet_base_ctor` with opcode `0x0C` and installs the `SMoveObject` vtable. `net_server_packet_factory_ctor` registers the same opcode with this constructor.
