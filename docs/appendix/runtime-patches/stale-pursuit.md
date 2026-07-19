# Stale pursuit

This runtime patch gives an unanswered pursuit dialog one deliberate recovery path. It remembers the exact pursuit context when the client enters response-pending state. If Escape finishes normal event dispatch without sending the native Close, the patch submits the cached ten-byte `CPursuit` Close body and then dispatches a synthetic `SPursuitMessage` Close acknowledgement through the client's normal event path.

The patch does not close every dialog or send on a timer. The pursuit Close button keeps its native path. The fallback passes decoded body `30 0A` to `net_post_decoded_server_packet_event`, which constructs the typed packet and lets the ordinary pane handlers close client-side pursuit state. This local message does not advance the receive cipher.

See [NPC dialogs](../../systems/npc-dialogs.md), [Pursuit (CPursuit)](../../network/client/058-0x3a-pursuit.md), and [Pursuit Message (SPursuitMessage)](../../network/server/048-0x30-pursuit-message.md).

## Behavior

Five non-close pursuit actions converge on `ui_npc_session_set_response_pending`. Each patched call first copies these values from `NPCSession` into patch-owned storage:

```c
struct StalePursuitState {
    u8  pending;       // +0x00
    u8  target_type;   // +0x01
    u8  reserved[2];   // +0x02
    u32 target_id;     // +0x04, host order
    u16 pursuit_id;    // +0x08, host order
    u16 step_id;       // +0x0A, host order
    u32 armed_at_ms;   // +0x0C, GetTickCount
};
```

The key hook records whether the event is Escape before passing the event to `event_dispatch_or_queue`. It reads no event fields after that call. When normal dispatch returns, the hook sends a fallback only when `pending` is still set and no more than 30,000 ms have passed since the unanswered response began.

Normal Close clears `pending` before tail-calling `net_send_pursuit_close_current`. Any new `SPursuitMessage` clears it before tail-calling `ui_npc_session_open_pursuit_message`. These two gates prevent the ordinary Close and the fallback from both sending.

The 30,000 ms window is a patch constant measured from the player's answer. It is not the reactor lifetime. Expiry only discards the cached context and never sends automatically. A successful fallback first queues the real client Close, then simulates the missing server acknowledgement locally.

## Hook sites

The preferred image base is `0x00400000`. File offsets are reference information only. A launcher uses the loaded module base plus the RVA.

| Purpose | Static address | RVA | File offset | Verified original bytes | Stub entry |
|---|---:|---:|---:|---|---:|
| Previous becomes pending | `0x0053D9B7` | `0x0013D9B7` | `0x0013CDB7` | `E8 64 E6 FE FF` | `stub + 0x000` |
| Next becomes pending | `0x0053DA71` | `0x0013DA71` | `0x0013CE71` | `E8 AA E5 FE FF` | `stub + 0x000` |
| Menu answer becomes pending | `0x0053DCE1` | `0x0013DCE1` | `0x0013D0E1` | `E8 3A E3 FE FF` | `stub + 0x000` |
| Text answer becomes pending | `0x0053E1AF` | `0x0013E1AF` | `0x0013D5AF` | `E8 6C DE FE FF` | `stub + 0x000` |
| Protected text answer becomes pending | `0x0053F194` | `0x0013F194` | `0x0013E594` | `E8 87 CE FE FF` | `stub + 0x000` |
| Native pursuit Close | `0x0053CDE1` | `0x0013CDE1` | `0x0013C1E1` | `E8 AA 0C 00 00` | `stub + 0x04F` |
| Open incoming pursuit message | `0x0052C799` | `0x0012C799` | `0x0012BB99` | `E8 B2 01 00 00` | `stub + 0x05B` |
| Dispatch key-down event | `0x00467DE1` | `0x00067DE1` | `0x000671E1` | `E8 0A F3 FF FF` | `stub + 0x067` |

Every replacement remains one complete five-byte call:

```diff
- E8 <verified original rel32>
+ E8 00 00 00 00
```

For each replacement, write `rel32 = stub_entry - (module_base + site_rva + 5)` in little-endian order.

## Native dependencies

