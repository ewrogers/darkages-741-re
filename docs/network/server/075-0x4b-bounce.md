# Bounce (`SBounce`)

`SBounce` lets the server supply a complete opcode-first client body and ask the client to transmit it. The client does not interpret the embedded command. It feeds those bytes directly into the ordinary client send path.

| Item | Value |
| --- | --- |
| Direction | Server to client |
| Command | `0x4B` (75) |
| Transform | derived |
| Session owner | `WorldUserFunc` |
| Handler | `net_handle_bounce_server_packet` |
| Name provenance | Microsoft C++ RTTI in the target |

## Body

```text
packet SBounce {
    u8      opcode                    // 0x4B
    u16     body_length
    bytes   client_body[body_length]
}
```

`client_body` begins with the client opcode that should be sent. The outer `SBounce` opcode and `body_length` are not included in the response.

## Client flow

The parser retains a view of the counted bytes instead of copying them into a fixed packet structure. The active handler is equivalent to:

```c
bool handle_bounce(SBounce *packet) {
    net_submit_client_packet(packet->client_body,
                             packet->body_length);
    return true;
}
```

There is no dispatch to a client packet builder, no opcode whitelist, and no semantic check of the embedded fields. This is why there is no single paired `CBounce` packet. The response is whichever client body the server placed inside `SBounce`.

## What the client adds

The embedded body is not copied directly to the wire. Once submitted, it receives the same processing as a locally built client packet:

- For an ordinary body, `net_submit_client_packet` appends the common transmitted zero byte.
- Embedded opcodes `0x39` and `0x3A` enter their existing randomized CRC-wrapper path instead.
- The embedded opcode selects the normal client-to-server `raw`, `static`, or `derived` transform.
- A `static` or `derived` result consumes the next client send `sequence`. A `raw` result does not.
- The transport adds the normal `0xAA` and `u16` frame header before sending.

The incoming `SBounce` has already used the independent server-to-client sequence because its own transform is `derived`. The handler does not copy or synchronize the two sequence values.

Beyond that transport work, the client changes no game state, session setting, UI, timer, key, file, or checksum state.

## Validity and limits

The `SBounce` path does not compare `body_length` with the remaining decoded bytes, and the handler does not reject a zero length. The downstream sender reads the first embedded byte as an opcode, so a valid message needs at least one complete opcode-first body.

The RTTI name confirms the term `SBounce`, but the intended server-side use is not visible in the client. The confirmed behavior is server-directed client packet submission, not a byte-for-byte wire echo. See [Transport](../transport.md) for the common framing and transform stages.
