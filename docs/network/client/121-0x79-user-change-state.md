# 121 / 0x79: CUserChangeStatePacket?

- Direction: client to server
- Internal packet name: `CUserChangeStatePacket?`
- Local behavioral alias: `UserChangeState / SetStatus`
- Related-game enum name: `UserChangeState`
- Name provenance: Related-game internal enum name `UserChangeState` at the same opcode is corroborated by this client's bounded state selector; the C++ class spelling remains reconstructed.
- Evidence: 1 concrete builder/sender call site
- Send handling: default common transform mode 1
- Wire frame after transformation: `0xAA, u16be body_size, body`

## Builder call sites

- `0x5fc790` : `net_send_c_user_change_state`

## Current structural notes

The recovered body is `[u8 opcode=0x79, u8 state]`.

- The client constrains the state to 0 through 7; out-of-range values are replaced with zero.
- After sending, it stores the selected state in the local client object at offset `+0x1048`.
- This supports the related-game enum name `UserChangeState` over the broader behavioral label `SetStatus`.
