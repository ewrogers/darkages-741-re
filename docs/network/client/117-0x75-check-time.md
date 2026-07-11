# 117 / 0x75: CCheckTimePacket?

- Direction: client to server
- Internal packet name: `CCheckTimePacket?`
- Local behavioral alias: `CheckTime / SyncTicks`
- Related-game enum name: `CheckTime`
- Name provenance: Related-game internal enum name `CheckTime` at the same opcode is directly corroborated by this client's server-tick plus `timeGetTime()` reply; the C++ class spelling remains reconstructed.
- Evidence: 1 concrete builder/sender call site
- Send handling: default common transform mode 1
- Wire frame after transformation: `0xAA, u16be body_size, body`

## Builder call sites

- `0x5f7830` : `net_send_c_check_time`

## Current structural notes

The recovered body is nine bytes:

| Offset | Type | Meaning |
|---:|---|---|
| 0 | `u8` | opcode `0x75` |
| 1 | `u32be` | value supplied by the incoming server time-check object |
| 5 | `u32be` | local `timeGetTime()` value |

- This is a direct response to the local RTTI-backed `SCheckTime` packet, confirming the related-game enum name `CheckTime`.
