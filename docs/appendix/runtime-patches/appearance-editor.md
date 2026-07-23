# Appearance editor

This runtime patch makes the client's dormant hair and appearance editor available through one patch-private server message. It reserves screen-menu type `12`, opens the existing `FaceMenuDialog` as a standalone pane, and leaves the stock `SScreenMenu` types 0 through 11 unchanged.

The patch does not recreate the editor or revive the incompatible `MerchantSession`. It reuses the stock layout loader, `FaceMenuDialog`, `UserShapeControlPane`, button handlers, timer, `CMerchant` sender, and standalone close path.

See [NPC dialogs](../../systems/npc-dialogs.md#dormant-hair-styling-dialog), [Screen Menu (`SScreenMenu`)](../../network/server/047-0x2f-screen-menu.md), and [Merchant (`CMerchant`)](../../network/client/057-0x39-merchant.md).

## Behavior

The server sends an opcode-`0x2F` decoded body whose second byte is the otherwise unsupported menu type `12`. The injected deserializer wrapper recognizes only that pair:

```text
opcode 0x2F and menu type 12
    -> validate the patch-private body
    -> load the dormant merchant layouts once
    -> construct FaceMenuDialog with no MerchantSession owner
    -> register it under the normal root pane
    -> consume the raw body before ordinary NPC dispatch

every other body
    -> call net_deserialize_server_packet unchanged
```

Opening the dialog copies the current character's gender, hair style, and hair color. Each value is clamped to the server-supplied range. The `UserShapeControlPane` preview animates through four frames at 300 ms per frame. Rotation changes only the preview direction and is never sent.

The editor closes after Submit, Target information, Cancel, or Escape. Submit sends the stock special `CMerchant` appearance body. Target information sends the stock object-information request. Cancel and Escape send nothing.

## Why intercept deserialization

The live `NPCSession` parser expects the current `SScreenMenu` common header, including `show_graphic` and `speaker_name`. `FaceMenuDialog` expects an older, shorter body. Adding type 12 to the live nested-model switch would still leave the two pane families and payload layouts incompatible.

The hook runs after transport decoding but before a typed `SScreenMenu` object is created. A patch-private type-12 body can therefore use the exact legacy layout consumed by `FaceMenuDialog`. Constructing the dialog with owner zero selects the existing standalone activation and cleanup paths, so no dormant `MerchantSession` remains registered to misread later current-format packets.

## Target

Target fingerprint:

```text
File: Darkages.exe
Size: 3,112,960 bytes
SHA-256: 054A5D6ADC56099C6BFD9D2A58675AFF62DC788B63209A3D906492F5B89E96C6
Preferred image base: 0x00400000
```

`event_dispatch` calls the typed server-packet deserializer after transport decoding and before the pane tree sees the event.

| Purpose | Static address | RVA | File offset | Original bytes | Replacement template |
| --- | ---: | ---: | ---: | --- | --- |
| Intercept server-packet deserialization | `0x00464982` | `0x00064982` | `0x00063D82` | `E8 69 1A 13 00` | `E8 rr rr rr rr` |

The file offset is reference information only. A launcher must patch `loaded_module_base + 0x00064982`.

```diff
- 00064982: E8 69 1A 13 00 | call net_deserialize_server_packet
+ 00064982: E8 rr rr rr rr | call appearance_editor_deserialize_hook
```

`rr rr rr rr` is the signed little-endian displacement from `loaded_module_base + 0x00064987` to the allocated stub.

At entry to the replacement call:

| Value | Location |
| --- | --- |
| Server-packet factory `this` | `ECX` |
| Opcode copied from decoded byte zero | `[ESP+0x04]` |
| Decoded body pointer | `[ESP+0x08]` |
| Decoded body length | `[ESP+0x0C]` |

The original function uses `thiscall`, returns the typed packet pointer in `EAX`, and removes twelve argument bytes. The stub preserves that ABI. Nonmatching traffic returns the original function's result. A matching type-12 body returns null after opening the standalone dialog.

## Native dependencies

| Name | Static address | RVA | Use |
| --- | ---: | ---: | --- |
| `memory_allocate_zeroed` | `0x004B44D0` | `0x000B44D0` | Allocate and clear the 0xB94-byte dialog |
| `ui_load_merchant_dialog_layouts` | `0x004CC970` | `0x000CC970` | Load `lmerc`, `lmerd`, and related cached layout state once |
| `ui_get_merchant_detail_dialog_bounds` | `0x004CD5E0` | `0x000CD5E0` | Obtain the `lmerd` dialog bounds |
| `ui_merchant_dialog_pane_activate` | `0x004CDC00` | `0x000CDC00` | Register an ownerless dialog under the root pane |
| `ui_merchant_face_menu_dialog_ctor` | `0x004D5EB0` | `0x000D5EB0` | Parse the legacy body and construct `FaceMenuDialog` |
| `net_deserialize_server_packet` | `0x005963F0` | `0x001963F0` | Preserve all non-type-12 packet behavior |

The dialog's existing Submit handler reaches `net_send_merchant_face_menu_selection`. The stub does not build an outbound packet or call the socket layer.

## Patch-private activation body

The server must send this as the decoded opcode-first body of an ordinary derived-transform server packet. This is not the normal typed `SScreenMenu` body:

```text
record appearance_editor_open_body {
    u8       opcode                         // 0x2F
    u8       patched_menu_type              // 12
    u8       target_type
    u32      target_id
    u8       ignored_unknown
    u16      speaker_sprite
    u8       speaker_color
    bytes    ignored_secondary[4]
    string16 content
    u8       gender_min                     // 1 male, 2 female
    u8       gender_max
    u8       hair_style_min                 // 1 through 18
    u8       hair_style_max
    u8       hair_color_min                 // 0 through 13
    u8       hair_color_max
    u16      retained_unknown
}
```

All multibyte values are big-endian. `content` is raw client text bytes, not Unicode. The injected gate accepts at most 255 content bytes and requires an exact total body length of `25 + content_length`.

The gate also requires:

- `1 <= gender_min <= gender_max <= 2`
- `1 <= hair_style_min <= hair_style_max <= 18`
- `0 <= hair_color_min <= hair_color_max <= 13`

The female character-creation UI exposes hair styles only through 17. A server that permits female selection should cap `hair_style_max` at 17 unless style 18 has been verified separately.

`retained_unknown` is stored by the dormant constructor but is not included in the appearance response. Its gameplay purpose remains unresolved. The sample uses `0x0078`, matching the constructor's built-in fallback value.

## Sample activation

This 42-byte decoded body opens a male-only barber dialog for target `0x12345678`. It permits hair styles 1 through 18 and hair colors 0 through 13:

```text
2F 0C 01 12 34 56 78 00
40 1E 00 00 00 00 00 00
11 43 68 6F 6F 73 65 20
79 6F 75 72 20 73 74 79
6C 65 01 01 01 12 00 0D
00 78
```

Decoded fields:

```text
opcode              = 0x2F
patched_menu_type   = 12
target_type         = 1
target_id           = 0x12345678
speaker_sprite      = 0x401E
content             = "Choose your style"
gender range        = 1..1
hair-style range    = 1..18
hair-color range    = 0..13
retained_unknown    = 0x0078
```

The normal server-to-client opcode-`0x2F` derived transform and receive sequence still apply. The example above is the plaintext body after transport decoding, not a complete `0xAA` frame or encrypted wire capture.

## Expected client messages

### Submit

If the player chooses hair style 9, male, and hair color 4, Submit produces this nine-byte meaningful `CMerchant` body:

```text
39 01 12 34 56 78 09 01 04
```

```text
record appearance_editor_submit_body {
    u8  opcode                         // 0x39
    u8  target_type                    // echoed
    u32 target_id                      // echoed
    u8  hair_style
    u8  gender                         // 1 male, 2 female
    u8  hair_color
}
```

There is no `u16 pursuit_id`. `net_submit_client_packet` applies the nondeterministic dialog-response inner wrapper, then the normal derived transform for opcode `0x39`, then framing. The transmitted bytes cannot be predicted from the meaningful body alone because the wrapper contains random bytes and the outer transform uses live sequence and session state.

The client closes the dialog immediately after submission. It does not wait for a dedicated appearance-editor acknowledgement. The server must validate and apply the selection, then use its normal world-object refresh flow to make the accepted appearance visible.

### Target information

The Target information button sends:

```text
43 01 12 34 56 78
```

This is the meaningful [`CRequestObjectInfo`](../../network/client/067-0x43-request-object-info.md) body: opcode `0x43`, subtype `1`, and the echoed target ID. Ordinary submission appends its transport zero before the static transform. The dialog then closes.

### Cancel, Escape, arrows, and rotation

Cancel and Escape close the standalone dialog locally and send no packet. Gender, hair, color, and rotation buttons also send nothing until Submit. Rotation is never part of a client message.

The server should treat local close as an abandoned editor transaction and should not wait indefinitely for a cancellation packet.

## Injected stub template

The stub is 0x128 bytes. External calls use zeroed `rel32` placeholders. Internal branches and stack cleanup are already encoded.

```text
000: 55                         | push ebp
001: 89 E5                      | mov ebp, esp
003: 53                         | push ebx
004: 56                         | push esi
005: 57                         | push edi
006: 83 EC 10                   | sub esp, 0x10            ; local RECT
009: 89 CB                      | mov ebx, ecx             ; preserve factory this
00B: 83 7D 08 2F                | cmp dword [ebp+8], 0x2F
00F: 0F 85 F7 00 00 00          | jne fallback
015: 8B 75 0C                   | mov esi, [ebp+0x0C]      ; decoded body
018: 85 F6                      | test esi, esi
01A: 0F 84 EC 00 00 00          | je fallback
020: 83 7D 10 02                | cmp dword [ebp+0x10], 2
024: 0F 82 E2 00 00 00          | jb fallback
02A: 80 3E 2F                   | cmp byte [esi], 0x2F
02D: 0F 85 D9 00 00 00          | jne fallback
033: 80 7E 01 0C                | cmp byte [esi+1], 12
037: 0F 85 CF 00 00 00          | jne fallback
03D: 83 7D 10 19                | cmp dword [ebp+0x10], 25
041: 0F 82 BE 00 00 00          | jb consume
047: 0F B6 46 0F                | movzx eax, byte [esi+0x0F]
04B: C1 E0 08                   | shl eax, 8
04E: 0F B6 56 10                | movzx edx, byte [esi+0x10]
052: 09 D0                      | or eax, edx              ; content length
054: 3D FF 00 00 00             | cmp eax, 255
059: 0F 87 A6 00 00 00          | ja consume
05F: 8D 50 19                   | lea edx, [eax+25]
062: 39 55 10                   | cmp [ebp+0x10], edx
065: 0F 85 9A 00 00 00          | jne consume              ; require exact length
06B: 8D 7C 06 11                | lea edi, [esi+eax+0x11]  ; range tail
06F: 0F B6 0F                   | movzx ecx, byte [edi]
072: 83 F9 01                   | cmp ecx, 1
075: 0F 82 8A 00 00 00          | jb consume
07B: 83 F9 02                   | cmp ecx, 2
07E: 0F 87 81 00 00 00          | ja consume
084: 0F B6 57 01                | movzx edx, byte [edi+1]
088: 39 CA                      | cmp edx, ecx
08A: 72 79                      | jb consume
08C: 83 FA 02                   | cmp edx, 2
08F: 77 74                      | ja consume
091: 0F B6 4F 02                | movzx ecx, byte [edi+2]
095: 83 F9 01                   | cmp ecx, 1
098: 72 6B                      | jb consume
09A: 83 F9 12                   | cmp ecx, 18
09D: 77 66                      | ja consume
09F: 0F B6 57 03                | movzx edx, byte [edi+3]
0A3: 39 CA                      | cmp edx, ecx
0A5: 72 5E                      | jb consume
0A7: 83 FA 12                   | cmp edx, 18
0AA: 77 59                      | ja consume
0AC: 0F B6 4F 04                | movzx ecx, byte [edi+4]
0B0: 83 F9 0D                   | cmp ecx, 13
0B3: 77 50                      | ja consume
0B5: 0F B6 57 05                | movzx edx, byte [edi+5]
0B9: 39 CA                      | cmp edx, ecx
0BB: 72 48                      | jb consume
0BD: 83 FA 0D                   | cmp edx, 13
0C0: 77 43                      | ja consume
0C2: 31 C9                      | xor ecx, ecx
0C4: E8 00 00 00 00             | call ui_load_merchant_dialog_layouts
0C9: 8D 45 E4                   | lea eax, [ebp-0x1C]
0CC: 50                         | push eax
0CD: 31 C9                      | xor ecx, ecx
0CF: E8 00 00 00 00             | call ui_get_merchant_detail_dialog_bounds
0D4: 6A 00                      | push 0
0D6: 68 94 0B 00 00             | push 0xB94
0DB: E8 00 00 00 00             | call memory_allocate_zeroed
0E0: 83 C4 08                   | add esp, 8
0E3: 85 C0                      | test eax, eax
0E5: 74 1E                      | je consume
0E7: 89 C7                      | mov edi, eax
0E9: 6A 00                      | push 0                    ; no MerchantSession owner
0EB: 8D 46 02                   | lea eax, [esi+2]          ; legacy payload
0EE: 50                         | push eax
0EF: 8D 45 E4                   | lea eax, [ebp-0x1C]
0F2: 50                         | push eax
0F3: 89 F9                      | mov ecx, edi
0F5: E8 00 00 00 00             | call ui_merchant_face_menu_dialog_ctor
0FA: 85 C0                      | test eax, eax
0FC: 74 07                      | je consume
0FE: 89 C1                      | mov ecx, eax
100: E8 00 00 00 00             | call ui_merchant_dialog_pane_activate
105: C6 06 00                   | mov byte [esi], 0         ; hide custom raw event
108: 31 C0                      | xor eax, eax              ; no typed packet
10A: EB 10                      | jmp done
10C: FF 75 10                   | push dword [ebp+0x10]    ; fallback length
10F: FF 75 0C                   | push dword [ebp+0x0C]    ; fallback body
112: FF 75 08                   | push dword [ebp+8]        ; fallback opcode
115: 89 D9                      | mov ecx, ebx
117: E8 00 00 00 00             | call net_deserialize_server_packet
11C: 83 C4 10                   | add esp, 0x10
11F: 5F                         | pop edi
120: 5E                         | pop esi
121: 5B                         | pop ebx
122: 89 EC                      | mov esp, ebp
124: 5D                         | pop ebp
125: C2 0C 00                   | ret 0x0C
```

The write at offset `0x105` changes only the patch-private event's copied decoded body. `event_dispatch` has already cached its opcode argument. Returning a null typed packet prevents the live `NPCSession` path from seeing type 12, and changing raw byte zero prevents any raw pane handler from treating the same event as another `SScreenMenu`.

## Stub relocations

For each `rel32`, write:

```text
target_runtime - (stub_runtime + instruction_offset + 5)
```

| Operand offset | Instruction offset | Target |
| ---: | ---: | --- |
| `0x0C5` | `0x0C4` | `loaded_base + 0x000CC970` |
| `0x0D0` | `0x0CF` | `loaded_base + 0x000CD5E0` |
| `0x0DC` | `0x0DB` | `loaded_base + 0x000B44D0` |
| `0x0F6` | `0x0F5` | `loaded_base + 0x000D5EB0` |
| `0x101` | `0x100` | `loaded_base + 0x000CDC00` |
| `0x118` | `0x117` | `loaded_base + 0x001963F0` |

The hook-site displacement uses:

```text
stub_runtime - (loaded_base + 0x00064987)
```

The launcher should keep the final stub page execute-read, not writable-executable.

## Installation and removal

Use the [safe launcher](safe-launcher.md). Require the exact target fingerprint and verify `E8 69 1A 13 00` before changing the call.

Start the process suspended, allocate at least 0x128 bytes, apply every stub relocation, write the stub, and change its final protection to execute-read. Replace the call only after the complete stub is valid. Restore page protection, flush the instruction cache for both ranges, and resume only when all steps succeed.

If any validation, allocation, relocation, protection, or write fails, restore the original call before resuming or terminate the still-suspended process. Never modify `Darkages.exe`.

Removal requires a suspended process, restoration of the verified original call, an instruction-cache flush, and release of the stub allocation. Suspend every client thread before removal so none can be executing inside the stub.

## Test checklist

1. Confirm ordinary server packets and `SScreenMenu` types 0 through 11 still reach `net_deserialize_server_packet`.
2. Send the sample type-12 body and confirm that one standalone `FaceMenuDialog` opens.
3. Verify that the initial preview is the current character appearance clamped to the supplied bounds.
4. Verify the 300 ms four-frame preview and the preview-only rotation buttons.
5. Submit a known combination and inspect the nine-byte meaningful `CMerchant` body before its inner wrapper.
6. Use Target information and inspect `43 01` plus the echoed target ID.
7. Confirm Cancel and Escape close locally without a client packet.
8. Send malformed lengths and ranges and confirm that no dialog opens and no typed packet is constructed.
9. Close the editor before sending another activation. Repeated concurrent type-12 dialogs are not supported.

## Known limits

- This patch defines a private protocol extension. An unpatched 7.41 client does not understand type 12.
- The server must not send the ordinary current `SScreenMenu` header for type 12. It must send the shorter body documented here.
- The patch validates the confirmed character-creation ranges. It does not expose unverified hair or palette IDs.
- The target-type enum and `retained_unknown` meaning remain unresolved.
- The client sends no explicit cancellation packet.
- The client does not apply server-side appearance state by itself. The server must accept the `CMerchant` form and publish the resulting world appearance through its normal update flow.
- Open only one appearance editor at a time and do not overlap it with another NPC conversation.
