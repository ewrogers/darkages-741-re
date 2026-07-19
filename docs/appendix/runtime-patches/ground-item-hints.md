# Ground item hints

This launcher patch replays visible ground items as translucent hints after the complete world pane has finished drawing. Walls, foliage, pillars, lighting, players, monsters, and effects keep their ordinary render paths. Holding either Alt key enables the extra item pass. Releasing Alt removes it immediately.

The working implementation uses launcher-allocated state and four executable stubs. It does not inject a DLL or modify the executable on disk.

## Resulting frame flow

The implementation separates collection from replay:

```text
render_world_pane_content wrapper
    -> save WorldPane and clear captured-item count
    -> original world-pane draw
        -> render_collect_world_objects wrapper
            -> original queue construction and draw
            -> copy eligible layer-4 item entries to bounded state
    -> test native EventMan Alt modifier
    -> replay captured items with blend mode 3
    -> return the original world-pane result
```

The final pass is intentionally simple. It does not calculate which item pixels are behind a static sprite. Instead, it replays every eligible visible item while Alt is held. An already visible item receives the same translucent hint as an occluded one.

## Allocated state

The launcher allocates a zeroed `0xCF4`-byte state block:

```c
struct GroundItemHintState {
    u32 count;                         // +0x000
    RenderContext *render_context;     // +0x004
    Canvas *canvas;                    // +0x008
    byte reserved[0x1C];
    WorldPane *world_pane;             // +0x028
    byte reserved_to_entries[0xD4];
    WorldDrawEntry entries[255];    // +0x100
};

struct WorldDrawEntry {
    WorldObject *object;
    s32 screen_x;
    s32 screen_y;
};
```

The fixed capacity prevents a damaged or unexpectedly large queue from overrunning launcher state. Additional items after entry 255 are ignored for that frame.

## Collect eligible items

The collector hook wraps `render_collect_world_objects`. It calls the original function first, preserves its result, then walks the completed layer-4 vector at render-context offsets `0xE0` through `0xE4`.

An entry is copied only when:

- its object pointer is non-null;
- its primary vtable is exactly `module_base + 0x0028B1AC`, the `WorldObject_Item` vtable;
- `WorldObject_Item + 0xB0` is ordinary blend mode `1`; and
- the capture count is below 255.

The wrapper copies the existing 12-byte draw entry and records the render context and canvas. It does not retain a new object reference, allocate memory, or call outside the client.

## Replay after the completed pane

The frame hook wraps `render_world_pane_content`. Before the original call it saves the live `WorldPane *this` pointer and resets the capture count. The nested collector hook repopulates the state while the original world draw runs.

After the original returns, the wrapper reads EventMan modifier byte `+0x434`. Bit `0x01` represents either Alt key. If the bit is clear, the wrapper returns without replaying anything.

For each captured entry, it revalidates the object pointer, exact item vtable, and ordinary blend mode. It then:

```c
old_mode = item->blend_mode;       // WorldObject_Item + 0xB0
item->blend_mode = 3;

render_world_object(
    render_context,
    canvas,
    entry,
    render_context->category_state + item->broad_category
);

item->blend_mode = old_mode;
```

This temporary write is why the working patch does not need to change `render_item_object` at `0x005DE7E4`. That function's final body blit reloads `WorldObject_Item + 0xB0`, so setting the field to `3` makes the existing code take the desired faded path. The original value is restored immediately after each draw.

## Redraw exactly on Alt transitions

The world pane is cached. Without invalidation, the visual change can wait for mouse movement or another dirty event.

The launcher hooks `input_emit_key_down` and `input_emit_key_up`, calls each original function first, then tests the raw scan code:

| Scan code | Key |
| --- | --- |
| `0x38` | left Alt |
| `0xB8` | right Alt |

For either code, the wrapper loads the last saved `WorldPane *` and calls `ui_pane_invalidate(pane, NULL)`. Separate key-down and key-up hooks make the hint appear and disappear without depending on later world input propagation.

