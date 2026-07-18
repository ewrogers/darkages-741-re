# Spelled (`SSpelled`)

| Item | Value |
| --- | --- |
| Direction | Server to client |
| Command | `0x3A` (58) |
| Encoding | derived |
| Name provenance | Microsoft C++ RTTI in the target |

## Purpose

The server uses this packet to maintain the small spell indicators shown beside the game view. These icons can represent buffs, debuffs, bonuses, and other timed spell effects.

The packet does not contain an exact duration or a slot number. It identifies an icon and supplies one discrete duration stage. The client chooses a local display slot and redraws the indicator at that stage.

## Body

```text
packet SSpelled {
    u8      opcode                    // 0x3A
    u16     icon
    u8      duration_stage
}
```

`net_deserialize_spelled_server_packet` reads `icon` as a big-endian value, followed by the one-byte stage.

## Duration stages

The stage names are project-owner protocol vocabulary. The client independently confirms the six palette indexes and the special removal behavior of zero.

| Value | Name | Palette index | Client behavior |
| ---: | --- | ---: | --- |
| `0` | `None` | none | Removes the matching icon, or does nothing if it is absent. |
| `1` | `Blue` | `0x58` | Draws the smallest remaining-duration bar. |
| `2` | `Green` | `0x89` | Draws the next bar step. |
| `3` | `Yellow` | `0x45` | Draws the next bar step. |
| `4` | `Orange` | `0x97` | Draws the next bar step. |
| `5` | `Red` | `0x28` | Draws the next bar step. |
| `6` | `White` | `0xFF` | Draws the largest remaining-duration bar. |

The stage changes both the narrow bar's palette color and its height. A normal countdown therefore moves from White toward Blue before the server removes the effect with stage `0`. The client does not range-check this byte, so values outside `0` through `6` have no defined protocol meaning.

## Local slots

RTTI class `GUIBackPane::_SpelledViewPane` inherits the indicator behavior from `SpelledViewPane_A`. The pane owns ten slots. Each slot stores one icon and one stage.

`ui_spelled_view_pane_apply_packet` handles an update as follows:

1. Search the ten slots for the same icon.
2. If found, replace its stage, or clear the slot when the new stage is `0`.
3. If absent and the stage is nonzero, use the first empty slot.
4. If all ten slots are occupied, ignore the new icon.

Removal does not compact later icons. A future new effect fills the first available gap. The icon is drawn from icon-library group `2`; the pane uses frame `0` of `spelled.epf` as its background.

## Duration ownership

The client stores no seconds, expiration time, or last-update timestamp for these effects. It also never decrements `duration_stage`. Its timer callback only updates pane visibility.

The project owner reports that the server retains the exact duration and sends `SSpelled` when an effect is added, crosses a display threshold, or expires. The client behavior supports that model: every visible stage transition must arrive in another packet.

The exact server-side threshold times are not present in this packet and cannot be recovered from the client display code alone. No paired client request was found; this is a server-pushed state update.
