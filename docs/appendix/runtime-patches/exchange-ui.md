# Exchange UI

These changes make `ExchangeDialog` draggable and optionally suppress or redirect its final alerts. The patch does not change the main-UI layout or inventory expansion state.

The pure byte patches and the hook design target only this client:

```text
File: Darkages.exe
Size: 3,112,960 bytes
SHA-256: 054A5D6ADC56099C6BFD9D2A58675AFF62DC788B63209A3D906492F5B89E96C6
Preferred image base: 0x00400000
```

Use the actual module base plus each RVA at runtime. Apply changes only after verifying the fingerprint and the complete original byte sequence.

## Make ExchangeDialog draggable

`ExchangeDialog` inherits the standard `DialogPane` pointer handler. Its constructor disables movement by writing zero to `this + 0x62C`. Changing only that immediate enables the existing movement path.

At static address `0x00469E33` (RVA `0x00069E33`, file offset `0x00069233` for reference), replace:

```diff
- 000: C7 82 2C 06 00 00 00 00 00 00 | mov dword ptr [edx+0x62C], 0 ; disable native dragging
+ 000: C7 82 2C 06 00 00 01 00 00 00 | mov dword ptr [edx+0x62C], 1 ; enable native dragging
```

This does not add a custom drag handler. Controls keep their normal hit testing, while unused dialog background can start a drag through primary-vtable slot `+0x48`.

## Suppress the two final alerts

Both close paths allocate a `0x634`-byte one-button alert and already handle allocation failure by skipping construction. Replacing the allocation sequence with `EAX = 0` takes that existing no-alert branch without allocating or leaking an object. The exchange-removal call remains unchanged.

For Cancelled event `0x04`, patch static address `0x0046AA81` (RVA `0x0006AA81`, file offset `0x00069E81` for reference):

```diff
- 000: 6A 00                         | push 0                     ; allocation helper argument
- 002: 68 34 06 00 00                | push 0x634                 ; allocate one alert object
- 007: E8 43 9A 04 00                | call allocation_helper     ; construct the final popup
+ 000: 31 C0                         | xor eax, eax                ; take the existing allocation-failure branch
+ 002: 90 90 90 90 90 90 90 90 90 90 | nop x10                    ; fill the verified 12-byte block
```

For final Accepted event `0x05`, patch static address `0x0046AC57` (RVA `0x0006AC57`, file offset `0x0006A057` for reference):

```diff
- 000: 6A 00                         | push 0                     ; allocation helper argument
- 002: 68 34 06 00 00                | push 0x634                 ; allocate one alert object
- 007: E8 6D 98 04 00                | call allocation_helper     ; construct the final popup
+ 000: 31 C0                         | xor eax, eax                ; take the existing allocation-failure branch
+ 002: 90 90 90 90 90 90 90 90 90 90 | nop x10                    ; fill the verified 12-byte block
```

Apply both rows to suppress both messages. Event `0x05` reaches its patched block only after both parties are accepted. Earlier acceptance updates still redraw the acknowledgement state and keep the dialog open.

## Redirect the text to the floating message bar

Redirection needs a detour because the visible text is packet data. The narrow design combines the no-alert patches above with hooks at the two event handlers:

| Role | Static address | RVA | Use |
| --- | --- | --- | --- |
| Cancelled handler | `0x0046A9E0` | `0x0006A9E0` | Hook entry; continue at `0x0046A9E5` |
| Accepted handler | `0x0046AB20` | `0x0006AB20` | Hook entry; continue at `0x0046AB25` |
| Floating palette append | `0x004803A0` | `0x000803A0` | Existing text append helper called by each stub |

For Cancelled, the decoded body is:

```text
[0] opcode, [1] event, [2] party, [3] length, [4..] message
```

For Accepted, append only when the incoming party will complete the pair. Party zero will complete when `other_accepted` at `ExchangeDialog +0x636` is already one. A nonzero party will complete when `local_accepted` at `+0x635` is already one.