Enabling this option also enables the [stuck-modifier cleanup](stuck-modifiers.md), so a lost Alt key-up during a focus change cannot leave the overlay active.

## Hook sites

| Hook | Static address | RVA | File offset, reference only | Continuation |
| --- | --- | --- | --- | --- |
| `input_emit_key_down` | `0x00467C10` | `0x00067C10` | `0x00067010` | `0x00467C15` |
| `input_emit_key_up` | `0x00467E30` | `0x00067E30` | `0x00067230` | `0x00467E35` |
| `render_world_pane_content` | `0x005CE280` | `0x001CE280` | `0x001CD680` | `0x005CE286` |
| `render_collect_world_objects` | `0x005D3740` | `0x001D3740` | `0x001D2B40` | `0x005D3745` |

The key-down, key-up, and item-collector entries use the same five-byte prologue change:

```diff
- 000: 55             | push ebp       ; displaced function prologue
- 001: 8B EC          | mov ebp, esp
- 003: 6A FF          | push -1
+ 000: E9 <stub rel32> | jmp hook_stub  ; enter the matching relocated wrapper
```

The completed-frame entry displaces six bytes:

```diff
- 000: 55             | push ebp       ; displaced frame-draw prologue
- 001: 8B EC          | mov ebp, esp
- 003: 83 EC 1C       | sub esp, 0x1C
+ 000: E9 <stub rel32> | jmp frame_stub ; replay items after the normal frame
+ 005: 90             | nop            ; fill the sixth displaced byte
```

Every stub contains a local trampoline that executes the complete displaced prologue and jumps to the listed continuation.

The implementation emits stubs of these fixed sizes:

| Stub | Size |
| --- | ---: |
| collector | 157 bytes |
| completed-frame replay | 186 bytes |
| key down | 84 bytes |
| key up | 84 bytes |

Stub builders resolve the actual module base, allocated state address, allocated stub address, helper calls, vtable address, and return displacement. Static Binary Ninja addresses are never treated as fixed runtime pointers.

## Annotated injected stubs

The listings below are the fixed templates before relocation. Placeholder operands are named in comments instead of being presented as usable addresses. A builder must resolve every placeholder and then verify the completed bytes before installing a hook.

### Item collector

This wrapper preserves the normal collection call, then copies up to 255 visible ground-item draw records into patch-owned state.

