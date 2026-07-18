# Group (`CGroup`)

| Item | Value |
| --- | --- |
| Direction | Client to server |
| Command | `0x2E` (46) |
| Encoding | derived |
| Name provenance | Project-owner protocol name, checked against the matching client builders |

## Purpose

The client uses this packet for ordinary group requests and for the recruiting group box. The action chooses the operation. Every confirmed form carries a character name, and `RecruitStart` appends the settings entered in `GroupAdDialogPane`.

The client has no derived packet RTTI for this name.

## Actions

The action names are project-owner protocol vocabulary. The matching client confirms the behavior shown below.

| Value | Name | Client behavior |
| ---: | --- | --- |
| `1` | `Invite` | No action-1 builder was found in the matching client. |
| `2` | `Request` | Sends an ordinary group request for the named character. `UserLookPane` and several world UI paths use this form. |
| `3` | `Accept` | Sent by the normal group prompt's accept action. A nonzero `GroupAnswer` setting sends the same response automatically. |
| `4` | `RecruitStart` | Publishes the local character's recruiting group box. |
| `5` | `RecruitView` | Requests recruiting details for the selected name. The paired server response is `SGroup` action `4`. |
| `6` | `RecruitStop` | Stops the local character's recruiting listing. |
| `7` | `RecruitJoin` | Requests to join the leader shown in `GroupAdInfoDialogPane`. |

## Body

```text
packet CGroup {
    u8      opcode                    // 0x2E
    u8      action
    string8 target_name

    if action == 4 {
        string8 group_name
        string8 note
        u8      minimum_level
        u8      maximum_level
        u8      maximum_warriors
        u8      maximum_wizards
        u8      maximum_rogues
        u8      maximum_priests
        u8      maximum_monks
    }
}
```

For `RecruitStart`, `target_name` is the local character name. `RecruitStop` also sends the local name. The request, view, and join forms use the selected character or leader name.

`ui_group_ad_dialog_read_model` reads the form in the same class order used by the UI: Warrior, Wizard, Rogue, Priest, then Monk. `net_send_group_recruit_start` writes one maximum byte for each row. Current membership is not part of this client-to-server form.

## Paired server messages

[`SGroup`](../server/099-0x63-group.md) action `1` opens the request prompt that can produce action `3`. Its action `4` supplies the recruiting details requested by action `5`. Server action `5` converts a recruiting join into an ordinary client action `2` request for the supplied name.
