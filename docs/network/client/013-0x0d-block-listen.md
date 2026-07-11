# 013 / 0x0d: CBlockListenPacket?

- Direction: client to server
- Internal packet name: `CBlockListenPacket?`
- Local behavioral alias: `BlockListen / IgnoreUser`
- Related-game enum name: `BlockListen`
- Name provenance: Related-game internal enum name `BlockListen` at the same opcode, corroborated by this client's three local subcommand builders; the C++ class spelling remains reconstructed.
- Evidence: 3 concrete builder/sender call sites
- Send handling: default common transform mode 1
- Wire frame after transformation: `0xAA, u16be body_size, body`

## Builder call sites

- `0x550aa0` : `net_send_c_block_listen_action_1`
- `0x550c60` : `net_send_c_block_listen_action_2`
- `0x550ee0` : `net_send_c_block_listen_action_3`

## Current structural notes

- Subcommand 1 emits `[u8 opcode=0x0D, u8 action=1]`.
- Subcommands 2 and 3 emit `[u8 opcode=0x0D, u8 action, u8 name_length, bytes[name_length]]`.
- The three-action layout and related-game name `BlockListen` fit an ignore/block-list management packet substantially better than the former invented class name.
