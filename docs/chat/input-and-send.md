# Chat input and outgoing packets

## Keyboard entry points

The world key handler at `0x5A1540` recognizes these text-entry keys when no higher-priority pane consumes the event:

| Key | Action |
|---|---|
| Enter (`0x0D`) | Open `ChatInputPane` in public-say mode `0` |
| `!` (`0x21`) | Open `ChatInputPane` in shout mode `1` |
| `"` (`0x22`) | Open the tell or whisper input flow at `0x54F9D0` |

The broader keyboard and mouse dispatch order is documented separately as it is recovered. This page records only the confirmed chat-specific branches.

## Public say and shout

`chat_open_say_input` at `0x54F840` constructs `ChatInputPane` and includes the local character name in its visual prefix:

| Mode | Prefix | Palette | Sent `say_type` |
|---:|---|---:|---:|
| `0` | `<name>: ` | `0xFF` | `0` |
| `1` | `<name>! ` | `0x45` | `1` |

`chat_input_pane_ctor` at `0x54FCA0` stores the mode byte at `this + 0x19C`. `chat_input_send_say` at `0x54FD90` later builds:

```text
u8 opcode = 0x0E
u8 say_type
string[u8 length] text
```

The packet is submitted through `net_submit_client_packet` and uses the normal `CSay` transform policy.

## Tell or whisper

`chat_tell_input_send` at `0x550590` is a `TellInputPane` vtable method and builds `CTell`:

```text
u8 opcode = 0x19
string[u8 length] target_name
string[u8 length] message
```

The target is stored at `this + 0x19C`. The message is read from the input control into a 100-byte temporary buffer before submission.

The receive-side reply is displayed through the `SMessage` family, but the exact private-tell subtype has not yet been distinguished from guild and world-message subtypes in this binary.
