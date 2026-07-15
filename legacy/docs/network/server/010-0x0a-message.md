# 010 / 0x0A: Message (`SMessage`)

## Identification

| Property | Value |
|---|---|
| Direction | Server to client |
| Opcode | `0x0A` |
| RTTI class | `SMessage` |
| Factory | `0x59A050` |
| Constructor | `0x59A0D0` |
| Vtable | `0x687F70` |
| Deserializer | `0x59A100` |

## Payload model

```text
u8 message_type
if message_type == 0x11: u8, u8, string[u8 length]
u16be data_length
bytes[data_length]
```

## Raw reader-call trace

`u8 -> u8 -> u8 -> string[u8 length] -> u16be -> view(n)`

The raw trace lists static reader call sites. Conditional variants and counted records are represented more accurately in the payload model above and must not be interpreted as one unconditional flat structure.

## Handler and display variants

`net_handle_s_message` at `0x5F6D80` routes the packet by `message_type`:

| Type | Result |
|---:|---|
| `0x00` | Append to `GameMessagePane` with palette `0x58`, RGB `127,167,243` |
| `0x03` | Append white text to `GameMessagePane` |
| `0x08`, `0x09` | Open standard `WindowMessageDialogPane` |
| `0x0A` | Open alternate `WindowMessageDialogPane` |
| `0x0B` | Append to `GameMessagePane` with palette `0x77`, RGB `143,151,55` |
| `0x0C` | Append to `GameMessagePane` with palette `0x54`, RGB `115,183,175` |
| `0x12` | Append white text to `ScorePane` when length is at most `70` |

The popup variants replace tab bytes with carriage returns before creating the pane. Look results use this popup path. The exact private tell, guild, and world-message assignments among the colored text types still require a capture.

See [Speech balloons and message routing](../../chat/receive-and-display.md) for the complete UI flow and function addresses.

## Verification status

- Opcode registration: confirmed from the client registry.
- Packet class name: confirmed from Visual C++ RTTI.
- Primitive widths and byte order: confirmed from reader implementations.
- `message_type`, length, and data roles: confirmed by handler use.
- Channel names for the colored text subtypes: pending capture verification.
