# 069 / 0x45: CReplyCRCPacket

- Direction: client to server
- Internal packet name: `CReplyCRCPacket`
- Local behavioral alias: `Heartbeat / CRC challenge reply`
- Related-game enum name: `ReplyCRC`
- Name provenance: Leaked company/engine class name corroborated by this client's opcode and local behavior.
- Evidence: 1 concrete builder/sender call site
- Send handling: default common transform mode 1
- Wire frame after transformation: `0xAA, u16be body_size, body`

## Builder call sites

- `0x5f2cf0` : `net_handle_s_request_crc`

## Current structural notes

The handler reads a `u16be` challenge from the incoming `SRequestCRCPacket`, then emits this 3-byte untransformed body:

| Offset | Type | Meaning |
|---:|---|---|
| 0 | `u8` | opcode `0x45` |
| 1 | `u16be` | CRC-16 reply |

- The reply starts with CRC state zero and applies `net_crc16_update` at `0x5B8F30` first to the challenge's low byte, then to its high byte.
- This local request/reply path confirms the leaked internal name `CReplyCRCPacket`; the earlier behavioral label `Heartbeat` described when it occurs, not what the packet class does.
