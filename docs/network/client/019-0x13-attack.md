# 019 / 0x13: Attack (`CAttack`)

- Direction: client to server
- Internal name: `CAttack`
- Local behavioral alias: `Assail`
- Related-game enum name: `Attack`
- Name provenance: Leaked company/engine class name corroborated by this client's opcode and local behavior.
- Evidence: 1 concrete builder/sender call site
- Send handling: default common transform mode 1
- Wire frame after transformation: `0xAA, u16be body_size, body`

## Builder call sites

- `net_send_c_attack` at `0x5F44B0`

## Plaintext body

```text
13
```

The local Space-key path reaches this payload-free sender through `input_handle_world_key_event` at `0x5F0D20`.
