# Network receive and packet dispatch

## Confirmed framing

```text
[start/sync byte] [u16be body_size] [u8 opcode] [payload...]
```

The binary frame parser at `0x567070` discards the first byte without comparing it to `0xAA`. It assembles the following two bytes as a big-endian body size. The size includes the opcode byte.

## Receive path

```text
net_connect_and_initialize_transport (0x565210)
    Winsock initialization, connect, WSAAsyncSelect
    |
net_dispatch_communications_event (0x5643D0)
    communications event dispatch
    | case 5
net_process_incoming_transport_data (0x564870)
    transport selector
    | TCP transport type 5
net_receive_binary_framed_data (0x567070)
    binary frame parser
    |
net_decrypt_server_packet_body (0x567DE0)
    optional packet transformation/decryption
    |
net_queue_received_packet_bytes (0x467060)
    copy/queue completed packet
    |
net_dispatch_received_message (0x4647C0)
    message dispatch
    |
net_deserialize_server_packet (0x5963F0)
    opcode registry and packet-object deserialization
    |
net_dispatch_game_server_message (0x5ED990)
    dispatches using the raw body and/or RTTI packet object
```

## Dual raw-body and RTTI-object dispatch

The received-message wrapper retains two useful representations:

| Message offset | Representation |
|---:|---|
| `+0x14` | raw post-decrypt packet body, beginning with the opcode |
| `+0x1C` | optional RTTI-deserialized packet object |

An unregistered opcode can therefore produce no object at `+0x1C` and still be handled from the raw body at `+0x14`. `net_dispatch_game_server_message` manually checks unregistered opcodes `0x1B`, `0x31`, `0x34`, `0x35`, `0x36`, and `0x4F`. It also checks registered opcodes `0x06`, `0x2E`, `0x3B`, `0x3C`, and `0x42` through the raw representation.

This explains the previously missing `0x1B EnterEditingMode`: it is not out-of-band and does not use a second transport. It follows normal framing and decryption, then bypasses the RTTI packet factory and is parsed by `net_handle_s_enter_editing_mode` (`0x5F71C0`). The adjacent manual `0x35 SShowPaper` handler uses the same paper UI in read-only mode. Its close/ESC path skips `C 0x23` and dismisses the window locally.

## Lobby/login opcode caveat

The recovered packet-object registry contains no factories for server opcodes `0x00`, `0x01`, or `0x02`. All 61 calls to `net_register_server_packet_factory` originate in the one game registry constructor. Separately, the receive crypto switch recognizes `0x00` as raw and `0x01`/`0x02` as primary-key encrypted. The manual game handlers described above are a separate reason an opcode can be absent from the registry.

- `0x00 SVersionCheck` is consumed by the recovered raw handler `net_handle_s_version_check_raw` at `0x4B7F80`. Its subtype `0` installs the server-selected salt-table seed and replacement primary key. `0x02 SCheck` remains without an isolated payload handler.
- `0x01 SNewUserCheck?` has confirmed framing/decrypt support, while the class name and lobby semantics remain uncertain.
- `0x03 STransferServer` is locally RTTI-registered and is known to perform the lobby-to-game-server handoff.

`0x00-0x02` are consumed after decryption by connection-state/raw-message paths rather than the recovered game-server packet factory. The raw `0x00` path is now located; a lobby capture remains the cleanest way to isolate `0x01` and `0x02` fully.

`net_connect_and_initialize_transport` registers window message `0x401` with Winsock events `0x21` (`FD_READ | FD_CLOSE`).

## Communications-object offsets

| Offset | Preliminary meaning |
|---:|---|
| `+0x78` | receive-buffer pointer |
| `+0x48080` | current receive-buffer position |
| `+0x48084` | unread buffered-byte count |
| `+0x48088` | current declared body size |
| `+0x480CC` | TCP socket |
| `+0x480D1` | assembled body; byte 0 is opcode |
| `+0x580D4` | frame byte counter |
| `+0x780D8` | transport type |
| `+0x780D9` | frame-in-progress flag |

## Packet reader API

| Address | Recovered operation |
|---:|---|
| `net_packet_reader_read_u8` at `0x595C20` | read `u8` |
| `net_packet_reader_read_u16_be` at `0x595C60` | read `u16be` |
| `net_packet_reader_read_u24_be` at `0x595CA0` | read `u24be` |
| `net_packet_reader_read_u32_be` at `0x595CE0` | read `u32be` |
| `net_packet_reader_read_bytes` at `0x595D20` | copy a fixed number of bytes |
| `net_packet_reader_take_view` at `0x595D60` | return a zero-copy view and advance by N |
| `net_packet_reader_read_u8_sized_bytes` at `0x595D90` | read `u8` length plus bytes |
| `net_packet_reader_read_u16_sized_bytes` at `0x595DC0` | read `u16be` length plus bytes |
| `net_packet_reader_read_u8_string` at `0x595DF0` | read `u8`-length-prefixed string and append NUL |
| `net_packet_reader_current_ptr` at `0x595E50` | return a view of all remaining bytes |
| `net_packet_reader_init_from_remaining` at `0x595E90` | construct a subreader over the remaining bytes |

## Encryption/transform layer

`net_decrypt_server_packet_body` preserves the opcode, uses body byte 1 as a selector, removes three trailer bytes, and XORs trailer bytes with `0x74`, `0x24`, and `0x64` before invoking `net_xor_packet_bytes` at `0x568230`.

The full inverse transform and its asymmetric client/server trailer constants are documented in [Packet encryption, decryption, and CRC reconstruction](./packet-crypto-and-crc.md).

## IDA naming convention

Network-system functions use a `net_` prefix. Provisional interpretations use `maybe_` in identifiers and question marks in comments because `?` is not valid inside an IDA symbol.

Some opcodes bypass this layer or select different transform modes. Those mode assignments should be documented alongside the known server encryption implementation.
