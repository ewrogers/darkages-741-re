# 000 / 0x00: Version Check (`SVersionCheck`, lobby)

## Identification

| Property | Value |
|---|---|
| Direction | Server to client |
| Opcode | `0x00` |
| Internal class vocabulary | `SVersionCheck` |
| Related-game enum | `VersionCheck` |
| Current receive crypto switch | explicitly recognized as raw |
| Current game-server RTTI registry | not registered |
| Local protocol status | known lobby/login-server packet |

## Payload model

This packet is consumed by `net_handle_s_version_check_raw` at `0x4B7F80`, outside the game-server RTTI packet registry. The second byte selects a subtype.

### Subtype `0x00`: encryption/session setup

```text
u8    opcode = 0x00
u8    subtype = 0x00
u32be unknown/check value
u8    salt_table_seed
u8    primary_key_length
u8    primary_key[primary_key_length]
```

- `salt_table_seed` selects one of ten packet mask-table formulas (`0..9`).
- The transmitted primary key replaces the default `"UrkcnItnI"`; captures are expected to show a nine-byte replacement, although the setter honors the transmitted length.
- Both changes are queued asynchronously to the communications worker.
- Subtypes `0x01` and `0x02` also have local branches, but their full semantics are not yet documented.

## Verification status

- Opcode and lobby use: supplied protocol knowledge.
- Internal class vocabulary: leaked related-engine packet template.
- Same-opcode related-game enum: confirmed by the supplied comparison list.
- Current-client framing support: confirmed; the local receive switch routes `0x00` as raw.
- Support through the currently recovered 61-entry game registry: disproven; there is no `0x00` factory entry.
- Current-client raw dispatch path and subtype-0 encryption fields: confirmed from local code.
- Meaning of subtype-0's `u32be` value and the remaining subtypes: pending.
