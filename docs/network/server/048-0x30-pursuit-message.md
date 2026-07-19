# Pursuit Message (`SPursuitMessage`)

`SPursuitMessage` drives multi-step NPC conversations. It can show a plain page, offer choices, collect text, expose Previous and Next navigation, open a protected ID/password form, or close the conversation.

| Item | Value |
| --- | --- |
| Direction | Server to client |
| Command | `0x30` (48) |
| Transform | `derived` |
| Name provenance | Microsoft C++ RTTI in the target |
| Main owner | `NPCSession` |

## Body

```text
packet SPursuitMessage {
    u8 opcode                         // 0x30
    u8 dialog_type

    if dialog_type != 10 {
        u8      target_type
        u32     target_id
        u8      ignored_unknown
        u16     speaker_sprite
        u8      speaker_color
        bytes   ignored_secondary_group[4]
        u16     pursuit_id
        u16     step_id
        u8      has_previous
        u8      has_next
        u8      show_graphic
        string8 speaker_name

        if dialog_type == 0 or dialog_type == 2 or
           dialog_type == 4 or dialog_type == 6 or
           dialog_type == 9 {
            string16 content
        }

        if dialog_type == 2 or dialog_type == 3 or
           dialog_type == 6 {
            u8 choice_count
            repeat choice_count {
                string8 choice_text
            }
        }

        if dialog_type == 4 or dialog_type == 5 or
           dialog_type == 9 {
            string8 input_prolog
            u8      maximum_input_bytes
            string8 input_epilog
        }
    }
}
```

All multibyte values are big-endian. Type 10 returns from the deserializer immediately after `dialog_type`, so its complete body is only two bytes.

The client skips the same one-byte and four-byte common-header groups as `SScreenMenu`. It does not interpret external names proposed for those bytes.

## Dialog types

| Type | Exact or reconstructed client class | Content | Tail and behavior |
| ---: | --- | --- | --- |
| `0` | `NPC_Pursuit_MessageDialog` | Yes | Plain popup |
| `1` | Base message dialog | No | Simple popup |
| `2` | `NPC_Pursuit_MenuQuestionMessage` | Yes | Choice list |
| `3` | `NPC_Pursuit_SimpleMenuQuestionMessage` | No | Choice list and a local `CSay` echo |
| `4` | `NPC_Pursuit_TextMessage` | Yes | Prolog, input, epilog |
| `5` | `NPC_Pursuit_SimpleTextMessage` | No | Input tail and a local `CSay` echo |
| `6` | `NPC_Pursuit_QuestionMessageFace` | Yes | Choice list; skips the normal speaker-art refresh |
| `9` | `NPC_Pursuit_NexonclubIdTextMessage` | Yes | Protected ID/password form |
| `10` | Close command | No | Closes the active NPC dialog |

Types 1 and 3 are real client branches. Type 5 behaves as a simple text-input message. Values 7 and 8 do not construct a known subtype in this path.

## Navigation and input

`has_previous` and `has_next` independently enable the corresponding buttons. Their response step rules are:

| Action | `CPursuit.step_id` | Arguments |
| --- | ---: | --- |
| Previous | `step_id - 1` | None |
| Next | `step_id + 1` | None |
| Close button | Current `step_id` | None, then close locally |
| Menu choice | `step_id + 1` | Type 1, one-based choice number |
| Text submit | `step_id + 1` | Type 2, `string8` text |

The booleans control availability only. The client performs the arithmetic itself and does not take destination step numbers from the server.

After queuing any navigation, answer, or close response, the client closes the current dialog path. A continuing pursuit must send another `SPursuitMessage` for the requested step.

Choice indexes are sent one-based even though the dialog collection is indexed from zero. `maximum_input_bytes` is applied to the edit control. Type 9 builds a separate ID and masked-password dialog from `lnpcnid.txt`; its regional account manager must accept the form before the client emits an ordinary type-2 text response. The response contains a nonempty string produced in the protected pane's manager-result buffer. It does not serialize the ID and password controls directly.

Simple menu type 3 first sends [`CSay`](../client/014-0x0e-say.md) containing the selected choice text. Simple text type 5 first sends `CSay` containing `input_prolog`, a space, the entered text, another space, and `input_epilog`. It then sends the normal `CPursuit` response.

## UI flow

`net_deserialize_pursuit_message_server_packet` builds the packet object. `ui_npc_session_open_pursuit_message` closes immediately for type 10; otherwise it updates `NPCSession` and creates `NPC_Pursuit_MessageDialog`. `ui_npc_pursuit_build_subtype` adds the question or input model.

The outer pane uses `lnpcd.txt`. Choice dialogs use `lnpcd2.txt`, ordinary input uses `lnpcd4.txt`, and protected input uses `lnpcnid.txt`. The outer `DialogPane` attachment order makes actions 4, 5, and 6 Previous, Next, and Close. Actions 0 through 3 belong to the base name, content, and scrolling controls.

See [NPC dialogs](../../systems/npc-dialogs.md) for the complete pane and response model and [NPC dialog illustrations](../../systems/npc-dialog-illustrations.md) for the optional speaker art.

## Paired packet

Every navigation or answer uses [`CPursuit`](../client/058-0x3a-pursuit.md). `0x3A` is one of only two client opcodes with the dialog-response inner wrapper described in [Packet transforms](../packet-transforms.md#dialog-response-inner-wrapper).

## Known limits

The target-type values are echoed back but not decoded into a complete local enum in this path.
