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

## Self-look and sound packet objects

`SSelfLook` reserves all 255 possible legend records inside the packet object. This accounts for most of its `0x9C64`-byte allocation. The wire response only carries the records selected by `legend_count`.

```c
struct SelfLookLegendMark {
    u32 icon;                    // +0x00, decoded from u8
    u32 palette_index;           // +0x04, decoded from u8
    char key[0x46];              // +0x08
    char text[0x46];             // +0x4E, parser adds CR + NUL
};                               // size 0x94

struct SSelfLookFields {
    u8 base[0x10];
    u8 internal_zeroes[3];       // +0x10
    u8 nation;                   // +0x13

    u32 guild_rank_length;       // +0x14
    char guild_rank[0x104];      // +0x18
    u32 title_length;            // +0x11C
    char title[0x104];           // +0x120
    u32 group_members_length;    // +0x224
    char group_members[0x104];   // +0x228
    u8 is_group_open;            // +0x32C
    u8 padding_32d[3];
    u32 internal_zero_330;

    u32 display_class_length;    // +0x334
    char display_class[0x104];   // +0x338
    u32 guild_length;            // +0x43C
    char guild[0x104];           // +0x440

    u8 legend_count;             // +0x544
    u8 padding_545[3];
    u32 show_ability_metadata;   // +0x548, decoded from u8
    u32 show_master_metadata;    // +0x54C, decoded from u8
    u32 character_class;         // +0x550, decoded from u8
    SelfLookLegendMark marks[255]; // +0x554

    u8 reserved_98c0[0x94];
    u8 is_recruiting;            // +0x9954
    char recruiting_leader[0x100]; // +0x9955
    char recruiting_name[0x100];   // +0x9A55
    char recruiting_note[0x100];   // +0x9B55
    u8 minimum_level;            // +0x9C55
    u8 maximum_level;            // +0x9C56
    u8 class_counts[5][2];       // +0x9C57: wanted, current
    u8 tail_padding[3];
};                               // allocated size 0x9C64

struct SSoundEffectFields {
    u8 base[0x10];
    u16 sound;                   // +0x10, decoded from u8
    u16 track;                   // +0x12, decoded from u8 for sound 0xFF
};                               // allocated size 0x14
```

The leader bytes are present in `SSelfLookFields`, but the group-ad UI updater omits them when it builds its temporary display model. See [Self Look](../../network/server/057-0x39-self-look.md) for the wire order and the UI effects.

## World-state packet objects

`SChangeHour` retains only the one byte read by its parser. Extra decoded body bytes are not copied into the object.

```c
struct SChangeHourFields {
    u8 base[0x10];
    u8 time_step;               // +0x10
    u8 padding_11[3];
};                              // allocated size 0x14
```