```text
000: 55                         | push ebp                  ; start the wrapper frame
001: 89 E5                      | mov ebp, esp              ; establish stack arguments
003: 83 EC 08                   | sub esp, 8                ; reserve saved-result locals
006: 53                         | push ebx                  ; preserve caller registers
007: 56                         | push esi
008: 57                         | push edi
009: 89 CE                      | mov esi, ecx              ; keep the render-list owner
00B: FF 75 18                   | push dword ptr [ebp+0x18] ; forward original argument 5
00E: FF 75 14                   | push dword ptr [ebp+0x14] ; forward original argument 4
011: FF 75 10                   | push dword ptr [ebp+0x10] ; forward original argument 3
014: FF 75 0C                   | push dword ptr [ebp+0x0C] ; forward original argument 2
017: FF 75 08                   | push dword ptr [ebp+0x08] ; forward original argument 1
01A: 89 F1                      | mov ecx, esi              ; restore the original this pointer
01C: E8 72 00 00 00             | call original_collector   ; run displaced prologue through the local gateway
021: 89 45 FC                   | mov [ebp-4], eax          ; preserve the original result
024: 8B BE E0 00 00 00          | mov edi, [esi+0xE0]       ; first collected draw record
scan_records:
02A: 3B BE E4 00 00 00          | cmp edi, [esi+0xE4]       ; reached the end of the records?
030: 73 55                      | jae collector_done        ; stop scanning
032: 8B 17                      | mov edx, [edi]            ; load the world object
034: 85 D2                      | test edx, edx              ; ignore an empty record
036: 74 4A                      | je next_record
038: 81 3A 78 56 34 12          | cmp [edx], item_vtable    ; require the verified item class
03E: 75 42                      | jne next_record
040: 83 BA B0 00 00 00 01       | cmp dword ptr [edx+0xB0], 1 ; require normal blend mode
047: 75 39                      | jne next_record
049: A1 00 10 11 11             | mov eax, [state.count]    ; current saved-record count
04E: 3D FF 00 00 00             | cmp eax, 255              ; enforce the fixed state capacity
053: 73 32                      | jae collector_done
055: 6B D8 0C                   | imul ebx, eax, 12          ; locate one three-dword record
058: 81 C3 00 11 11 11          | add ebx, state.entries    ; resolve its destination
05E: 8B 0F                      | mov ecx, [edi]            ; copy object pointer
060: 89 0B                      | mov [ebx], ecx
062: 8B 4F 04                   | mov ecx, [edi+4]          ; copy first draw value
065: 89 4B 04                   | mov [ebx+4], ecx
068: 8B 4F 08                   | mov ecx, [edi+8]          ; copy second draw value
06B: 89 4B 08                   | mov [ebx+8], ecx
06E: FF 05 00 10 11 11          | inc dword ptr [state.count] ; publish the saved record
074: 89 35 04 10 11 11          | mov [state.render_context], esi ; save context for frame replay
07A: 8B 45 08                   | mov eax, [ebp+8]          ; load the current canvas argument
07D: A3 08 10 11 11             | mov [state.canvas], eax   ; save canvas for frame replay
next_record:
082: 83 C7 0C                   | add edi, 12               ; advance to the next draw record
085: EB A3                      | jmp scan_records
collector_done:
087: 8B 45 FC                   | mov eax, [ebp-4]          ; restore the original result
08A: 5F                         | pop edi                   ; restore caller registers
08B: 5E                         | pop esi
08C: 5B                         | pop ebx
08D: 89 EC                      | mov esp, ebp
08F: 5D                         | pop ebp
090: C2 14 00                   | ret 0x14                  ; preserve original stack cleanup
original_collector:
093: 55                         | push ebp                  ; replay displaced prologue
094: 89 E5                      | mov ebp, esp
096: 6A FF                      | push -1
098: E9 63 FF FF 11             | jmp collector_continuation ; return to the client after the hook
```

### Completed-frame replay

This wrapper performs the normal world-pane draw first. While Alt is down, it replays saved items with translucent blend mode and restores each object immediately afterward.

