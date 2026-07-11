# 056 / 0x38: Refresh (`CRefresh`)

- Direction: client to server
- Internal name: `CRefresh`
- Local behavioral alias: `Refresh`
- Related-game enum name: `RefreshUser`
- Name provenance: Leaked company/engine class name corroborated by this client's opcode and local behavior.
- Evidence: 1 concrete builder/sender call site
- Send handling: default common transform mode 1
- Wire frame after transformation: `0xAA, u16be body_size, body`

## Builder call sites

- `0x5f4640`

## Payload

```text
u8 opcode = 0x38
no payload
```

`net_send_c_refresh` at `0x5F4640` constructs exactly this one-byte plaintext body.

## Callers and behavior

`object_handle_world_input_event` at `0x5F1480` sends this packet for the internal F5 key event code `0x89`. Ctrl+R with modifier value `2` is an alternate shortcut. Before sending, both paths call `object_reset_movement_sync_state` at `0x5F4900` to clear pending movement synchronization records.

`net_handle_s_move` at `0x5F2FC0` also sends `CRefresh` when an authoritative position result disagrees with the local `WorldObject_User` coordinates.

Sending this packet does not locally clear the object list. See [View range and refresh](../../objects/view-range-and-refresh.md) for the client-side resynchronization path and current limits of the evidence.
