# Self Save OK (`SSelfSaveOK`)

`SSelfSaveOK` is an empty acknowledgement packet. The client can decode and construct it, but the current gameplay dispatcher has no packet-specific handler for opcode `0x21`.

| Item | Value |
| --- | --- |
| Direction | Server to client |
| Command | `0x21` (33) |
| Transform | `derived` |
| Concrete class | RTTI class `SSelfSaveOK` |
| Gameplay owner | None found |
| Name provenance | Exact client RTTI |

## Body

```text
packet SSelfSaveOK {
    u8      opcode                    // 0x21
}
```

The concrete object is only the size of the common server-packet base. Its vtable uses the inherited base deserializer, so it consumes no body fields after the opcode.

## Client handling

`net_server_packet_factory_ctor` registers opcode `0x21`, and `net_create_self_save_ok_server_packet` constructs the exact RTTI-backed class. This lets the normal receive path recognize and decode the packet.

`net_dispatch_server_packet` has no parsed or raw `0x21` branch. The packet reaches the normal unhandled return without changing gameplay state or UI state. No other packet-specific consumer was found through the class, constructor, or vtable references.

The exact RTTI name labels this as a successful self-save acknowledgement, but the version 741 client does not display or act on it after receipt. A matching client request and the server-side purpose of the acknowledgement remain unresolved.
