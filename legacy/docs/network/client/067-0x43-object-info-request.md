# 067 / 0x43: Object Info Request (`CObjectInfoRequest`)

- Direction: client to server
- Internal name: `CObjectInfoRequest`
- Local behavioral alias: `Interact`
- Related-game enum name: `RequestBubbleInfo`
- Name provenance: Leaked company/engine class name corroborated by this client's opcode and local behavior.
- Evidence: 5 concrete builder/sender call sites
- Send handling: common transform mode 0
- Wire frame after transformation: `0xAA, u16be body_size, body`

## Builder call sites

- `0x4cd350`
- `0x534a90`
- `0x5aa0e0`
- `net_send_c_object_info_request` at `0x5F4730`
- `0x5f47f0`

## Current structural notes

- Byte 0 of the untransformed body is opcode `0x43`.
- The world-click builder at `0x5F4730` emits subtype `1` followed by `object_id:u32be`.

```text
43 01 object_id:u32be
```

An ordinary left-click on another world object reaches this builder. Ctrl+left-click on another user opens a local `PopupMenuPane` instead and sends no immediate packet.
