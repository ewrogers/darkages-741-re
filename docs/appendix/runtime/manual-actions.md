# Manual native actions

The client already has native action producers for spells, skills, inventory transfers, movement, and equipment. Calling these producers on the game thread avoids UI hit testing and does not require the matching lower-tray page to be visible.

These functions are not safe `CreateRemoteThread` entry points. Most are x86 `__thiscall` members that require a live object in `ECX`. All of them reach client state that is owned and mutated by the main game thread.

## Address and thread rules

These addresses apply only to the documented version 741 executable. Resolve every function as `loaded_module_base + RVA`.

| Function | Static address | RVA | Purpose |
| --- | ---: | ---: | --- |
| `ui_equip_pane_request_remove_slots_1_and_3` | `0x0045FDA0` | `0x0005FDA0` | Perform the tilde unequip action |
| `net_send_remove_equipment` | `0x00460330` | `0x00060330` | Remove one equipment slot |
| `event_dispatcher_tick` | `0x00464180` | `0x00064180` | Main-thread command-queue hook |
| `ui_inventory_activate_slot` | `0x00490960` | `0x00090960` | Use one item slot |
| `ui_equip_pane_get` | `0x00493620` | `0x00093620` | Get the live `EquipPane` |
| `ui_spell_delay_control_pane_get` | `0x00493630` | `0x00093630` | Get the casting controller |
| `net_send_drop` | `0x00496C90` | `0x00096C90` | Drop a live inventory item on a tile |
| `net_send_give` | `0x00496D90` | `0x00096D90` | Give a live inventory item to an object |
| `ui_skill_inventory_activate` | `0x004992F0` | `0x000992F0` | Use a live skill entry |
| `ui_spell_begin_target_selection` | `0x0049A4E0` | `0x0009A4E0` | Open the entity-target selector |
| `ui_spell_inventory_activate` | `0x0049A670` | `0x0009A670` | Activate a spell through its normal argument dispatcher |
| `ui_spell_open_string_input` | `0x0049A720` | `0x0009A720` | Open the free-text prompt |
| `ui_spell_open_number_inputs` | `0x0049A950` | `0x0009A950` | Open the fixed-count numeric prompt |
| `net_build_use_spell_target` | `0x0049AB60` | `0x0009AB60` | Start a spell with an explicit target |
| `ui_spell_is_denied` | `0x0049AC90` | `0x0009AC90` | Check the server-managed denied-spell list |
| `net_build_use_spell_no_args` | `0x0049AD40` | `0x0009AD40` | Lower-level no-argument spell builder |
| `ui_spell_text_input_submit` | `0x0049B190` | `0x0009B190` | Submit the active free-text prompt |
| `ui_spell_numeric_input_submit` | `0x0049B380` | `0x0009B380` | Submit the active numeric prompt |
| `ui_start_spell_cast` | `0x0049B900` | `0x0009B900` | Queue a completed `CUseSpell` body and start cast timing |
| `ui_cancel_spell_delay` | `0x0049BA50` | `0x0009BA50` | Cancel the pending local cast |
| `net_submit_client_packet` | `0x00563E00` | `0x00163E00` | Copy and queue a supplied opcode-first body |
| `ui_gui_back_get_inventory_item` | `0x005A2F90` | `0x001A2F90` | Resolve one live item entry through `GUIBackPane` |
| `ui_get_gui_back_pane` | `0x005A9C40` | `0x001A9C40` | Get the live lower-tray owner |
| `ui_world_pane_handle_direction_input` | `0x005F0C40` | `0x001F0C40` | Perform the normal turn-or-step direction action |

The injected proxy should compare `GetCurrentThreadId()` with the thread ID stored at RVA `0x00340400`. Resolve client objects again when each queued command runs. Do not retain pane, item, skill, spell, or world-object pointers across ticks.

Prefer the narrowest native producer that already accepts the supplied values. It preserves packet construction, client-side guards, and the normal queue handoff without replaying pointer input or dialog behavior. Submit a body directly through `net_submit_client_packet` only when the native producer is bound to UI state, as with the two gold amount dialogs. A direct wrapper must reproduce any useful validation that the skipped UI would have performed.

## Main-thread command queue

An external controller can submit a small command without using window messages:

