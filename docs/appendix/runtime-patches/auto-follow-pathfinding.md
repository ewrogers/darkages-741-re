# Auto-follow pathfinding

This runtime patch turns Shift+double-right-click on a player or monster into follow-only mode. By default, the local character stops when the shortest known path is three tiles long. The client keeps checking the target every 100 ms, so walking starts again when the target moves farther away.

Normal double-right-click keeps the original follow-and-attack behavior. Shift+single-right-click keeps the original turn-or-step behavior.

The patch does not load a DLL. A launcher allocates one small block of memory in the suspended client, writes the code below, and redirects five instructions to it. This is still an in-memory code patch. There is no configuration-only way to add these options to version 741.

See [Pathfinding and following](../../systems/pathfinding-and-pursuit.md) for the normal client behavior.

## Behavior

The client normally blocks Shift pointer events from reaching players and monsters. It treats those objects as transparent and sends the click to the ground handler, where Shift+right-click means turn or step toward the cursor. This is why an earlier version of this patch only made the character face the target.

The new dispatcher hook admits one narrow extra case:

```c
if (shift &&
    event->type == 5 &&             /* double-right-click */
    (object->broad_category == 1 || /* human */
     object->broad_category == 2))  /* monster or Mundane */
{
    dispatch_to_object = true;
}
```

Ground items keep their native category-`8` exception. Every other Shift event follows the original filter.

Once the event reaches the living object, Shift is copied into its action message as bit `0x04`. The option selector uses that bit to choose a different set of follow options:

```c
shift_follow.distance = 3;
shift_follow.allow_attack = false;
```

The built-in breadth-first search still creates the route. An entity route ends on a tile beside the target, so:

```c
route_distance_to_target = remaining_steps + 1;
```

Before each move, the patch compares that distance with the requested stop distance. When it is close enough, it clears only the current route. It does not cancel the pending 100 ms target check.

```c
if (route_distance_to_target <= follow.distance) {
    ui_world_pane_reset_movement_state(world, 1);
    return;
}
```

Argument `1` is important. It keeps the pursuit run number valid, allowing the next timer check to find the target again. Ordinary movement input and map changes still use the full reset with argument `0`, so their existing cancellation behavior is unchanged.

The patch also wraps the pursuit-only `CAttack` call. When `allow_attack` is false, that call returns without sending a packet. The client may still turn to face an adjacent target.

The stop distance is the length of the current shortest route, not straight-line distance. A wall therefore counts as part of the trip around it. The patch does not back away if the target walks closer than the requested distance.

## Hook sites

The preferred image base is `0x00400000`. File offsets are reference information only. A launcher uses the loaded module base plus the RVA.

| Purpose | Static address | RVA | File offset | Verified original bytes | Stub entry |
|---|---:|---:|---:|---|---:|
| Admit Shift double-right-click for living objects | `0x005D48E5` | `0x001D48E5` | `0x001D3CE5` | `0F B6 4D C3 85 C9 0F 85 BA 00 00 00` | `stub + 0x1B0` |
| Select Shift follow at the living-object call | `0x005EF33A` | `0x001EF33A` | `0x001EE73A` | `E8 31 57 00 00` | `stub + 0x000` |
| Stop consuming a route at the requested distance | `0x005F49E5` | `0x001F49E5` | `0x001F3DE5` | `8B 45 E0 83 B8 B8 02 00 00 00` | `stub + 0x0A8` |
| Record the run number after the pursuit reset | `0x005F4AA2` | `0x001F4AA2` | `0x001F3EA2` | `83 7D 08 00 75 05` | `stub + 0x072` |
| Filter the pursuit-only attack call | `0x005F4D0E` | `0x001F4D0E` | `0x001F410E` | `E8 9D F7 FF FF` | `stub + 0x044` |

The two call replacements are:

```diff
- E8 <verified original rel32>
+ E8 00 00 00 00
```

For each call, write:

```text
rel32 = stub_entry - (module_base + site_rva + 5)
```

The three jump replacements are:

```diff
# 0x005D48E5
- 0F B6 4D C3 85 C9 0F 85 BA 00 00 00
+ E9 00 00 00 00 90 90 90 90 90 90 90

# 0x005F49E5
- 8B 45 E0 83 B8 B8 02 00 00 00
+ E9 00 00 00 00 90 90 90 90 90

# 0x005F4AA2
- 83 7D 08 00 75 05
+ E9 00 00 00 00 90
```

Use the same `rel32` formula with the matching stub entry. The extra `90` bytes keep every replacement the same size as the complete instructions it replaces.

## Injected stub template

