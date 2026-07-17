# Attack (`CAttack`)

| Item | Value |
| --- | --- |
| Direction | Client to server |
| Command | `0x13` (19) |
| Encoding | session key |
| Name provenance | Project protocol vocabulary, confirmed against the local builder and its attack input paths. |

## Purpose

The client sends `CAttack` when the player attacks. The packet is only the opcode and carries no target, direction, or timing value.

## Body

```text
packet CAttack {
    u8 opcode                    // 0x13
}
```

`net_send_attack` submits exactly this one-byte plaintext body.

## Space-key timing

Pressing or holding Space reaches `ui_world_pane_attack_from_keyboard`. The first attack is immediate. Later Space-key attack events are accepted only when more than 100 ms has elapsed since the previous accepted event:

```text
if last_attack_time == 0 || now - last_attack_time > 100 {
    send CAttack
    last_attack_time = now
}
```

The comparison is strictly greater than 100 ms. There is no 1,000 ms attack throttle in this path. Holding Space depends on repeated keyboard events reaching the pane; this function does not create a separate repeating attack timer.

## Other attack path

`ui_world_pane_attack_target` can face and attack an adjacent selected target. It calls the same opcode-only builder without the Space-key throttle.

These are client-side submission rules. They do not establish the server's combat cooldown or prove that every submitted attack succeeds.