```c
IPC thread:
    validate and copy command into a bounded queue

event_dispatcher_tick hook:
    drain a small command budget
    resolve current client roots
    validate the requested slot, target, and lifecycle
    call one native producer
    call the original event_dispatcher_tick
```

The IPC thread must never call these functions. It must also never wait for the game thread while holding a lock the hook needs. The wider queue and failure rules are in [Event proxy design](../../systems/event-proxy.md).

## Resolving the live entries

`ui_get_gui_back_pane()` returns null outside the lower-tray lifetime. Its children exist independently of which page is currently selected:

```c
GUIBackPane *gui = ui_get_gui_back_pane();

ItemInventoryPane *items =
    *(ItemInventoryPane **)((u8 *)gui + 0x4F88);

SkillSpellInventoryPane *books =
    *(SkillSpellInventoryPane **)((u8 *)gui + 0x4F8C);

NewSkillInventoryPane *skills =
    *(NewSkillInventoryPane **)((u8 *)books + 0x224);

NewSpellInventoryPane *spells =
    *(NewSpellInventoryPane **)((u8 *)books + 0x228);
```

The checked inventory accessor uses the `GUIBackPane_Interface` secondary base at complete-object offset `+0x190`:

```c
InvItemPane *item = ui_gui_back_get_inventory_item(
    (GUIBackPane_Interface *)((u8 *)gui + 0x190),
    slot);
```

It returns null unless the slot is in the inclusive range `1` through `60`.

The item pane has 60 direct pointers at `+0x1A0`. Each skill or spell pane has a capacity at `+0x190` and a pointer to its item array at `+0x194`. Validate `1 <= slot <= capacity`, require a non-null entry, and confirm that the entry's retained slot matches the requested slot.

The complete object layouts are in [Inventory and character panes](inventory-ui.md). The root lifetimes are in [Runtime state walking](state-walking.md).

## Use an item

Use the one-based item slot through:

```c
void __thiscall ui_inventory_activate_slot(
    ItemInventoryPane *inventory,
    u8 slot);
```

The caller must enforce `1 <= slot <= 60`. This function subtracts one and indexes `inventory + 0x1A0` without checking the range. It does check that the selected pointer is non-null, then reaches the normal denial-list check and `CUse` builder.

## Drop or give an inventory item

Resolve `InvItemPane *item = inventory->items[slot - 1]` at execution time. For an ordinary item, require slot `1` through `59`, a non-null pointer, and `item->slot == slot`. The complete item stores its one-based slot at `+0x214`, quantity at `+0x240`, and stackable flag at `+0x244`.

Use quantity `1` when the command omits a quantity. Reject zero. For a non-stackable item, require exactly `1`. For a stackable item, require `1 <= quantity <= item->quantity`.

To drop the item on a map tile, validate X and Y against the current map and call:

```c
u32 __thiscall net_send_drop(
    InvItemPane *item,
    u16 target_y,
    u16 target_x,
    u32 quantity);
```

The native argument order is Y followed by X. The packet body is still `opcode, slot, X, Y, quantity`. The function reads the slot from `item + 0x214`, builds [`CDrop`](../../network/client/008-0x08-drop.md), and enters the normal packet submission queue.

To give the item to another living object, reject the local character's own ID and call:

```c
u32 __thiscall net_send_give(
    InvItemPane *item,
    u32 object_id,
    u32 quantity);
```

This builds [`CGive`](../../network/client/041-0x29-give.md). The normal version 741 drag path always supplies quantity `1`, even for a stackable item. The builder and packet accept a full `u32` quantity, but server acceptance of a manually supplied larger quantity has not been exercised.

Both native builders preserve the client's local manufacture-mode guard. Their return value does not provide a reliable server outcome. Success or rejection arrives later as server traffic.

## Drop or give gold

Slot `60` selects gold in the UI, but gold packets do not contain a slot. `net_send_drop_gold` and `net_send_give_gold` are dialog-bound methods that read `_nmoney.txt` controls, so they are not useful when the amount and target are already supplied.

Build the opcode-first body in a bounded main-thread wrapper and call:

```c
u32 __thiscall net_submit_client_packet(
    Socket *socket,
    const u8 *body,
    s16 body_length);
```

