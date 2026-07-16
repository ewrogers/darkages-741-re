# Network transport

The transport layer adds a small frame around every packet body. It also chooses the packet transform before sending and removes it after receiving.

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
TCP receive
  -> net_receive_frames
  -> optional packet transform
  -> net_post_decoded_server_packet_event
  -> event_dispatch
  -> packet class or direct handler
```

Socket data is buffered and consumed by `net_receive_frames`. A decoded opcode-first body becomes event type `0x13`, so the normal main-thread event system can deliver it to game code.

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
