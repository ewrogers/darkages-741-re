# Request CRC (`SRequestCRC`)

| Item | Value |
| --- | --- |
| Direction | Server to client |
| Command | `0x3B` (59) |
| Encoding | derived |
| Name provenance | Microsoft C++ RTTI in the target |

## Purpose

The server sends a two-byte challenge and expects an immediate [`CReplyCRC`](../client/069-0x45-reply-crc.md) response. Despite the packet names, this exchange does not make the client checksum its executable, files, memory, or session state.

The RTTI-backed class confirms the body layout. The active global handler independently reparses the same value from the decoded byte buffer before constructing the reply.

## Body

```text
packet SRequestCRC {
    u8      opcode                    // 0x3B
    u16     challenge
}
```

`net_deserialize_request_crc_server_packet` reads the one big-endian value. The packet carries no algorithm selector, expected checksum, filename, range, or other input.

## Client response

`net_handle_request_crc_server_body` starts the custom CRC16 state at zero, feeds the challenge's low byte and then its high byte, and writes the result as a big-endian `CReplyCRC` value.

For this exact two-byte input, that calculation is equivalent to reversing the challenge bytes. See [Checksums](../checksums.md#request-challenge) for why the table-based update collapses to a byte swap.

The client saves no state from the request and performs no comparison. No failure or alternate response branch exists.
