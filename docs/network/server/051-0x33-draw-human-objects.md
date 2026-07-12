# 051 / 0x33: Draw Human Objects (`SDrawHumanObjects`)

## Identification

| Property | Value |
|---|---|
| Direction | Server to client |
| Opcode | `0x33` |
| RTTI class | `SDrawHumanObjects` |
| Factory | `0x5984C0` |
| Constructor | `0x598540` |
| Vtable | `0x687DD8` |
| Deserializer | `0x598570` |

## Payload model

```text
u16be x
u16be y
u8 unknown_04
u32be object_id
u16be appearance_id
if appearance_id != special_appearance_constant:
  packed/variant fields: u8, u16be, u8, u16be, u8, u16be, u8, u8, u8, u16be, u8, u16be, u8, u16be, u8, u8, u8, u16be, u8, u8, u8, u8, u8
else:
  u16be, u8, u8, u8, skip/view 5 bytes, u8
string[u8 length]
string[u8 length]
Several packed appearance bits are normalized after reading.
```

## Raw reader-call trace

`u16be -> u16be -> u8 -> u32be -> u16be -> u8 -> u16be -> u8 -> u16be -> u8 -> u16be -> u8 -> u8 -> u8 -> u16be -> u8 -> u16be -> u8 -> u16be -> u8 -> u8 -> u16be -> u8 -> u8 -> u8 -> u8 -> u8 -> u16be -> u8 -> u8 -> u8 -> view(n) -> u8 -> string[u8 length] -> string[u8 length]`

The raw trace lists static reader call sites. Conditional variants and counted records are represented more accurately in the payload model above and must not be interpreted as one unconditional flat structure.

## Client handling

`net_handle_s_draw_human_objects` at `0x5F3340` compares `object_id` with the self object ID stored at controller offset `+0x214`.

- A different ID creates or replaces `WorldObject_Human` through `object_create_human` at `0x5CA140`.
- A matching ID reuses the existing `WorldObject_User` or creates it through `object_create_self_user` at `0x5CA830`.
- Normal appearance records call `object_human_apply_appearance` at `0x5E0070`.
- An `appearance_id` of `0xFFFF` uses `object_living_apply_monster_appearance` at `0x5E0370`, which supports disguised or monster-form humans.

The handler also applies the visible name and related name/group overlays, then finalizes the actor's displayed state.

One `u8` in the normal appearance variant is stored at packet-object offset `+0x260` and used as the actor light-mask number. It defaults to `1`. When the current map mode is `3`, values greater than zero load `mask1%02d.epf` and attach the resulting light mask to the human object. See [Map lighting and masks](../../map/lighting.md).

## Verification status

- Opcode registration: confirmed from the client registry.
- Packet class name: confirmed from Visual C++ RTTI.
- Primitive widths and byte order: confirmed from reader implementations.
- Object identity, coordinates, self split, and appearance variant: confirmed from the handler.
- The object light-mask number is confirmed from its renderer use. Several other packed appearance fields and both strings are not fully named.
