# Hello (`SHello`)

The server welcome is the bridge between the initial connection and normal packet processing. The observed message is a standard `0xAA` frame with opcode `0x7E`, but the client deliberately handles the first receive as unparsed wire bytes.

| Item | Value |
| --- | --- |
| Direction | Server to client |
| Command | `0x7E` (126) |
| Framing | Observed binary `0xAA` frame with a `u16be` body size |
| Transform | `raw` during the initial raw-stream receive mode |
| Name provenance | Behavioral alias; there is no `SHello` RTTI class or server packet factory entry |

## Observed form

```text
frame SHello {
    u8 marker                  // 0xAA
    u16be body_size
    u8 opcode                  // 0x7E
    u8 escape                  // 0x1B
    bytes greeting             // observed as "CONNECTED SERVER\n"
}
```

The `0x1B` immediately before the greeting text is an escape byte. It is part of the body and is separate from the frame size.

## How the client handles it

A new socket starts with raw-stream mode enabled. In that mode, `net_receive_frames` calls `recv` and passes the complete received bytes to `net_post_raw_server_bytes_event`. It does not yet validate the frame marker or size, select a packet transform, or construct a server packet object.

`TerminalPane2` receives the event through primary-vtable slot `+0x50`. `ui_terminal_pane_handle_server_data` scans every byte with this small control state machine:

```text
0x1B, 'C', next byte  -> select binary framing and connect
0x1B, 'S', next byte  -> select alternate text framing and connect
```

For the observed text, the `C` in `CONNECTED` doubles as the framing command and the first readable letter. The handler does not compare the remaining text. It also does not require opcode `0x7E`; that byte and the outer header are simply earlier bytes in the stream.

After the next byte completes the transition, the client clears raw-stream mode. Later receives use normal frame parsing, transforms, and packet dispatch. The same transition queues [Hello (`CHello`)](../client/098-0x62-hello.md), resets the outgoing encrypted-packet sequence, and queues [Version (`CVersion`)](../client/000-0x00-version.md).

## Terminal compatibility

This handler contains direct terminal-protocol behavior. It recognizes Telnet `IAC DO TERMINAL-TYPE` (`FF FD 18`) and answers with terminal type `dumb`. It also parses several ANSI-style escape forms.

This supports describing the welcome as a terminal-compatible connection handshake. The executable does not establish why that design was retained or whether readability in a live terminal was its original purpose.

## Known limits

The exact greeting text comes from observed server traffic. The client only proves the shorter escape-command behavior above. `SHello` is therefore a useful protocol name, not a compiler-recovered class name.