Copy at most 130 bytes to a hook-owned stack buffer, add a null terminator, append it with palette `0x58`, then append the normal newline. Afterward run the original handler through its trampoline. With the no-alert patch installed, the native handler still updates state and removes the exchange but creates no popup.

This mirrors only the floating `SMessage` type `0x00` display branch. Do not call the network parser recursively. If persistent history is also required, queue a bounded synthetic message event for the normal main-thread dispatcher.

## Annotated result stubs

The optional detour uses separate cancelled and accepted stubs. Zero operands mark addresses or relative displacements that the builder must relocate for the actual module and stub bases.

### Cancelled result

The cancelled handler always has a final result message, so this wrapper only bounds and displays it before returning to the original handler.

```text
000: 55                         | push ebp                  ; start the wrapper frame
001: 89 E5                      | mov ebp, esp
003: 81 EC 88 00 00 00          | sub esp, 0x88             ; reserve a 136-byte local message buffer
009: 53                         | push ebx                  ; preserve caller registers
00A: 56                         | push esi
00B: 57                         | push edi
00C: 89 4D FC                   | mov [ebp-4], ecx          ; save the ExchangeDialog pointer
00F: 8B 5D 08                   | mov ebx, [ebp+8]          ; load the decoded packet body
012: 0F B6 4B 03                | movzx ecx, byte ptr [ebx+3] ; read message byte length
016: 81 F9 82 00 00 00          | cmp ecx, 130              ; enforce the hook-owned buffer limit
01C: 76 05                      | jbe copy_message
01E: B9 82 00 00 00             | mov ecx, 130              ; truncate an oversized message
copy_message:
023: 8D 73 04                   | lea esi, [ebx+4]          ; source is the packet message
026: 8D BD 78 FF FF FF          | lea edi, [ebp-0x88]       ; destination is the local buffer
02C: FC                         | cld                       ; copy forward
02D: F3 A4                      | rep movsb                 ; copy the bounded byte count
02F: C6 07 00                   | mov byte ptr [edi], 0     ; null-terminate for the UI helper
032: 6A 58                      | push 0x58                 ; use the normal result-message palette
034: 8D 85 78 FF FF FF          | lea eax, [ebp-0x88]       ; load bounded message text
03A: 50                         | push eax
03B: E8 00 00 00 00             | call floating_palette_append ; append the result message
040: 83 C4 08                   | add esp, 8                ; remove helper arguments
043: 6A 58                      | push 0x58                 ; use the same palette for newline
045: 68 00 00 00 00             | push floating_newline     ; append the client's normal newline text
04A: E8 00 00 00 00             | call floating_palette_append
04F: 83 C4 08                   | add esp, 8                ; remove helper arguments
052: 5F                         | pop edi                   ; restore caller registers
053: 5E                         | pop esi
054: 5B                         | pop ebx
055: 8B 4D FC                   | mov ecx, [ebp-4]          ; restore the ExchangeDialog pointer
058: 89 EC                      | mov esp, ebp              ; discard the wrapper frame
05A: 5D                         | pop ebp
05B: 55                         | push ebp                  ; replay displaced handler prologue
05C: 89 E5                      | mov ebp, esp
05E: 6A FF                      | push -1
060: E9 00 00 00 00             | jmp cancelled_continuation ; let the native handler update and close the exchange
```

### Accepted result

The accepted handler displays its message only when the incoming acceptance completes the pair. The remainder is the same bounded append and native-handler handoff.

