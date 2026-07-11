# 122 / 0x7a: CRequestFamilyNamePacket?

- Direction: client to server
- Internal packet name: `CRequestFamilyNamePacket?`
- Local behavioral alias: `RequestFamilyName / RequestFamilyList`
- Related-game enum name: `RequestLoverName`
- Name provenance: The related-game enum calls this opcode `RequestLoverName`; this client instead constructs `FamilyList`, loads `lfamily.txt`, and receives `SFamilyName`, so the local `FamilyName` terminology is stronger. The C++ class spelling remains reconstructed.
- Evidence: 1 concrete builder/sender call site
- Send handling: default common transform mode 1
- Wire frame after transformation: `0xAA, u16be body_size, body`

## Builder call sites

- `0x4719b0` : `net_send_c_request_family_name`

## Current structural notes

- The recovered request body contains only opcode `0x7A`.
- Its only caller is the constructor for the local `FamilyList` UI, which also loads `lfamily.txt`.
- The paired local receive class is `SFamilyName` at opcode `0x6D`.
- The related game calls this feature `LoverName`, while the later leaked template list uses `FriendList`; the current binary's repeated `Family` terminology is the strongest evidence for this client.