Allocate and write at least `0x1E0` bytes. The follow code occupies `stub + 0x000` through `stub + 0x18B`, state begins at `stub + 0x190`, the Shift dispatcher entry occupies `stub + 0x1B0` through `stub + 0x1D3`, and the generation branch trampoline ends at `stub + 0x1DF`.

All zeroed `abs32` and external `rel32` operands below are relocation placeholders. Local branches are already complete.

```text
000: 8B 45 0C                   | mov eax,[ebp+0x0C]             ; living-object message
003: F6 40 2C 04                | test byte [eax+0x2C],0x04     ; Shift?
007: 74 2F                      | je normal_click
009: 89 0D 00 00 00 00          | mov [state.world],ecx
00F: 8B 44 24 04                | mov eax,[esp+0x04]            ; target ID
013: A3 00 00 00 00             | mov [state.target_id],eax
018: A1 00 00 00 00             | mov eax,[state.shift_distance]
01D: A3 00 00 00 00             | mov [state.active_distance],eax
022: A0 00 00 00 00             | mov al,[state.shift_allow_attack]
027: A2 00 00 00 00             | mov [state.allow_attack],al
02C: C6 05 00 00 00 00 01       | mov byte [state.active],1
033: E9 00 00 00 00             | jmp native_pursuit

038: C6 05 00 00 00 00 00       | normal_click: mov byte [state.active],0
03F: E9 00 00 00 00             | jmp native_pursuit

044: 80 3D 00 00 00 00 00       | cmp byte [state.active],0
04B: 74 20                      | je native_attack
04D: 39 0D 00 00 00 00          | cmp [state.world],ecx
053: 75 18                      | jne native_attack
055: 8B 81 C8 02 00 00          | mov eax,[ecx+0x2C8]
05B: 3B 05 00 00 00 00          | cmp eax,[state.tick_generation]
061: 75 0A                      | jne native_attack
063: 80 3D 00 00 00 00 00       | cmp byte [state.allow_attack],0
06A: 75 01                      | jne native_attack
06C: C3                         | ret                            ; suppress CAttack
06D: E9 00 00 00 00             | native_attack: jmp net_send_attack

072: 80 3D 00 00 00 00 00       | cmp byte [state.active],0
079: 74 24                      | je generation_replay
07B: 8B 45 B4                   | mov eax,[ebp-0x4C]            ; WorldPane
07E: 3B 05 00 00 00 00          | cmp eax,[state.world]
084: 75 19                      | jne generation_replay
086: 8B 45 08                   | mov eax,[ebp+0x08]            ; target ID
089: 3B 05 00 00 00 00          | cmp eax,[state.target_id]
08F: 75 0E                      | jne generation_replay
091: 8B 45 B4                   | mov eax,[ebp-0x4C]
094: 8B 80 C8 02 00 00          | mov eax,[eax+0x2C8]
09A: A3 00 00 00 00             | mov [state.tick_generation],eax
09F: 83 7D 08 00                | generation_replay: cmp dword [ebp+0x08],0
0A3: E9 2C 01 00 00             | jmp generation_flag_trampoline

0A8: 80 3D 00 00 00 00 00       | cmp byte [state.active],0
0AF: 74 5E                      | je advance_replay
0B1: 8B 45 E0                   | mov eax,[ebp-0x20]            ; WorldPane
0B4: 3B 05 00 00 00 00          | cmp eax,[state.world]
0BA: 75 53                      | jne advance_replay
0BC: 8B 90 C8 02 00 00          | mov edx,[eax+0x2C8]
0C2: 3B 15 00 00 00 00          | cmp edx,[state.tick_generation]
0C8: 74 19                      | je generation_valid           ; before timer schedule
0CA: 8B 0D 00 00 00 00          | mov ecx,[state.tick_generation]
0D0: 41                         | inc ecx
0D1: 39 CA                      | cmp edx,ecx
0D3: 75 3A                      | jne advance_replay
0D5: 8B 0D 00 00 00 00          | mov ecx,[state.target_id]
0DB: 39 88 BC 02 00 00          | cmp [eax+0x2BC],ecx
0E1: 75 2C                      | jne advance_replay
0E3: 8B 90 B8 02 00 00          | generation_valid: mov edx,[eax+0x2B8]
0E9: 83 C2 01                   | add edx,1                     ; route distance
0EC: 8B 0D 00 00 00 00          | mov ecx,[state.active_distance]
0F2: 83 F9 01                   | cmp ecx,1
0F5: 7D 05                      | jge distance_valid
0F7: B9 01 00 00 00             | mov ecx,1
0FC: 39 CA                      | distance_valid: cmp edx,ecx
0FE: 7F 0F                      | jg advance_replay
100: 6A 01                      | push 1                        ; clear route, keep timer
102: 8B 4D E0                   | mov ecx,[ebp-0x20]
105: E8 00 00 00 00             | call reset_movement
10A: E9 00 00 00 00             | jmp native_advance_epilogue
10F: 8B 45 E0                   | advance_replay: mov eax,[ebp-0x20]
112: 83 B8 B8 02 00 00 00       | cmp dword [eax+0x2B8],0
119: E9 00 00 00 00             | jmp native_advance_continue

11E: 55                         | auto_follow_start: push ebp
11F: 89 E5                      | mov ebp,esp
121: 8B 4D 08                   | mov ecx,[ebp+0x08]            ; WorldPane
124: 89 0D 00 00 00 00          | mov [state.world],ecx
12A: 8B 45 0C                   | mov eax,[ebp+0x0C]            ; target ID
12D: A3 00 00 00 00             | mov [state.target_id],eax
132: 8B 55 10                   | mov edx,[ebp+0x10]            ; distance
135: 83 FA 01                   | cmp edx,1
138: 7D 05                      | jge start_min_ok
13A: BA 01 00 00 00             | mov edx,1
13F: 81 FA FF 00 00 00          | start_min_ok: cmp edx,255
145: 7E 05                      | jle start_distance_ok
147: BA FF 00 00 00             | mov edx,255
14C: 89 15 00 00 00 00          | start_distance_ok: mov [state.active_distance],edx
152: 8B 45 14                   | mov eax,[ebp+0x14]            ; allow attack
155: 85 C0                      | test eax,eax
157: 0F 95 C0                   | setne al
15A: A2 00 00 00 00             | mov [state.allow_attack],al
15F: C6 05 00 00 00 00 01       | mov byte [state.active],1
166: FF 75 0C                   | push dword [ebp+0x0C]
169: 8B 4D 08                   | mov ecx,[ebp+0x08]
16C: E8 00 00 00 00             | call native_pursuit
171: 89 EC                      | mov esp,ebp
173: 5D                         | pop ebp
174: C2 10 00                   | ret 16

177: C6 05 00 00 00 00 00       | auto_follow_cancel: mov byte [state.active],0
17E: 8B 4C 24 04                | mov ecx,[esp+0x04]            ; WorldPane
182: 6A 00                      | push 0
184: E8 00 00 00 00             | call reset_movement
189: C2 04 00                   | ret 4

18C: 00 00 00 00                | alignment padding
190: 00 00 00 00                | state.world
194: 00 00 00 00                | state.target_id
198: 00 00 00 00                | state.tick_generation
19C: 03 00 00 00                | state.active_distance
1A0: 03 00 00 00                | state.shift_distance
1A4: 00                         | state.active
1A5: 00                         | state.allow_attack
1A6: 00                         | state.shift_allow_attack
1A7: 00                         | padding
1A8: 00 00 00 00 00 00 00 00    | padding

1B0: 80 7D C3 00                | cmp byte [ebp-0x3D],0          ; native Shift flag
1B4: 74 19                      | je dispatch_living
1B6: 8B 45 0C                   | mov eax,[ebp+0x0C]             ; pointer event
1B9: 80 78 0C 05                | cmp byte [eax+0x0C],5          ; double-right-click?
1BD: 75 0B                      | jne skip_object
1BF: 8B 45 A0                   | mov eax,[ebp-0x60]             ; broad category
1C2: 83 E8 01                   | sub eax,1
1C5: 83 F8 01                   | cmp eax,1                      ; category 1 or 2?
1C8: 76 05                      | jbe dispatch_living
1CA: E9 00 00 00 00             | skip_object: jmp native_skip_object
1CF: E9 00 00 00 00             | dispatch_living: jmp native_dispatch_object

1D4: 75 05                      | generation_flag_trampoline: jne target_nonzero
1D6: E9 00 00 00 00             | jmp native_target_zero
1DB: E9 00 00 00 00             | target_nonzero: jmp native_target_nonzero
```

