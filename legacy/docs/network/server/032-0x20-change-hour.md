# 032 / 0x20: Change Hour (`SChangeHour`)

## Identification

| Property | Value |
|---|---|
| Direction | Server to client |
| Opcode | `0x20` |
| RTTI class | `SChangeHour` |
| Factory | `0x598050` |
| Constructor | `0x5980D0` |
| Vtable | `0x687D88` |
| Deserializer | `0x598100` |

## Preliminary payload model

```text
u8 hour
```

## Raw reader-call trace

`u8`

The raw trace lists static reader call sites. Conditional variants and counted records are represented more accurately in the preliminary model above and must not be interpreted as one unconditional flat structure.

## Verification status

- Opcode registration: confirmed from the client registry.
- Packet class name: confirmed from Visual C++ RTTI.
- Primitive widths and byte order: confirmed from reader implementations.
- Semantic field name and lighting effect: confirmed from the local handler and `Light` metadata lookup.

## Client handling

`net_handle_s_change_hour` at `0x5F2160` stores the byte at world offset `+0x25C` and calls `lighting_update_for_server_hour` at `0x5EF360`.

The client converts the byte to a metadata time slot:

```c
slot = hour * 2;
if (slot > 24)
    slot = 24;
```

It then looks up the current map in the metadata section named `Light`. The selected record supplies a `0..32` light value, an RGB tint, and whether `%06d.hea` should be loaded. See [Map lighting and masks](../../map/lighting.md).
