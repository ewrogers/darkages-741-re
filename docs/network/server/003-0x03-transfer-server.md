# Transfer Server (`STransferServer`)

| Item | Value |
| --- | --- |
| Direction | Server to client |
| Command | `0x03` (3) |
| Transform | `raw` |
| Name provenance | Microsoft C++ RTTI in the target |

## Purpose

This packet moves the client from the bootstrap server to another endpoint. It carries the new IPv4 address and port plus an opaque handoff token.

The constructor calls `net_server_packet_base_ctor` with opcode `0x03` and installs the `STransferServer` vtable. `net_server_packet_factory_ctor` registers the same opcode with this constructor.

`net_deserialize_transfer_server_packet` fills an `STransferServer` object. The main-menu dispatcher passes that object to `net_handle_transfer_server`, which closes the current TCP connection, connects to the supplied endpoint, and sends [Transfer Server (`CTransferServer`)](../client/016-0x10-transfer-server.md) on the new connection.

## Body

```c
packet STransferServer {
    u8 opcode;                 // 0x03
    u32be ipv4_value;
    u16be port;
    u8 token_length;
    u8 token[token_length];
}
```

The IPv4 integer is stored in the little-endian socket state without another byte swap. In the observed exchange, `01 00 00 7F` becomes `127.0.0.1`, and `0A 32` is port `2610`.

The observed token has length `0x1B`:

```text
02 09 5E 6B 62 70 56 5B 5F 7D 71 0B
73 6F 63 6B 65 74 5B 32 35 36 5D 00 00 07 22
```

Some bytes resemble protocol state, including the selected seed table, the nine-byte key, and a length-prefixed string. The client does not parse them here, so the token remains intentionally opaque.