The generation hook replaces both the native compare at `0x005F4AA2` and its conditional jump at `0x005F4AA6`. The latter address is therefore inside the six patched bytes and is not a valid continuation. The local jump from `stub + 0x0A3` preserves the flags produced by the replayed compare. The trampoline then sends a zero target ID to untouched address `0x005F4AA8`, or a nonzero target ID to untouched address `0x005F4AAD`.

## Stub relocations

For an `abs32` operand, write the target runtime address directly. For a `rel32` operand at offset `O`, write:

```text
rel32 = target - (stub + O + 4)
```

| Operand offsets | Kind | Target |
|---|---|---|
| `0x00B`, `0x04F`, `0x080`, `0x0B6`, `0x126` | `abs32` | `stub + 0x190` (`state.world`) |
| `0x014`, `0x08B`, `0x0D7`, `0x12E` | `abs32` | `stub + 0x194` (`state.target_id`) |
| `0x05D`, `0x09B`, `0x0C4`, `0x0CC` | `abs32` | `stub + 0x198` (`state.tick_generation`) |
| `0x01E`, `0x0EE`, `0x14E` | `abs32` | `stub + 0x19C` (`state.active_distance`) |
| `0x019` | `abs32` | `stub + 0x1A0` (`state.shift_distance`) |
| `0x02E`, `0x03A`, `0x046`, `0x074`, `0x0AA`, `0x161`, `0x179` | `abs32` | `stub + 0x1A4` (`state.active`) |
| `0x028`, `0x065`, `0x15B` | `abs32` | `stub + 0x1A5` (`state.allow_attack`) |
| `0x023` | `abs32` | `stub + 0x1A6` (`state.shift_allow_attack`) |
| `0x034`, `0x040`, `0x16D` | `rel32` | `module_base + 0x001F4A70` (`ui_world_pane_pursue_and_auto_attack_target`) |
| `0x06E` | `rel32` | `module_base + 0x001F44B0` (`net_send_attack`) |
| `0x106`, `0x185` | `rel32` | `module_base + 0x001F4900` (`ui_world_pane_reset_movement_state`) |
| `0x10B` | `rel32` | `module_base + 0x001F4A5B` (queued-step epilogue) |
| `0x11A` | `rel32` | `module_base + 0x001F49EF` (queued-step continuation) |
| `0x1CB` | `rel32` | `module_base + 0x001D49AB` (native skip-object path) |
| `0x1D0` | `rel32` | `module_base + 0x001D48F1` (native object-dispatch path) |
| `0x1D7` | `rel32` | `module_base + 0x001F4AA8` (native zero-target path) |
| `0x1DC` | `rel32` | `module_base + 0x001F4AAD` (native nonzero-target path) |