| Name | Static address | RVA | Use |
|---|---:|---:|---|
| `event_dispatch_or_queue` | `0x004670F0` | `0x000670F0` | Perform normal event propagation first |
| `ui_npc_session_set_response_pending` | `0x0052C020` | `0x0012C020` | Preserve the original pending transition |
| `ui_npc_session_open_pursuit_message` | `0x0052C950` | `0x0012C950` | Preserve incoming `SPursuitMessage` handling |
| `net_send_pursuit_close_current` | `0x0053DA90` | `0x0013DA90` | Preserve the native Close-button path |
| `net_submit_client_packet` | `0x00563E00` | `0x00163E00` | Submit the fallback plaintext body |
| `net_post_decoded_server_packet_event` | `0x00467060` | `0x00067060` | Dispatch decoded `30 0A` through the normal server-packet event path |
| `GetTickCount` import thunk | `0x0061FEC4` | `0x0021FEC4` | Bound the cached context lifetime |
| communications manager pointer | `0x0073D958` | `0x0033D958` | `this` for packet submission |

`net_submit_client_packet` is the outbound boundary. For opcode `0x3A`, it applies the dialog wrapper, CRC, configured transform, client sequence, and asynchronous communications queue. The patch does not write to the socket or own sequence state.

`net_post_decoded_server_packet_event` is the inbound simulation boundary. Its `this` pointer is the event dispatcher stored at `communications_manager + 0x74`. It copies the two-byte body, creates event type `0x13`, constructs `SPursuitMessage` during dispatch, and reaches the same NPC-session Close handler as a real decoded packet.

## Injected stub template

Allocate and zero at least `0x150` bytes in the target process. Bytes `0x000` through `0x131` are code. Bytes `0x132` through `0x13F` are padding. `StalePursuitState` begins at `stub + 0x140`.

All zeroed `abs32` and `rel32` operands below are relocation placeholders.

```text
000: C6 05 00 00 00 00 00 | mov byte [pending], 0
007: 8A 81 A1 02 00 00    | mov al, [ecx+0x2A1]
00D: A2 00 00 00 00       | mov [target_type], al
012: 8B 81 A4 02 00 00    | mov eax, [ecx+0x2A4]
018: A3 00 00 00 00       | mov [target_id], eax
01D: 66 8B 81 AC 02 00 00 | mov ax, [ecx+0x2AC]
024: 66 A3 00 00 00 00    | mov [pursuit_id], ax
02A: 66 8B 81 AE 02 00 00 | mov ax, [ecx+0x2AE]
031: 66 A3 00 00 00 00    | mov [step_id], ax
037: 51                   | push ecx
038: E8 00 00 00 00       | call GetTickCount
03D: 59                   | pop ecx
03E: A3 00 00 00 00       | mov [armed_at_ms], eax
043: C6 05 00 00 00 00 01 | mov byte [pending], 1
04A: E9 00 00 00 00       | jmp ui_npc_session_set_response_pending

04F: C6 05 00 00 00 00 00 | mov byte [pending], 0
056: E9 00 00 00 00       | jmp net_send_pursuit_close_current

05B: C6 05 00 00 00 00 00 | mov byte [pending], 0
062: E9 00 00 00 00       | jmp ui_npc_session_open_pursuit_message

067: 55                   | push ebp
068: 89 E5                | mov ebp, esp
06A: 53                   | push ebx
06B: 56                   | push esi
06C: 57                   | push edi
06D: 31 DB                | xor ebx, ebx
06F: 8B 7D 08             | mov edi, [ebp+8]
072: 80 7F 0C 08          | cmp byte [edi+0x0C], 8
076: 75 08                | jne 0x080
078: 80 7F 10 1B          | cmp byte [edi+0x10], 0x1B
07C: 75 02                | jne 0x080
07E: B3 01                | mov bl, 1
080: 57                   | push edi
081: E8 00 00 00 00       | call event_dispatch_or_queue
086: 89 C6                | mov esi, eax
088: 84 DB                | test bl, bl
08A: 0F 84 99 00 00 00    | je 0x129
090: 80 3D 00 00 00 00 01 | cmp byte [pending], 1
097: 0F 85 8C 00 00 00    | jne 0x129
09D: E8 00 00 00 00       | call GetTickCount
0A2: 2B 05 00 00 00 00    | sub eax, [armed_at_ms]
0A8: 3D 30 75 00 00       | cmp eax, 30000
0AD: 77 73                | ja 0x122
0AF: C6 05 00 00 00 00 00 | mov byte [pending], 0
0B6: 83 EC 0C             | sub esp, 12
0B9: C6 04 24 3A          | mov byte [esp], 0x3A
0BD: A0 00 00 00 00       | mov al, [target_type]
0C2: 88 44 24 01          | mov [esp+1], al
0C6: A1 00 00 00 00       | mov eax, [target_id]
0CB: 0F C8                | bswap eax
0CD: 89 44 24 02          | mov [esp+2], eax
0D1: 66 A1 00 00 00 00    | mov ax, [pursuit_id]
0D7: 86 C4                | xchg al, ah
0D9: 66 89 44 24 06       | mov [esp+6], ax
0DE: 66 A1 00 00 00 00    | mov ax, [step_id]
0E4: 86 C4                | xchg al, ah
0E6: 66 89 44 24 08       | mov [esp+8], ax
0EB: C6 44 24 0A 00       | mov byte [esp+10], 0
0F0: 8D 1C 24             | lea ebx, [esp]
0F3: 6A 0A                | push 10
0F5: 53                   | push ebx
0F6: 8B 0D 00 00 00 00    | mov ecx, [communications_manager]
0FC: E8 00 00 00 00       | call net_submit_client_packet
101: 83 C4 0C             | add esp, 12
104: 68 30 0A 00 00       | push 0x00000A30
109: 8D 04 24             | lea eax, [esp]
10C: 6A 02                | push 2
10E: 50                   | push eax
10F: 8B 0D 00 00 00 00    | mov ecx, [communications_manager]
115: 8B 49 74             | mov ecx, [ecx+0x74]
118: E8 00 00 00 00       | call net_post_decoded_server_packet_event
11D: 83 C4 04             | add esp, 4
120: EB 07                | jmp 0x129
122: C6 05 00 00 00 00 00 | mov byte [pending], 0
129: 89 F0                | mov eax, esi
12B: 5F                   | pop edi
12C: 5E                   | pop esi
12D: 5B                   | pop ebx
12E: 5D                   | pop ebp
12F: C2 04 00             | ret 4
```