```text
000: 55                         | push ebp                  ; start the wrapper frame
001: 89 E5                      | mov ebp, esp
003: 83 EC 10                   | sub esp, 0x10             ; reserve saved-result and blend locals
006: 53                         | push ebx                  ; preserve caller registers
007: 56                         | push esi
008: 57                         | push edi
009: 89 CE                      | mov esi, ecx              ; keep the world pane
00B: 89 35 28 10 11 11          | mov [state.world_pane], esi ; save pane for key-triggered invalidation
011: C7 05 00 10 11 11 00 00 00 00 | mov dword ptr [state.count], 0 ; begin a fresh frame
01B: 89 F1                      | mov ecx, esi              ; restore the original this pointer
01D: E8 8D 00 00 00             | call original_frame_draw ; run the normal frame through the local gateway
022: 89 45 FC                   | mov [ebp-4], eax          ; preserve the original result
025: E8 D6 FF FF EF             | call input_get_event_manager ; read live modifier state
02A: 85 C0                      | test eax, eax              ; no input manager means no hint
02C: 74 77                      | je replay_done
02E: F6 80 34 04 00 00 01       | test byte ptr [eax+0x434], 1 ; is either Alt key down?
035: 74 6E                      | je replay_done
037: 31 FF                      | xor edi, edi              ; start at saved record zero
replay_loop:
039: 3B 3D 00 10 11 11          | cmp edi, [state.count]    ; replay every saved item
03F: 73 64                      | jae replay_done
041: 6B C7 0C                   | imul eax, edi, 12          ; locate the saved record
044: 8D 98 00 11 11 11          | lea ebx, [eax+state.entries]
04A: 8B 13                      | mov edx, [ebx]            ; load the item object
04C: 85 D2                      | test edx, edx              ; skip stale empty records
04E: 74 52                      | je next_replay
050: 81 3A 78 56 34 12          | cmp [edx], item_vtable    ; recheck object type before use
056: 75 4A                      | jne next_replay
058: 83 BA B0 00 00 00 01       | cmp dword ptr [edx+0xB0], 1 ; recheck expected blend state
05F: 75 41                      | jne next_replay
061: 89 55 F4                   | mov [ebp-0x0C], edx       ; save object across the renderer call
064: 8B 82 B0 00 00 00          | mov eax, [edx+0xB0]       ; save original blend mode
06A: 89 45 F8                   | mov [ebp-8], eax
06D: C7 82 B0 00 00 00 03 00 00 00 | mov dword ptr [edx+0xB0], 3 ; render this replay translucently
077: 8B 0D 04 10 11 11          | mov ecx, [state.render_context] ; recover frame render state
07D: 8B 81 BC 02 00 00          | mov eax, [ecx+0x2BC]      ; load category-state table
083: 8B 55 F4                   | mov edx, [ebp-0x0C]       ; recover the item object
086: 03 42 2C                   | add eax, [edx+0x2C]       ; select its broad render category
089: 50                         | push eax                  ; pass category state
08A: 53                         | push ebx                  ; pass saved draw record
08B: FF 35 08 10 11 11          | push dword ptr [state.canvas] ; pass current canvas
091: E8 6A FF FF F0             | call render_world_object  ; draw one hint copy
096: 8B 55 F4                   | mov edx, [ebp-0x0C]       ; recover the item object
099: 8B 45 F8                   | mov eax, [ebp-8]          ; recover original blend mode
09C: 89 82 B0 00 00 00          | mov [edx+0xB0], eax       ; restore object state immediately
next_replay:
0A2: 47                         | inc edi                   ; advance to the next saved item
0A3: EB 94                      | jmp replay_loop
replay_done:
0A5: 8B 45 FC                   | mov eax, [ebp-4]          ; restore the original frame result
0A8: 5F                         | pop edi                   ; restore caller registers
0A9: 5E                         | pop esi
0AA: 5B                         | pop ebx
0AB: 89 EC                      | mov esp, ebp
0AD: 5D                         | pop ebp
0AE: C3                         | ret                       ; preserve original return convention
original_frame_draw:
0AF: 55                         | push ebp                  ; replay displaced prologue
0B0: 89 E5                      | mov ebp, esp
0B2: 83 EC 1C                   | sub esp, 0x1C
0B5: E9 46 FF FF F1             | jmp frame_continuation    ; return to the client after the hook
```

### Alt key wrappers

Key down and key up use the same template. Only the original-function continuation and the relocated invalidation call differ.

```text
000: 55                         | push ebp                  ; start the wrapper frame
001: 89 E5                      | mov ebp, esp
003: 83 EC 08                   | sub esp, 8                ; reserve saved-result locals
006: 56                         | push esi                  ; preserve the pane owner
007: 89 CE                      | mov esi, ecx              ; keep the original this pointer
009: FF 75 14                   | push dword ptr [ebp+0x14] ; forward original argument 4
00C: FF 75 10                   | push dword ptr [ebp+0x10] ; forward original argument 3
00F: FF 75 0C                   | push dword ptr [ebp+0x0C] ; forward original argument 2
012: FF 75 08                   | push dword ptr [ebp+0x08] ; forward raw scan code
015: 89 F1                      | mov ecx, esi              ; restore the original this pointer
017: E8 2E 00 00 00             | call original_key_event  ; preserve normal client input behavior
01C: 89 45 FC                   | mov [ebp-4], eax          ; preserve the original result
01F: 0F B6 45 08                | movzx eax, byte ptr [ebp+8] ; load raw scan code
023: 83 F8 38                   | cmp eax, 0x38             ; left Alt?
026: 74 07                      | je invalidate_world
028: 3D B8 00 00 00             | cmp eax, 0xB8             ; right Alt?
02D: 75 11                      | jne key_done
invalidate_world:
02F: 8B 0D 28 10 11 11          | mov ecx, [state.world_pane] ; use the last completed world pane
035: 85 C9                      | test ecx, ecx              ; skip before the first frame
037: 74 07                      | je key_done
039: 6A 00                      | push 0                    ; no explicit dirty rectangle
03B: E8 C0 FF FF E2             | call ui_pane_invalidate   ; redraw exactly on the Alt transition
key_done:
040: 8B 45 FC                   | mov eax, [ebp-4]          ; restore the original input result
043: 5E                         | pop esi                   ; restore caller state
044: 89 EC                      | mov esp, ebp
046: 5D                         | pop ebp
047: C2 10 00                   | ret 0x10                  ; preserve original stack cleanup
original_key_event:
04A: 55                         | push ebp                  ; replay displaced prologue
04B: 89 E5                      | mov ebp, esp
04D: 6A FF                      | push -1
04F: E9 AC FF FF E3             | jmp key_event_continuation ; return to the client after the hook
```

