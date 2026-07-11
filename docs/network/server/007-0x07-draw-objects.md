# 007 / 0x07: Draw Objects (`SDrawObjects`)

## Identification

| Property | Value |
|---|---|
| Direction | Server to client |
| Opcode | `0x07` |
| RTTI class | `SDrawObjects` |
| Factory | `0x5989C0` |
| Constructor | `0x598A40` |
| Vtable | `0x687E70` |
| Deserializer | `0x598AB0` |

## Payload model

```text
u16be record_count
repeat record_count times:
  u16be x
  u16be y
  u32be object_id
  u16be sprite_id

  if sprite_id >= 0x4000 and sprite_id <= 0x7fff:
    u8 monster_field_a
    u8 monster_field_b
    u8 monster_field_c
    u8 monster_field_d
  else:
    u8 item_field

  u8 common_field_a
  u8 common_field_b

  if sprite_id >= 0x4000 and sprite_id <= 0x7fff:
    u8 label_kind
    if label_kind == 2:
      string[u8 length] label
```

## Raw reader-call trace

`u16be -> subreader(remaining)`

The raw trace lists static reader call sites. Conditional variants and counted records are represented more accurately in the payload model above and must not be interpreted as one unconditional flat structure.

## Client handling

The deserializer at `0x598AB0` reads the count and exposes a subreader over the remaining bytes. `net_s_draw_objects_read_record` at `0x598B30` consumes one variable-length record. `net_handle_s_draw_objects` at `0x5F3150` loops exactly `record_count` times.

- `sprite_id` `0x4000..0x7FFF` creates `WorldObject_Monster`; the appearance index is `sprite_id - 0x4000`.
- `sprite_id` `0x8000..0xBFFF` creates `WorldObject_Item`; the item index is `sprite_id - 0x8000`.
- Other sprite-ID ranges are ignored by this handler.

The monster class is used for creatures and NPC-style actors. This client has no separate `WorldObject_NPC` RTTI class.

## Verification status

- Opcode registration: confirmed from the client registry.
- Packet class name: confirmed from Visual C++ RTTI.
- Primitive widths and byte order: confirmed from reader implementations.
- Record loop and class selection: confirmed from `0x598B30` and `0x5F3150`.
- Several per-record byte meanings: unknown.
