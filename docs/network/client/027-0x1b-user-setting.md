# User Setting (`CUserSetting`)

| Item | Value |
| --- | --- |
| Direction | Client to server |
| Command | `0x1B` (27) |
| Encoding | `derived` |
| Name provenance | Project-owner protocol name, confirmed by the `GameSettingDialog` call sites |

## Purpose

The Game Settings dialog uses this packet to request the server's settings list and toggle a server-managed setting. The body always has the same two-byte format. Only the meaning of `setting_id` changes.

The dialog also contains six client-managed settings. Those choices update `AppConfig` and do not send this packet.

## Body

```text
packet CUserSetting {
    u8      opcode                    // 0x1B
    u8      setting_id
}
```

All multibyte packet fields use the book's common big-endian rule. This body has no multibyte fields.

## Setting identifiers

| ID | Owner | Observed label or local key | Request behavior |
| ---: | --- | --- | --- |
| `0` | Server | Full list | Request the current server-managed rows |
| `1` | Server | `Listen to whisper` | Toggle after the row has been initialized |
| `2` | Server | `Join a group` | Toggle after the row has been initialized |
| `3` | Server | `Listen to shout` | Toggle after the row has been initialized |
| `4` | Server | `Believe in wisdom` | Toggle after the row has been initialized |
| `5` | Server | `Believe in magic` | Toggle after the row has been initialized |
| `6` | Server | `Exchange` | Toggle after the row has been initialized |
| `7` | Client | `GroupAnswer` | No packet |
| `8` | Server | `Clan whisper` | Toggle after the row has been initialized |
| `9` | Client | `ScrollLevel` | No packet |
| `10` | Client | `SkillSpellSelectByToggle` | No packet |
| `11` | Client | `UserClickMode` | No packet |
| `12` | Client | `MonsterSayRecordMode` | No packet |
| `13` | Client | `GroupObjectOption` | No packet |

The labels in the supplied capture are server text. The client-side names are configuration keys recovered from the executable, not necessarily the text shown by every localization.

## Request and response flow

Opening `GameSettingDialog` sends ID `0`. The server answers with [`SMessage`](../server/010-0x0a-message.md) type `0x07`, using a tab-separated list inside the message text.

Selecting a ready server row sends its ID. The server answers with another type `0x07` message containing one replacement row. The client displays the returned `ON` or `OFF` text verbatim. It does not parse or retain a server-setting boolean.

Number keys `1` through `9` select those IDs, and `0` selects ID `10`. The remaining rows are available through their dialog controls.

The complete ownership, memory, and persistence behavior is described in [Game settings](../../systems/game-settings.md).

## Known limits

The supplied full response contains a seventh token labeled `Fast Move`. This version consumes that token to keep the list aligned but does not use its text or status because row 7 is client-managed. The local field is saved under the historical key `GroupAnswer`. This could be protocol drift or a stale configuration-key name, so the two names should not be treated as confirmed aliases. The separate local ID 9 `ScrollLevel` field is the option that actually reaches movement interpolation code.

The client has no derived packet RTTI for `CUserSetting`. Its name comes from project vocabulary and its behavior is confirmed by the local builder and dialog flow.
