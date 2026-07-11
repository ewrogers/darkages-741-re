# 017 / 0x11: Change Dir (`CChangeDir`)

- Direction: client to server
- Internal name: `CChangeDir`
- Local behavioral alias: `Turn`
- Related-game enum name: `ChangeDirection`
- Name provenance: Leaked company/engine class name corroborated by this client's opcode and local behavior.
- Evidence: 1 concrete builder/sender call site
- Send handling: default common transform mode 1
- Wire frame after transformation: `0xAA, u16be body_size, body`

## Builder call sites

- `net_send_c_change_dir` at `0x5F4510`

## Plaintext body

```text
11 direction:u8
```

`input_turn_self` at `0x5F0900` updates the local self object before sending this packet.
