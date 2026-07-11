# 001 / 0x01: New User Check (`SNewUserCheckPacket?`, lobby candidate)

## Identification

| Property | Value |
|---|---|
| Direction | Server to client |
| Opcode | `0x01` |
| Reconstructed class candidate | `SNewUserCheckPacket?` |
| Related-game enum | `NewUserCheck` |
| Current receive crypto switch | explicitly recognized as primary-key mode |
| Current game-server RTTI registry | not registered |
| Local protocol status | transport support confirmed; packet-object handler uncertain |

## Payload model

Unknown.

## Verification status

- Same-opcode name: present in the supplied related-game enum.
- Current-client framing/decrypt support: confirmed; the local receive switch routes `0x01` through primary-key decryption.
- The loaded game-server registry has no `0x01` entry.
- The exact `NewUserCheck` semantics and post-decrypt lobby handler still require a local capture or state-specific handler.
