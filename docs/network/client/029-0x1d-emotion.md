# Emotion (`CEmotion`)

`CEmotion` asks the server to play one of the character's emotes. The body carries an emotion request code. It does not carry a duration, target, or sound.

| Item | Value |
| --- | --- |
| Direction | Client to server |
| Command | `0x1D` (29) |
| Transform | `derived` |
| UI owner | RTTI class `WorldPane` |
| Name provenance | Project-owner protocol vocabulary matched to the locally confirmed builder and keyboard path |

## Body

```text
packet CEmotion {
    u8      opcode                    // 0x1D
    u8      emotion                   // emotion request code
}
```

`net_send_emotion` submits exactly these two meaningful bytes. The common client-packet submission path keeps its usual local trailing zero outside the logical body.

The sender accepts any `u8`. It does not apply its own range check.

## Normal keyboard path

`ui_world_pane_handle_keyboard_event` maps modified number-row keys through a fixed 33-entry table. The covered keys are `1` through `0` and hyphen under three nonzero modifier states.

The normal table sends these emotion values:

```text
0 through 8, 12 through 35
```

Values `9`, `10`, and `11` are not produced by this keyboard table. This is a UI limit, not a packet-builder limit.

## Emotion codes are not motion IDs

The same client table keeps the outgoing emotion code and the expected local body-motion ID as separate fields. Its normal pairs reduce to:

| `CEmotion.emotion` | Local `SMotion.animation` |
| --- | --- |
| `0` through `8` | `9` through `17` |
| `12` through `13` | `18` through `19` |
| `14` through `35` | `23` through `44` |

This means the client does not model the server reply as a same-byte echo. The exact server-side lookup is outside this binary, but the client data clearly expects a translation from an emotion request to a body motion.

## Server validation behavior

Project-owner runtime testing shows that the matching server accepts forged emotion values outside the normal UI table. Those requests can make the server distribute body motions that the ordinary emote shortcuts cannot request.

The receiving client does not apply one global range check to [`SMotion`](../server/026-0x1a-motion.md). Its human and monster image sessions still reject motions for which they have no usable animation resource. The observed effect is therefore limited to a supported body animation and is visual only.

## Paired packet

On acceptance, the server distributes [`SMotion`](../server/026-0x1a-motion.md) with the affected object's ID, the selected body motion, and a timing value.