The key-down template uses `E8 C0 FF FF E2` at offset `0x03B`; the key-up template uses `E8 C0 FF FF E1`. Both encode `call ui_pane_invalidate`, and the builder replaces the four-byte displacement for the allocated stub address.

## Ordering and limits

The replay happens after the complete normal world-pane draw. This guarantees that static map art cannot hide the hint. It also means the hint is technically later than players, monsters, effects, and lighting.

The implementation has no static-rectangle intersection test, no player or monster overlap filter, and no blinded-state gate. The translucent mode keeps the result hint-like, but it is still a topmost item copy. This is the deliberate reliability tradeoff in the working implementation.

The native local-player replay remains separate. `render_replay_layer_zero_and_self` is not hooked, and the item renderer is not patched. Normal jungle-tree mode `0x6D` also remains unchanged.

## Preserve the static renderer

Before allocating anything, the launcher verifies the original 48-byte static mode selector at `0x005E487D`:

```text
000: 8B 55 D0                   | mov edx, [ebp-0x30]       ; load the current static object
003: 0F B6 82 B9 00 00 00       | movzx eax, byte ptr [edx+0xB9] ; read its SOTP render flags
00A: 25 80 00 00 00             | and eax, 0x80             ; test the full-hide flag
00F: 74 09                      | je test_partial_hide      ; leave mode unchanged when clear
011: C7 45 E8 6D 00 00 00       | mov dword ptr [ebp-0x18], 0x6D ; keep jungle-tree behavior
018: EB 16                      | jmp selector_done
test_partial_hide:
01A: 8B 4D D0                   | mov ecx, [ebp-0x30]       ; reload the current static object
01D: 0F B6 91 B9 00 00 00       | movzx edx, byte ptr [ecx+0xB9] ; read its SOTP render flags
024: 83 E2 40                   | and edx, 0x40             ; test the partial-hide flag
027: 74 07                      | je selector_done          ; leave mode unchanged when clear
029: C7 45 E8 03 00 00 00       | mov dword ptr [ebp-0x18], 3 ; use the native translucent mode
selector_done:
```

These bytes are verified but never replaced. This both rejects the earlier whole-static prototype and proves that SOTP flag `0x80`, flag `0x40`, and jungle-tree behavior are intact.

## Safe installation and rollback

Apply the patch while the matching client is suspended. Verify the executable fingerprint, four hook prologues, and static selector before writing. Allocate the state and four stubs, populate all relocations, make the stubs executable, verify their bytes, and flush the instruction cache. Then install and verify all four jumps.

On failure, restore written hooks in reverse order. Free a stub only after its hook is confirmed restored. Free shared state only after every hook is safe. Preserve cleanup failures alongside the original error and do not resume a partially patched client.

The implementation's targeted `GameClientServiceTests` cover the 255-entry bound, all resolved helper and continuation targets, both Alt scan codes, static-selector preservation, and five- versus six-byte jump construction.