Resolve `socket` from the pointer at RVA `0x0033D958` for the current invocation. The function copies the body before returning, appends the ordinary transmitted zero, queues communications command `6`, and wakes the network worker.

```text
CDropGold body, 9 bytes:
24 amount:u32be x:u16be y:u16be

CGiveGold body, 9 bytes:
2A amount:u32be object_id:u32be
```

Require a nonzero amount. The normal client does not compare a gold amount with the current balance before submission. For `CDropGold`, validate the requested tile locally even though observed server behavior places accepted gold beneath the character.

The same submission boundary can produce `CDrop` and `CGive` from numeric inputs alone, but doing so bypasses the item builders' live-item lookup and local manufacture-mode guard. Prefer the native item builders when a matching `InvItemPane` exists.

## Use a skill

Resolve `SkillInvItemPane *skill = skill_items[slot - 1]`, then call:

```c
void __thiscall ui_skill_inventory_activate(
    SkillInvItemPane *skill);
```

This is the normal activation path. It refuses use while `action_delay_active` at `+0x322` or the unresolved block byte at `+0x323` is set. It then sends any configured skill text and submits `CUseSkill`.

## Start a spell

The client has seven handled spell argument types. A prompt is not one target form. Type `1` opens a free-text prompt, while types `3`, `4`, `6`, and `7` open a numeric prompt with a fixed value count.

| Type | Normal interaction | `CUseSpell` trailing body |
| ---: | --- | --- |
| `1` | Free-text prompt | Nonempty raw text bytes, with no length or terminator |
| `2` | Entity-target selector | `u32` target ID, `u16` X, `u16` Y |
| `3` | Numeric prompt | Four big-endian `u16` values |
| `4` | Numeric prompt | Three big-endian `u16` values |
| `5` | No prompt or target | No trailing bytes |
| `6` | Numeric prompt | Two big-endian `u16` values |
| `7` | Numeric prompt | One big-endian `u16` value |
| `8` | No normal activation case | Unresolved; reject for manual invocation |

To reproduce the normal UI behavior, resolve the live `SpellInvItemPane` and call:

```c
void __thiscall ui_spell_inventory_activate(
    SpellInvItemPane *spell);
```

The dispatcher checks `action_delay_active` at `+0x297`, reads `spell_args_type` at `+0x194`, and then opens the matching prompt or begins the cast. This route is sufficient when the user should still type the prompt value or select the entity in the client.

### No target

Require argument type `5` and reject the command while the casting controller's `cast_active` at `+0x8C94` is already one.

For type `5`, it reaches `net_build_use_spell_no_args`, checks the denied-spell list, builds `CUseSpell`, and starts the spell's configured cast-line sequence. A zero-line spell is sent immediately.

Calling `net_build_use_spell_no_args` directly is possible, but it bypasses the action-delay check. The wrapper must reproduce that check if it uses the lower-level function.

### Entity target

Require spell argument type `2`, a live target ID, current target coordinates, no action delay, and no active cast. Then call:

```c
void __thiscall net_build_use_spell_target(
    SpellInvItemPane *spell,
    u32 target_id,
    u16 target_y,
    u16 target_x);
```

The unusual parameter order matches the native caller. The builder emits `target_id`, then `target_x`, then `target_y` on the wire. Resolve the target at execution time and read its `tile_y +0x40` and `tile_x +0x44`; stale coordinates can make the request inconsistent.

This builder checks the denied-spell list and starts the same cast-line sequence as the no-target form. It does not perform the spell entry's action-delay check.

Starting while another cast is active overwrites the queued body and cancels the casting controller's existing timers. Reject that state unless replacing the cast is explicitly intended.

Calling `ui_spell_begin_target_selection(spell, 0)` opens the native selector instead. Its other observed mode belongs to spell-icon drag and drop, not a second `CUseSpell` target format.

### Free-text and numeric prompts

Calling `ui_spell_inventory_activate` opens `StringSpellInputPane` for type `1` or `NumberArgsSpellInputPane` for types `3`, `4`, `6`, and `7`. The native submit functions require those live dialog objects and read their attached line-input controls, so they are poor entry points for a controller that already has the supplied values.

For a fully supplied command, construct the opcode-first body in the main-thread wrapper and call:

