# Network packet objects

Network events carry either decoded packet bodies or an early connection greeting. Once normal packet parsing begins, RTTI-backed server packet objects retain fields needed by their handlers. Packet wire layouts remain on the individual packet pages.

## Decoded server event

```text
struct ServerEventFields {
    bytes *body                 // Event +0x14, command byte first
    u32 body_length             // Event +0x18
    ServerPacket *parsed        // Event +0x1C, null when no class exists
}
```

During the first TCP receive, the same event family can carry an owned copy of the complete wire bytes instead of a decoded body. `TerminalPane2` handles that raw form before the packet factory is active.

## Connection handshake fields

These fields belong to the large socket object. Only the state needed to explain the welcome transition is shown.

```text
struct SocketHandshakeFields {
    u8 transport_selector       // +0x780D8, 1..4 are modem COM ports, 5 is TCP
    bool raw_stream_mode        // +0x780DC
    bool text_framing_enabled   // +0x780DD
}
```

The constructor sets both booleans. While `raw_stream_mode` is true, the selected receiver posts the available greeting bytes without packet parsing. The observed `ESC C` welcome clears both fields, enabling binary framing on TCP. `ESC S` clears raw-stream mode but leaves printable outbound framing enabled. The serial receiver also changes from greeting bytes to printable records when raw-stream mode is cleared.

The RTTI-backed `TerminalPane2` owns the control parser:

```text
struct TerminalPane2HandshakeFields {
    u32 control_state           // +0x190
    Pane *text_output           // +0x1A0, exact derived type unknown
}
```

Important control states include normal text, escape, Telnet IAC, Telnet option, and the final connected transition. Its network-event method occupies primary-vtable slot `+0x50`.

## Startup packet objects

These are partial layouts for the RTTI-backed server packet objects used during the observed bootstrap exchange. The common `ServerPacket` base occupies the first `0x10` bytes.

```c
struct STransferServerFields {
    u8 base[0x10];
    u32 ipv4_value;              // +0x10, decoded from u32be
    u16 port;                    // +0x14, decoded from u16be
    u32 token_length;            // +0x18
    u8 token[];                  // +0x1C, inline and locally NUL-terminated
};

struct SStipulationFields {
    u8 base[0x10];
    u8 mode;                     // +0x10
    u32 greeting_crc32;          // +0x14, mode 0
    u32 compressed_size;         // +0x18, mode 1
    u8 *compressed_data;         // +0x1C, mode 1
};

struct SBrowserFields {
    u8 base[0x10];
    u8 subtype;                  // +0x10
    u16 first_size;              // +0x12, subtypes 1 and 2
    u8 *first_data;              // +0x14
    u16 second_size;             // +0x18
    u8 *second_data;             // +0x1C
    char homepage_url[];         // +0x20, subtype 3 inline string
};
```

The apparent overlap is variant storage. A subtype or mode determines which fields are valid.

## Message packet objects

These packet objects keep short `string8` values inline, but `SMessage` retains its larger main body as a pointer into the decoded packet storage.

```c
struct SMessageFields {
    u8 base[0x10];
    u32 message_type;            // +0x10, decoded from u8
    u32 message_length;          // +0x14, decoded from u16be
    u8 *message;                 // +0x18
    u8 extra_0;                  // +0x1C, type 0x11 only
    u8 extra_1;                  // +0x1D, type 0x11 only
    u8 padding_1e[2];
    u32 extra_text_length;       // +0x20, type 0x11 string8
    char extra_text[256];        // +0x24, type 0x11
};                              // allocated size 0x124

struct SSayFields {
    u8 base[0x10];
    u32 speech_mode;             // +0x10, decoded from u8
    u32 object_id;               // +0x14, decoded from u32be
    char text[256];              // +0x18, decoded from string8
};                              // allocated size 0x118
```

The type-`0x11` `SMessage` prefix is parsed even though the recovered consumers do not display that type. `SSay` text is used directly by the world-balloon path.

## World-state packet objects

`SChangeHour` retains only the one byte read by its parser. Extra decoded body bytes are not copied into the object.

```c
struct SChangeHourFields {
    u8 base[0x10];
    u8 time_step;               // +0x10
    u8 padding_11[3];
};                              // allocated size 0x14
```
