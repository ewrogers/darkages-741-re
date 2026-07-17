# Request Portrait (`SRequestPortrait`)

| Item | Value |
| --- | --- |
| Direction | Server to client |
| Command | `0x49` (73) |
| Encoding | session key |
| Name provenance | Microsoft C++ RTTI in the target |

## Purpose

The server asks the client to upload the current character's local portrait and profile text.

The constructor calls `net_server_packet_base_ctor` with opcode `0x49` and installs the `SRequestPortrait` vtable. `net_server_packet_factory_ctor` registers the same opcode with this constructor.

## Body

```text
packet SRequestPortrait {
    u8      opcode                    // 0x49, no body fields
}
```

`net_server_request_portrait_deserialize` is empty. `UserInfoPane` handles the decoded packet and immediately sends `CSendPortrait`.

See [Portraits and profiles](../../systems/portraits-and-profiles.md) for the complete request and response flow.