## Options and manual entry points

The default Shift gesture reads these two values:

| Option | Address | Default | Meaning |
|---|---:|---:|---|
| Shift stop distance | `stub + 0x1A0` | `3` | Stop when the current shortest route is this many tiles long. Valid range is `1` through `255`. |
| Shift allow attack | `stub + 0x1A6` | `0` | Zero blocks the pursuit-only attack. Nonzero allows the native attack when adjacent. |

Another main-thread patch can start a follow directly through `stub + 0x11E`:

```c
void __stdcall auto_follow_start(
    WorldPane *world,
    u32 target_id,
    s32 stop_distance,
    bool allow_attack);
```

The wrapper clamps `stop_distance` to `1..255`, saves the options, and calls the native pursuit function. It must run on the game thread.

`stub + 0x177` provides an explicit manual stop:

```c
void __stdcall auto_follow_cancel(WorldPane *world);
```

An external process must not call either entry through a remote worker thread. Supporting arbitrary external target IDs would also need a small command slot drained from a game-thread hook. That queue is outside this patch. Shift+double-right-click is the included no-DLL trigger.

## Installation and removal

Use the [safe launcher](safe-launcher.md). Require the exact version-741 fingerprint and verify all five original byte sequences before writing.

1. Start the process suspended.
2. Allocate at least `0x1E0` readable, writable, and executable bytes.
3. Copy the stub template and apply every relocation.
4. Write the five hook replacements.
5. Restore page protections and flush the instruction cache for the stub and hook sites.
6. Resume only after every check and write succeeds.

If any step fails, restore all changed hook bytes before resuming or terminate the suspended process. Removal restores the five original byte ranges, flushes the instruction cache, and releases the stub allocation.

Never rewrite `Darkages.exe`.

## Test checklist

- Test normal double-right-click first. It must still walk beside a living target and attack; this reaches the generation hook immediately and catches an invalid continuation before testing the new mode.
- Shift+double-right-click follows but sends no `CAttack`.
- Shift+single-right-click still turns or steps toward the cursor.
- Shift pointer input on ground items keeps its native behavior.
- The default route stops at a shortest-path distance of three tiles.
- Moving the target farther away restarts walking on a later 100 ms check.
- A closer target does not make the local character back away.
- Keyboard movement, ground clicks, Space, map changes, and position resets still cancel the follow.
- A blocked or missing target follows the native retry and stop rules.
- Opening and closing doors changes the next route in the same way as native pursuit.

## Known limits

- The hook sites, bytes, stack state, and native continuations are statically verified against the matching client. The complete patch still needs in-game runtime testing before it should be enabled by default.
- This avoids DLL loading, but it still places executable code in the client process.
- The stop rule is route distance. It is not a circle drawn around the target.
- The patch follows but does not hold an exact formation. It never moves away from a target that comes too close.
- Manual entry points are safe only from the game thread.