```c
void __thiscall ui_start_spell_cast(
    SpellDelayControlPane *control,
    const u8 *body,
    s16 body_length,
    u16 spell_icon,
    u8 cast_lines,
    const char *spell_name);
```

The body begins with opcode `0x0F` and the spell's one-based slot. Type `1` appends nonempty raw text bytes. The native dialog requests at most `0x64` bytes and does not add a length or terminator. Numeric forms append exactly the count of big-endian `u16` values shown above. A controller should accept already validated `u16` values directly instead of reproducing the native comma-separated text parser, whose signed and overflow behavior is not yet documented.

Before this lower-level call, require a live matching spell entry, the expected argument type, no action delay, no active cast, a non-null casting controller, and a passing denied-spell check. Enforce the exact type-specific length and keep the completed body within `2..0x7FFF` bytes because the function takes a signed 16-bit length. `ui_start_spell_cast` trusts the supplied length, replaces the shared queued body, and cancels the controller's current timers.

## Cancel casting

Get the controller and require a non-null pointer:

```c
SpellDelayControlPane *control =
    ui_spell_delay_control_pane_get();

bool __thiscall ui_cancel_spell_delay(
    SpellDelayControlPane *control);
```

The function clears `cast_active` and cancels every timer owned by the pane. It does not send a cancellation packet. It only prevents a still-queued `CUseSpell` from being sent. It cannot undo a zero-line spell or a timed spell whose final packet has already been submitted.

## Move or turn

Recover the complete `WorldPane` as described in [Runtime state walking](state-walking.md), require a ready in-game map, and validate direction `0` through `3`:

```c
bool __thiscall ui_world_pane_handle_direction_input(
    WorldPane *world,
    u8 direction);
```

The values are Up `0`, Right `1`, Down `2`, and Left `3`. This helper first clears queued path and pursuit state. If the character faces another direction, it turns and sends `CChangeDirection`. If the facing already matches, it attempts one collision-checked step and sends `CMove` only when accepted.

One invocation can therefore turn without moving. This matches ordinary directional input.

## Unequip by equipment slot

The ordinary equipment-control path receives a zero-based UI action from `0` through `17`, adds one, and calls `net_send_remove_equipment`. The packet therefore uses one-based equipment slots `1` through `18`.

To request one specific equipment slot, validate `1 <= slot <= 18`, resolve the current pane through `ui_equip_pane_get()`, and call:

```c
u32 __thiscall net_send_remove_equipment(
    EquipPane *equip,
    s16 slot);
```

The builder emits the two-byte body `{ 0x44, slot }` through `net_submit_client_packet`. It uses only the low byte of `slot`. It does not validate the range, inspect whether the slot is occupied, or dereference `equip` in this build. Pass the live pane in `ECX` anyway so the call follows the native contract and remains robust if nearby client versions differ.

The return value reports local queue submission, not server acceptance. Local equipment state changes later when the server sends `SRemoveEquip`.

### Tilde action

Get the complete pane through `ui_equip_pane_get()` and require a non-null result:

```c
void __thiscall ui_equip_pane_request_remove_slots_1_and_3(
    EquipPane *equip);
```

The helper unconditionally submits `CRemoveEquipment` for slot `1`, then slot `3`. The tilde binding was supplied as project-owner behavior; the local helper body confirms the two-slot request.

## Why `CreateRemoteThread` is unsafe

`CreateRemoteThread` starts a `DWORD WINAPI thread_proc(void *)`. It supplies one stack argument and does not install a C++ `this` pointer in `ECX`. The functions above expect `__thiscall` register state, live pane objects, and sometimes several stack arguments.

An injected thunk could marshal the registers, but it would still execute on the wrong thread. Pane lifetimes, timers, movement state, packet submission, encryption sequences, and client allocators can race the main game thread. Even `net_send_remove_equipment`, whose `ECX` value is not dereferenced in its current body, reaches the shared transport and is not safe on a worker thread.

Use `CreateRemoteThread` only for a narrow bootstrap when needed. Queue gameplay commands and invoke them from a bounded main-thread tick hook.

## Known limits

The calling contracts and state checks on this page are statically verified against the matching executable. They have not yet been exercised by an in-game injected dispatcher. Server rules can still reject any request that the local client accepts.
