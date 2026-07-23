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

## Example decoded bodies

These examples are complete decoded packet bodies. They do not include the frame header, sequence, trailer, or session-key transform. A server must apply the ordinary derived transform for opcode `0x30` before framing the packet.

Every non-close example uses target type `1`, target ID `0x12345678`, pursuit ID `0x0500`, current step 5, speaker sprite `0x401E`, and speaker name `Guide`. Previous and Next are enabled. `show_graphic` is zero so the examples do not depend on a matching local illustration. The skipped common-header bytes are also zero.

The response shown after each server body is the meaningful `CPursuit` body before the client applies the dialog-response inner wrapper, static transform, and frame. Types 0 and 1 demonstrate Next, question types select the first row, and text types submit `Bob`.

### Type 0: plain message

```text
30 00 01 12 34 56 78 00 40 1E 00 00 00 00 00 05
00 00 05 01 01 00 05 47 75 69 64 65 00 09 43 6F
6E 74 69 6E 75 65 3F
```

Decoded body length: 39 bytes. Pressing Next increments step 5 to 6:

```text
3A 01 12 34 56 78 05 00 00 06
```

### Type 1: simple popup

```text
30 01 01 12 34 56 78 00 40 1E 00 00 00 00 00 05
00 00 05 01 01 00 05 47 75 69 64 65
```

Decoded body length: 28 bytes. Pressing Next produces the same no-argument step response:

```text
3A 01 12 34 56 78 05 00 00 06
```

### Type 2: menu question

```text
30 02 01 12 34 56 78 00 40 1E 00 00 00 00 00 05
00 00 05 01 01 00 05 47 75 69 64 65 00 09 43 6F
6E 74 69 6E 75 65 3F 02 03 59 65 73 02 4E 6F
```

Decoded body length: 47 bytes. Selecting the first row, `Yes`, advances to step 6 and returns one-based choice 1:

```text
3A 01 12 34 56 78 05 00 00 06 01 01
```

### Type 3: simple menu question

```text
30 03 01 12 34 56 78 00 40 1E 00 00 00 00 00 05
00 00 05 01 01 00 05 47 75 69 64 65 02 03 59 65
73 02 4E 6F
```

Decoded body length: 36 bytes. Selecting `Yes` first sends a `CSay` containing `Yes`, then sends:

```text
3A 01 12 34 56 78 05 00 00 06 01 01
```

### Type 4: text input

```text
30 04 01 12 34 56 78 00 40 1E 00 00 00 00 00 05
00 00 05 01 01 00 05 47 75 69 64 65 00 09 43 6F
6E 74 69 6E 75 65 3F 05 4E 61 6D 65 3A 0D 01 2E
```

Decoded body length: 48 bytes. Submitting `Bob` advances to step 6 with argument type 2:

```text
3A 01 12 34 56 78 05 00 00 06 02 03 42 6F 62
```

### Type 5: simple text input

```text
30 05 01 12 34 56 78 00 40 1E 00 00 00 00 00 05
00 00 05 01 01 00 05 47 75 69 64 65 07 41 6E 73
77 65 72 3A 0D 01 2E
```

Decoded body length: 39 bytes. Submitting `Bob` first sends a `CSay` containing `Answer: Bob .`, then sends:

```text
3A 01 12 34 56 78 05 00 00 06 02 03 42 6F 62
```

### Type 6: face question

```text
30 06 01 12 34 56 78 00 40 1E 00 00 00 00 00 05
00 00 05 01 01 00 05 47 75 69 64 65 00 09 43 6F
6E 74 69 6E 75 65 3F 02 03 59 65 73 02 4E 6F
```

Decoded body length: 47 bytes. Selecting `Yes` returns:

```text
3A 01 12 34 56 78 05 00 00 06 01 01
```

This subtype skips the normal speaker-art refresh even though its body retains the common speaker fields.

### Type 9: protected ID/password

```text
30 09 01 12 34 56 78 00 40 1E 00 00 00 00 00 05
00 00 05 01 01 00 05 47 75 69 64 65 00 09 43 6F
6E 74 69 6E 75 65 3F 07 41 63 63 6F 75 6E 74 0D
06 53 75 62 6D 69 74
```

Decoded body length: 55 bytes. The server packet cannot force a response. The regional account manager must accept the form. If it produces the example result `approved`, the client sends:

```text
3A 01 12 34 56 78 05 00 00 06 02 08 61 70 70 72
6F 76 65 64
```

### Type 10: close command

```text
30 0A
```

Decoded body length: 2 bytes. The client closes the NPC session and sends no response.

Types 7 and 8 have no example because this client does not construct a known dialog subtype for them.

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

After queuing navigation or an answer, the client enters response-pending. It deactivates the answer pane, disables Previous and Next, and leaves Close available while it waits. A continuing pursuit must send another `SPursuitMessage` for the requested step. Close queues the current-step `CPursuit` and then closes the NPC session locally.

Choice indexes are sent one-based even though the dialog collection is indexed from zero. `maximum_input_bytes` is applied to the edit control. Type 9 builds a separate ID and masked-password dialog from `lnpcnid.txt`; its regional account manager must accept the form before the client emits an ordinary type-2 text response. The response contains a nonempty string produced in the protected pane's manager-result buffer. It does not serialize the ID and password controls directly.

The protected type-9 pane also has a secondary action that opens the configured item-shop URL through `ShellExecuteA`. This external-browser path is separate from the dormant in-client [`CCashShop`](../client/108-0x6c-cash-shop.md) and [`SItemShop`](069-0x45-item-shop.md) shopping-bag flow.

Simple menu type 3 first sends [`CSay`](../client/014-0x0e-say.md) containing the selected choice text. Simple text type 5 first sends `CSay` containing `input_prolog`, a space, the entered text, another space, and `input_epilog`. It then sends the normal `CPursuit` response.

## UI flow

`net_deserialize_pursuit_message_server_packet` builds the packet object. `ui_npc_session_open_pursuit_message` closes immediately for type 10; otherwise it updates `NPCSession` and creates `NPC_Pursuit_MessageDialog`. `ui_npc_pursuit_build_subtype` adds the question or input model.

`CreateUserDialogPane` also compares the raw decoded opcode with `0x30`. That lobby path immediately returns handled without reading the body or changing UI state. It therefore does not establish a second `0x30` body layout; the only parsed `0x30` server schema recovered from this client remains `SPursuitMessage`.

The outer pane uses `lnpcd.txt`. Choice dialogs use `lnpcd2.txt`, ordinary input uses `lnpcd4.txt`, and protected input uses `lnpcnid.txt`. The outer `DialogPane` attachment order makes actions 4, 5, and 6 Previous, Next, and Close. Actions 0 through 3 belong to the base name, content, and scrolling controls.

See [NPC dialogs](../../systems/npc-dialogs.md) for the complete pane and response model and [NPC dialog illustrations](../../systems/npc-dialog-illustrations.md) for the optional speaker art.

## Paired packet

Every navigation or answer uses [`CPursuit`](../client/058-0x3a-pursuit.md). `0x3A` is one of only two client opcodes with the dialog-response inner wrapper described in [Packet transforms](../packet-transforms.md#dialog-response-inner-wrapper).

## Known limits

The target-type values are echoed back but not decoded into a complete local enum in this path.
