# Network architecture

The active transport opens with a blocking 32-bit Winsock TCP `connect`, then registers the socket with the window through `WSAAsyncSelect` for event-driven I/O. Application code exchanges opcode-first packet bodies. The socket layer applies the direction-specific transform, adds or removes framing, and moves decoded server bodies into the main event system.

All addresses are static virtual addresses for preferred image base `0x00400000`.

## Client-to-server path

| Stage | Address | Role |
| --- | --- | --- |
| Inline packet builders | many | Write the opcode at body byte 0, append fields, and submit the plaintext body |
| `net_submit_client_packet` | `0x00563E00` | Copies the body into the socket event queue; opcodes `0x39` and `0x3A` receive an extra CRC-bearing wrapper |
| `net_socket_dispatch` | `0x005643D0` | Routes socket command 6 to the framed sender |
| `net_send_client_packet` | `0x005648A0` | Selects raw, static-key, or derived-key handling from the outbound opcode |
| `net_encrypt_client_packet` | `0x00567FB0` | Applies the rolling selector, XOR passes, MD5 check bytes, and seed trailer |
| Winsock `send` | `0x00564A67` | Sends the final frame |

The binary client-to-server frame is:

```text
AA body_size:u16be body[body_size]
```

The `0xAA` marker and size are added only after transformation. Raw opcodes keep their plaintext body unchanged. Transformed bodies are described in [Packet transforms](packet-transforms.md).

The same socket class retains an older printable compatibility transport using `net_send_text`, `net_send_byte`, and a separate receive state machine. The normal TCP configuration uses the binary framing path above.

## Server-to-client path

| Stage | Address | Role |
| --- | --- | --- |
| Winsock `recv` | `0x00567918` | Refills a `0x18000`-byte socket buffer |
| `net_read_transport_byte` | `0x00567870` | Serves one byte at a time from the buffered transport |
| `net_receive_frames` | `0x00567070` | Consumes a sync byte, reads `body_size:u16be`, collects the body, and selects its transform |
| `net_decrypt_server_packet` | `0x00567DE0` | Reverses the server transform and removes its seed trailer |
| `net_post_decoded_server_packet_event` | `0x00467060` | Copies the decoded opcode-first body into event type `0x13` |
| `event_process_queued_event` | `0x004647C0` | Retains the decoded body and creates a server packet object when the opcode has a registered constructor |
| UI or manager event handlers | varies | Consume selected decoded bodies directly when no packet class is registered |
| `net_dispatch_server_packet` | `0x005ED990` | Routes registered, parsed gameplay packets to handlers |

The receive state machine discards the first frame byte as a sync marker but does not compare it with `0xAA`. It then reads the next two bytes as the big-endian body size. A malformed stream can therefore desynchronize without failing at the marker itself.

## Packet classes and RTTI

The binary contains RTTI for the socket, packet reader, server packet base, client packet base, server packet factory, and 61 concrete server packet classes.

`net_server_packet_factory_ctor` at `0x00595F00` registers those 61 constructors in a 256-entry opcode table. `net_deserialize_server_packet` at `0x005963F0` creates the registered class, builds a packet reader, and invokes vtable slot `+8` to parse the body. This gives the [server packet index](server/README.md) direct class-name and opcode evidence.

Absence from that table does not mean an opcode is unused. `SVersionCheck`, `SNewUserCheck`, `SLoginCheck`, and `SMetaData` remain decoded byte buffers in the event and are consumed directly by `MainMenuPane`, `CreateUserDialogPane`, or `MetaTableManager`. Those owner classes have RTTI, but the packet buffers do not become concrete RTTI packet objects.

Only the base client packet RTTI type exists. Client packets are assembled inline, so the [client packet index](client/README.md) uses locally verified builder opcodes and separately records the provenance of friendly names.

## Useful observation points

For tooling that observes rather than changes protocol behavior:

- `net_submit_client_packet` sees most outbound plaintext bodies before common transformation.
- `net_send_client_packet` is the authoritative outbound transform-policy boundary.
- `net_post_decoded_server_packet_event` sees inbound bodies after common decryption.
- `net_deserialize_server_packet` is the server class factory and parser boundary.
- UI and manager event dispatchers are the parser boundary for out-of-factory packets.
- The Winsock calls see only framed wire bytes.

The decoded event path is usually the safest place to inspect packet contents because it avoids reimplementing framing and both XOR modes. The two indexes deliberately remain direction-specific because the same opcode can have a different name and transform policy in each direction.
