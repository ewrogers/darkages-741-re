# Network transport

Normal game traffic uses framed packet bodies. The first server receive is a special case: the client passes the received wire bytes to a terminal-compatible greeting handler before it enables ordinary frame parsing.

## Initial connection receive

A new socket starts with `raw_stream_mode` enabled. On the active TCP path, `net_receive_frames` then copies the complete `recv` buffer into a network event without checking its frame header, command, or transform.

The observed [Hello (`SHello`)](server/126-0x7e-hello.md) is still a standard binary frame on the wire. Its body contains the escape sequence `0x1B 'C'` inside readable greeting text. `TerminalPane2` scans for that sequence, selects binary framing, and clears raw-stream mode. The frame header and opcode `0x7E` are present but are not part of the client's welcome check.

An `0x1B 'S'` command instead selects the legacy printable framing described below. It is a transport encoding, not a language or character encoding. Its intended historical transport remains unconfirmed.

## Legacy printable frame

The alternate path is fully compiled and directly reachable through `ESC S`. It applies the normal opcode-based transform first, then splits the transformed packet body into printable records. The printable envelope replaces the binary `0xAA + u16be length` header. It does not include that header in the encoded bytes.

This means the packet protocol does not change. Raw opcodes remain raw. Static- and derived-key packets still carry their normal sequence and trailer bytes, and they advance the same encrypted-packet sequence used with binary framing.

This support is not confined to an unused helper. The active TCP receiver can collect printable records after `ESC S`, and the separately compiled `net_receive_serial_modem_data` receiver calls the same decoder for serial transport selectors.

The executable names its transport choices directly:

| Selector | Displayed transport | Compiled path |
| ---: | --- | --- |
| 1 through 4 | `MODEM COM1` through `MODEM COM4` | Windows serial port |
| 5 | `PPP or LAN` | Winsock TCP |

`net_open_serial_modem_transport` builds `COM%d`, opens it with `CreateFileA`, and configures serial buffers, timeouts, baud rate, 8-N-1 defaults, and flow control. Its receiver first passes the greeting through raw-stream mode. Once the greeting clears that mode, later serial traffic is collected as printable records and sent through the normal packet transform and event path.

The matching 7.41 configuration selects transport 5, and the observed server selects `ESC C`. This proves the modem-compatible system remains fully compiled without proving which earlier game or service originally required it.

```text
struct PrintableRecord {
    u8 marker              // '*' for first record, '+' for continuation
    u8 record_sequence     // ASCII '0' through '9', advances modulo 10
    u8 group_count         // ASCII '1' through ':', where ':' means 10
    u8 encoded[]           // four printable bytes per three input bytes
    u8 terminator          // ',' when more records follow, '.' on the last
    u8 newline             // 0x0A
}
```

The ASCII `record_sequence` belongs only to the printable envelope. It is separate from the encrypted-packet sequence stored inside transformed packet bodies. An encrypted packet sent this way therefore participates in both counters.

Each record carries at most ten three-byte groups, or 30 transformed bytes. Every three input bytes become four six-bit values. The encoder adds `0x3B` to each value, producing its private printable alphabet. This resembles Base64 grouping but does not use the Base64 alphabet.

One or two remaining input bytes are padded with zero six-bit values, encoded as `0x3B`. The decoder rebuilds complete three-byte groups, so its output length is rounded up to a multiple of three.

The receiver collects `*` and `+` records until the final period. `net_decode_printable_frames` validates the decimal record sequence and the sum of the advertised group counts before returning the reconstructed transformed body. The client reads its opcode, applies the normal server transform policy, and posts it through the same decoded-packet event path used by binary frames. This is application-level packet splitting and reassembly, independent of how TCP divides data into receives.

## Binary frame

```text
struct PacketFrame {
    u8 marker              // 0xAA when sent by this client
    u16be body_size
    u8 body[body_size]
}
```

The receive state machine discards the first byte as a sync marker but does not confirm that it equals `0xAA`. It then reads the big-endian body size and collects that many bytes.

## Client to server

```text
game packet builder
  -> net_submit_client_packet
  -> net_send_client_packet
  -> optional packet transform
  -> add AA and body size
  -> TCP send
```

Most builders create an opcode-first plaintext body and pass it to `net_submit_client_packet`. Opcodes `0x39` and `0x3A` receive an extra randomized CRC wrapper there. This wrapper is separate from the common packet transform.

`net_send_client_packet` chooses no transform, the startup key, or the session key. The final TCP frame is added after that choice.

Encrypted client packets use a one-byte outgoing sequence. The client writes the current value and increments it for the next encrypted packet. The server tracks those packets with its own receive counter, which advances in step but is separate state. Incoming encrypted server packets use the other direction's sequence, so receive traffic does not advance the client send counter. Raw packets advance neither encrypted sequence.

## Server to client

```text
first TCP receive
  -> raw wire-byte event
  -> TerminalPane2 escape handler
  -> select framing and clear raw-stream mode

later TCP receive
  -> net_receive_frames
  -> optional packet transform
  -> net_post_decoded_server_packet_event
  -> event_dispatch
  -> packet class or direct handler
```

After the greeting, socket data is buffered and consumed by `net_receive_frames`. A decoded opcode-first body becomes event type `0x13`, so the normal main-thread event system can deliver it to game code.

## Server packet classes

The client contains RTTI for a server packet base, a packet factory, and 61 concrete server packet classes. `net_server_packet_factory_ctor` registers their constructors by command code. `net_deserialize_server_packet` builds the class and asks it to read the body.

Some packets skip this class factory. `SVersionCheck`, `SNewUserCheck`, `SLoginCheck`, and `SMetaData` remain decoded byte buffers and are handled by panes or managers. A missing factory class therefore does not mean a command is unused.

Client packets are different. Only the client packet base class appears in RTTI. Most outgoing messages are built inline, so their names come from behavior and project-owner protocol knowledge rather than recovered concrete class names.

## Useful boundaries

- `net_submit_client_packet` sees outgoing plaintext bodies.
- `net_send_client_packet` chooses the outgoing transform.
- `net_post_decoded_server_packet_event` sees incoming decoded bodies.
- `net_deserialize_server_packet` is the typed server packet boundary.
- Winsock sees only framed wire bytes.

These boundaries are useful for tracing and for the [event proxy design](../systems/event-proxy.md). Addresses are in the [function reference](../appendix/functions.md).
