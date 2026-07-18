# Game settings

The Game Settings dialog combines two kinds of preference in one list. Seven rows are controlled by the server. Six rows are real client preferences that remain in memory and are saved to `Darkages.cfg`.

This split matters because the same click can either send a packet or change local behavior immediately.

## Dialog flow

`GameSettingDialog` loads `_nsett.txt` and attaches 13 setting controls. Opening it sends [`CUserSetting`](../network/client/027-0x1b-user-setting.md) with setting ID `0`.

The server returns [`SMessage`](../network/server/010-0x0a-message.md) type `0x07`. The client uses the first message byte to distinguish a full tab-separated list from a single-row update.

```text
open dialog
  -> CUserSetting 0
  <- SMessage 0x07 full list

choose server row
  -> CUserSetting row_id
  <- SMessage 0x07 replacement text

choose client row
  -> update AppConfig and redraw the row
```

The dialog keeps one temporary ready byte for each row. Server rows start unavailable and become ready when their full-list token arrives. Client rows start ready because their text and values come from `AppConfig`. This 13-byte array belongs to the dialog and is discarded when the dialog closes.

## Ownership

| Setting IDs | Owner | State source | Persistence |
| --- | --- | --- | --- |
| `1` through `6`, `8` | Server | Returned row text | Not saved by this client |
| `7`, `9` through `13` | Client | `AppConfig` fields | `Darkages.cfg` |

The server returns formatted strings such as `Listen to whisper:ON `. The client replaces the row text but does not parse the suffix into a boolean. A supplied group-toggle trace confirms that setting 2 is the invitation row, formatted as `Join a group     :OFF` or `Join a group     :ON `.

For these seven rows, no longer-lived client setting field or later client-side enforcement was found. The server therefore owns their effective state. The client alone does not prove whether that state is stored per character or per account. The separate bottom-button icon reads `SSelfLook.is_group_open`, not the formatted setting text.

## Hard-coded ownership switch

The server and client split is compiled into a 13-entry table. It is not negotiated when the dialog opens.

```c
static const u8 server_owned[13] = {
    1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0
};

void activate_setting(u8 setting_id) {
    if (server_owned[setting_id - 1]) {
        if (row_ready[setting_id - 1])
            send_CUserSetting(setting_id);
    } else {
        update_local_AppConfig(setting_id);
        redraw_setting_row(setting_id);
    }
}
```

The full-list response parser consults the same table. It consumes every tab-separated token to preserve the row numbering, but replaces text only for server-owned rows. Client-owned rows keep the text produced from local configuration.

## Client memory

The six local values occupy this compact region of the global `AppConfig` object:

```c
struct AppConfigGameSettings {
    // offsets are relative to the complete AppConfig object
    u8  skill_spell_select_by_toggle; // +0x547, setting 10
    u8  group_answer;                 // +0x548, setting 7
    s32 scroll_level;                 // +0x54C, setting 9
    s32 user_click_mode;              // +0x550, setting 11
    s32 monster_say_record_mode;      // +0x554, setting 12
    s32 group_object_option;          // +0x558, setting 13
};
```

`app_config_ctor` supplies defaults of zero for the first five fields and one for `group_object_option`. The configuration loader replaces those defaults when matching file keys are present.

## Saving

`ui_game_setting_apply_local` changes the selected field in memory and formats the new localized row text. Closing the dialog normally calls `app_save_config`, which rewrites `Darkages.cfg` and includes these keys:

| Setting | File key | Introduced by config version |
| ---: | --- | ---: |
| `10` | `SkillSpellSelectByToggle` | `0x2000` |
| `7` | `GroupAnswer` | `0x2100` |
| `9` | `ScrollLevel` | `0x2300` |
| `11` | `UserClickMode` | `0x2400` |
| `12` | `MonsterSayRecordMode` | `0x2500` |
| `13` | `GroupObjectOption` | `0x2600` |

These choices belong to the client installation, not a character record. Another client installation will use its own configuration file.

## What the client settings do

| ID | File key | Default | Confirmed effect |
| ---: | --- | ---: | --- |
| `7` | `GroupAnswer` | `0` | A nonzero value accepts an incoming [`SGroup`](../network/server/099-0x63-group.md) request immediately with [`CGroup`](../network/client/046-0x2e-group.md) action `3`, instead of constructing the normal prompt dialog. The prompt's manual accept action calls the same builder. |
| `9` | `ScrollLevel` | `0` | Selects four-step or eight-step interpolation for the local player's walk animation. It does not change the `CMove` body or server movement rules. |
| `10` | `SkillSpellSelectByToggle` | `0` | Changes repeated skill and spell selection commands from fixed pane choices to toggling between the paired choices. It does not alter casting delay or animation timing. |
| `11` | `UserClickMode` | `0` | A nonzero value suppresses the normal [`CRequestObjectInfo`](../network/client/067-0x43-request-object-info.md) subtype `1` request when the clicked world object is another user. Monster and item click paths are unchanged. |
| `12` | `MonsterSayRecordMode` | `0` | A nonzero value bypasses the normal sender filter before monster speech is added to the local message-recording path. It does not change the speech balloon lifetime. |
| `13` | `GroupObjectOption` | `1` | Allows the optional group-advertisement object created from [`SDrawHumanObjects`](../network/server/051-0x33-draw-human-objects.md). Disabling it removes or omits that local overlay. |

These are local behavior switches. None changes a server-owned setting, and only the group-answer option sends a packet as a consequence of later gameplay traffic.

## Scroll level and movement timing

`map_try_move_local_player` starts the local walk sequence and then sends [`CMove`](../network/client/006-0x06-move.md). `ScrollLevel` is reduced to a boolean and passed only into the local human image session.

This is the setting that reaches movement code. The `Fast Move` text found in the server's skipped row 7 token does not.

| `ScrollLevel` | Interpolation ticks | Delay per tick | Walk frames | Total duration |
| ---: | ---: | ---: | --- | ---: |
| `0` | 4 | 114 ms | `1, 2, 3, 4` | 456 ms |
| Above `0` | 8 | 57 ms | `1, 1, 2, 2, 3, 3, 4, 4` | 456 ms |

Ordinary remote `WorldObject_Human` instances use a separate four-tick sequence at 100 ms per tick, totaling 400 ms. They never consult the local `ScrollLevel` value.

Both sequences cover the same projected tile distance. The four-step horizontal increments are `6, 8, 6, 8` pixels and the vertical increments are `3, 4, 3, 4`, totaling 28 by 14 pixels. The eight-step sequence divides those increments into `2, 4, 4, 4, 2, 4, 4, 4` horizontally and `1, 2, 2, 2, 1, 2, 2, 2` vertically. Direction changes only the signs and axes used for those increments.

The enabled setting therefore produces smaller, more frequent visual steps. It does not make a tile crossing complete sooner. It also does not change the `CMove` step counter, the time at which the accepted request is sent, the server acknowledgement path, or the attack and spell timing systems.

## Version mismatch in the full list

The supplied server list contains eight tokens. Token 7 is `Fast Move`, but this client marks row 7 as local and builds it from `AppConfig +0x548`, whose saved key is `GroupAnswer`. The parser still consumes token 7 so that token 8, `Clan whisper`, remains aligned, but it does not use the server's `Fast Move` text or status.

This could be protocol drift or a stale configuration-key name. It does not establish that `Fast Move` and `GroupAnswer` mean the same thing.