The outbound builder reserves 12 stack bytes and writes a separate zero at body offset 10 because the native submitter reads `body[length]` while constructing this packet class. The submitted plaintext length remains exactly 10. The later `push 0x00000A30` provides decoded bytes `30 0A` plus safe padding for the simulated inbound copy.

## Stub relocations

For an `abs32` operand, write the target runtime address directly. For a `rel32` operand at offset `O`, write `target - (stub + O + 4)`.

| Operand offsets | Kind | Target |
|---|---|---|
| `0x002`, `0x045`, `0x051`, `0x05D`, `0x092`, `0x0B1`, `0x124` | `abs32` | `stub + 0x140` (`pending`) |
| `0x00E`, `0x0BE` | `abs32` | `stub + 0x141` (`target_type`) |
| `0x019`, `0x0C7` | `abs32` | `stub + 0x144` (`target_id`) |
| `0x026`, `0x0D3` | `abs32` | `stub + 0x148` (`pursuit_id`) |
| `0x033`, `0x0E0` | `abs32` | `stub + 0x14A` (`step_id`) |
| `0x03F`, `0x0A4` | `abs32` | `stub + 0x14C` (`armed_at_ms`) |
| `0x039`, `0x09E` | `rel32` | `module_base + 0x0021FEC4` |
| `0x04B` | `rel32` | `module_base + 0x0012C020` |
| `0x057` | `rel32` | `module_base + 0x0013DA90` |
| `0x063` | `rel32` | `module_base + 0x0012C950` |
| `0x082` | `rel32` | `module_base + 0x000670F0` |
| `0x0F8`, `0x111` | `abs32` | `module_base + 0x0033D958` |
| `0x0FD` | `rel32` | `module_base + 0x00163E00` |
| `0x119` | `rel32` | `module_base + 0x00067060` |

## Installation and removal

Use the [safe launcher](safe-launcher.md). Before writing anything, require the exact version-741 fingerprint and verify all eight original byte sequences. Start the process suspended, allocate the stub, apply every relocation, write the stub and zeroed state, then replace the calls. If any check or write fails, restore every changed call before resuming or terminate the suspended process.

Change page protection only for the exact ranges being written. Restore each original protection, flush the instruction cache for the stub and hook sites, and resume only after every step succeeds. Removal requires another suspended state, restoration of all verified original calls, an instruction-cache flush, and release of the stub allocation.

This is an in-memory patch. It must never rewrite `Darkages.exe`.

## Known limits

- The fallback covers the version-741 `NPC_Pursuit_MessageDialog` response-pending path. It is not a generic dialog-close hook.
- Escape is the fallback trigger. The pursuit Close button already reaches the patched native Close call and sends through the original sender.
- A fallback can be attempted once per pending response and only during the 30-second window.
- The synthetic `30 0A` repairs the client-side NPC session through normal dispatch. It does not prove that the server accepted the preceding `CPursuit` Close or cleared its own pursuit state.
- Runtime reproduction should confirm that an expired reactor accepts the cached Close and returns `30 0A` before this patch is enabled by default.