```text
000: 55                         | push ebp                  ; start the wrapper frame
001: 89 E5                      | mov ebp, esp
003: 81 EC 88 00 00 00          | sub esp, 0x88             ; reserve a 136-byte local message buffer
009: 53                         | push ebx                  ; preserve caller registers
00A: 56                         | push esi
00B: 57                         | push edi
00C: 89 4D FC                   | mov [ebp-4], ecx          ; save the ExchangeDialog pointer
00F: 8B 5D 08                   | mov ebx, [ebp+8]          ; load the decoded packet body
012: 80 7B 02 00                | cmp byte ptr [ebx+2], 0   ; did the local party accept?
016: 0F 85 15 00 00 00          | jne check_local_accepted ; no, test the local state instead
01C: 8B 45 FC                   | mov eax, [ebp-4]          ; reload the ExchangeDialog pointer
01F: 80 B8 36 06 00 00 01       | cmp byte ptr [eax+0x636], 1 ; has the other party already accepted?
026: 0F 85 55 00 00 00          | jne skip_message         ; this event does not complete the pair
02C: E9 10 00 00 00             | jmp display_message      ; both parties are now accepted
check_local_accepted:
031: 8B 45 FC                   | mov eax, [ebp-4]          ; reload the ExchangeDialog pointer
034: 80 B8 35 06 00 00 01       | cmp byte ptr [eax+0x635], 1 ; has the local party already accepted?
03B: 0F 85 40 00 00 00          | jne skip_message         ; this event does not complete the pair
display_message:
041: 0F B6 4B 03                | movzx ecx, byte ptr [ebx+3] ; read message byte length
045: 81 F9 82 00 00 00          | cmp ecx, 130              ; enforce the hook-owned buffer limit
04B: 76 05                      | jbe copy_message
04D: B9 82 00 00 00             | mov ecx, 130              ; truncate an oversized message
copy_message:
052: 8D 73 04                   | lea esi, [ebx+4]          ; source is the packet message
055: 8D BD 78 FF FF FF          | lea edi, [ebp-0x88]       ; destination is the local buffer
05B: FC                         | cld                       ; copy forward
05C: F3 A4                      | rep movsb                 ; copy the bounded byte count
05E: C6 07 00                   | mov byte ptr [edi], 0     ; null-terminate for the UI helper
061: 6A 58                      | push 0x58                 ; use the normal result-message palette
063: 8D 85 78 FF FF FF          | lea eax, [ebp-0x88]       ; load bounded message text
069: 50                         | push eax
06A: E8 00 00 00 00             | call floating_palette_append ; append the result message
06F: 83 C4 08                   | add esp, 8                ; remove helper arguments
072: 6A 58                      | push 0x58                 ; use the same palette for newline
074: 68 00 00 00 00             | push floating_newline     ; append the client's normal newline text
079: E8 00 00 00 00             | call floating_palette_append
07E: 83 C4 08                   | add esp, 8                ; remove helper arguments
skip_message:
081: 5F                         | pop edi                   ; restore caller registers
082: 5E                         | pop esi
083: 5B                         | pop ebx
084: 8B 4D FC                   | mov ecx, [ebp-4]          ; restore the ExchangeDialog pointer
087: 89 EC                      | mov esp, ebp              ; discard the wrapper frame
089: 5D                         | pop ebp
08A: 55                         | push ebp                  ; replay displaced handler prologue
08B: 89 E5                      | mov ebp, esp
08D: 6A FF                      | push -1
08F: E9 00 00 00 00             | jmp accepted_continuation ; let the native handler update and close the exchange
```

Relocate the two calls to `module_base + 0x000803A0`, the newline pointer to `module_base + 0x0028BC68`, and the final jump to the matching handler continuation. The cancelled operand offsets are `0x3C`, `0x46`, `0x4B`, and `0x61`; the accepted offsets are `0x6B`, `0x75`, `0x7A`, and `0x90`.

Each verified handler entry receives only this five-byte hook:

```diff
- 000: 55             | push ebp                  ; displaced handler prologue
- 001: 8B EC          | mov ebp, esp
- 003: 6A FF          | push -1
+ 000: E9 <signed-rel32> | jmp exchange_result_stub ; enter the matching relocated wrapper
```

## Installation scope

The draggable-dialog change and the two no-alert changes are independent, same-size byte patches. Redirecting alert text to the floating message bar remains an optional detour.

No constructor hook, destructor hook, exchange pointer tracking, or `GUIBackPane` layout save and restore is required. The player can drag the exchange window away from the expanded inventory instead of temporarily forcing the small main-UI layout.

Apply all code changes with the [safe launcher workflow](safe-launcher.md). Resolve addresses from the loaded module base, and never wait for controller IPC from a text-redirection hook.
