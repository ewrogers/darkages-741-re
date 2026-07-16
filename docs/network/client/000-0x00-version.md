# Version (`CVersion`)

The client sends its numeric version immediately after the server welcome finishes the connection handshake. For this build, the complete plaintext body is `00 02 E5 4C 4B 00`.

| Item | Value |
| --- | --- |
| Direction | Client to server |
| Command | `0x00` (0) |
| Framing | Binary `0xAA` frame after the observed `ESC C` welcome |
| Transform | `raw` |
| Name provenance | Project protocol name confirmed against the local builder |

## What triggers it

The first TCP receive is delivered to `TerminalPane2` as unparsed wire bytes. Its network handler scans for a terminal-style connection command:

```text
server welcome
  -> ESC C selects binary framing
  -> next byte completes the connection transition
  -> queue CHello
  -> reset the client packet sequence
  -> queue CVersion
```

`ESC S` reaches the same transition but selects the alternate text framing mode. The full text `CONNECTED SERVER\n` is not required by the client. After `ESC C` or `ESC S`, any following byte is enough to continue.

Both outgoing bodies are queued for the communications worker. The sequence reset occurs immediately before `CVersion` is built. Because `CVersion` is raw, it contains no sequence byte and does not advance the encrypted-packet sequence.

## Body

```text
packet CVersion {
    u8 opcode                 // 0x00
    u16be version_code        // 741, encoded as 0x02E5
    u8 marker_l               // 0x4C, ASCII "L"
    u8 marker_k               // 0x4B, ASCII "K"
    u8 terminator             // 0x00, appended by net_submit_client_packet
}
```

The 7.41 builder supplies `00 02 E5 4C 4B`. `net_submit_client_packet` appends `00` and includes it in the queued length, so the supplied decoded capture shows the complete six-byte body.

With binary framing selected, the complete wire bytes are:

```text
AA 00 06 00 02 E5 4C 4B 00
```

The body size is six bytes. No transform trailer or encrypted sequence is added because opcode `0x00` is raw.

## Where 741 comes from

The executable stores the decorated text `7D4E--1K`. The connection handler copies only its decimal digits, producing `741`, then converts that text to an integer and stores it in `client_version_code`.

Other client code displays the same value as `Version 7.41` by dividing it into `7` and `41`. This confirms that the big-endian field is a decimal version code rather than three separate version bytes.

## Known limits

The meanings of the literal `L` and `K` bytes are not established. They are fixed in this client and are not derived from the welcome, configuration, or session state.

The paired response is [Version Check (`SVersionCheck`)](../server/000-0x00-version-check.md). The connection trigger is documented under [Hello (`SHello`)](../server/126-0x7e-hello.md).
