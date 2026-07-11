# 005 / 0x05: User Appearance (`SUserAppearance`)

## Identification

| Property | Value |
|---|---|
| Direction | Server to client |
| Opcode | `0x05` |
| RTTI class | `SUserAppearance` |
| Factory | `0x59CAC0` |
| Constructor | `0x59CB40` |
| Vtable | `0x6881A0` |
| Deserializer | `0x59CB70` |

## Payload model

```text
u32be object_id
u8 unknown_04
u8 unknown_05
u8 unknown_06
u8 flags_07
u8 unknown_08
```

## Raw reader-call trace

`u32be -> u8 -> u8 -> u8 -> u8 -> u8`

The raw trace lists static reader call sites. Conditional variants and counted records are represented more accurately in the payload model above and must not be interpreted as one unconditional flat structure.

## Client handling

`net_handle_s_user_appearance` at `0x5F2E90` checks bit `0x80` in the byte stored at packet-object offset `+0x17`. When clear, it writes `object_id` to controller offsets `+0x210` and `+0x214`. The packet establishes self identity but does not allocate `WorldObject_User`. Allocation occurs when a matching [`SDrawHumanObjects`](051-0x33-draw-human-objects.md) record arrives.

The handler also forwards the packet to the component at controller offset `+0x2CC`. The meanings of the other bytes remain open.

## Verification status

- Opcode registration: confirmed from the client registry.
- Packet class name: confirmed from Visual C++ RTTI.
- Primitive widths and byte order: confirmed from reader implementations.
- `object_id` and the `0x80` branch: confirmed from client state writes.
- Remaining byte meanings: unknown.
