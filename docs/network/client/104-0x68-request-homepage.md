# 104 / 0x68: CRequestHomepagePacket?

- Direction: client to server
- Internal packet name: `CRequestHomepagePacket?`
- Local behavioral alias: `RequestHomepage`
- Related-game enum name: `SlotScroll`
- Name provenance: Internal-style local name inferred from this client's behavior; no exact leaked class match is known yet.
- Evidence: 1 concrete builder/sender call site
- Send handling: common transform mode 0
- Wire frame after transformation: `0xAA, u16be body_size, body`

## Builder call sites

- `0x4ba0c0` : `net_send_c_request_homepage`

## Current structural notes

- The recovered body is `[u8 opcode=0x68, u8 action=1]`.
- Both callers are in the local stipulation/login-notice receive path and issue this request before processing that content.
- The related game later reuses `0x68` as `SlotScroll`; the current caller context favors retaining `RequestHomepage` here.
