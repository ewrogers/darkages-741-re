# Hold Alt to show translucent ground-item hints

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
struct GroundItemHintState741 {
    u32 count;                         // +0x000
    RenderContext *render_context;     // +0x004
    Canvas *canvas;                    // +0x008
    byte reserved[0x1C];
    WorldPane *world_pane;             // +0x028
    byte reserved_to_entries[0xD4];
    WorldDrawEntry741 entries[255];    // +0x100
};

struct WorldDrawEntry741 {
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

Enabling this option also enables the [stuck-modifier cleanup](clear-stuck-modifier-keys.md), so a lost Alt key-up during a focus change cannot leave the overlay active.

## Hook sites

| Hook | Static address | RVA | File offset, reference only | Original bytes | Continuation |
| --- | --- | --- | --- | --- | --- |
| `input_emit_key_down` | `0x00467C10` | `0x00067C10` | `0x00067010` | `55 8B EC 6A FF` | `0x00467C15` |
| `input_emit_key_up` | `0x00467E30` | `0x00067E30` | `0x00067230` | `55 8B EC 6A FF` | `0x00467E35` |
| `render_world_pane_content` | `0x005CE280` | `0x001CE280` | `0x001CD680` | `55 8B EC 83 EC 1C` | `0x005CE286` |
| `render_collect_world_objects` | `0x005D3740` | `0x001D3740` | `0x001D2B40` | `55 8B EC 6A FF` | `0x005D3745` |

Each five-byte site receives `E9 <stub rel32>`. The six-byte frame site receives `E9 <stub rel32> 90`. Every stub contains a local trampoline that executes the complete displaced prologue and jumps to the listed continuation.

The implementation emits stubs of these fixed sizes:

| Stub | Size |
| --- | ---: |
| collector | 157 bytes |
| completed-frame replay | 186 bytes |
| key down | 84 bytes |
| key up | 84 bytes |

Stub builders resolve the actual module base, allocated state address, allocated stub address, helper calls, vtable address, and return displacement. Static Binary Ninja addresses are never treated as fixed runtime pointers.

## Ordering and limits

The replay happens after the complete normal world-pane draw. This guarantees that static map art cannot hide the hint. It also means the hint is technically later than players, monsters, effects, and lighting.

The implementation has no static-rectangle intersection test, no player or monster overlap filter, and no blinded-state gate. The translucent mode keeps the result hint-like, but it is still a topmost item copy. This is the deliberate reliability tradeoff in the working implementation.

The native local-player replay remains separate. `render_replay_layer_zero_and_self` is not hooked, and the item renderer is not patched. Normal jungle-tree mode `0x6D` also remains unchanged.

## Preserve the static renderer

Before allocating anything, the launcher verifies the original 48-byte static mode selector at `0x005E487D`:

```text
8B 55 D0 0F B6 82 B9 00 00 00 25 80 00 00 00 74
09 C7 45 E8 6D 00 00 00 EB 16 8B 4D D0 0F B6 91
B9 00 00 00 83 E2 40 74 07 C7 45 E8 03 00 00 00
```

These bytes are verified but never replaced. This both rejects the earlier whole-static prototype and proves that SOTP flag `0x80`, flag `0x40`, and jungle-tree behavior are intact.

## Safe installation and rollback

Apply the patch while the matching client is suspended. Verify the executable fingerprint, four hook prologues, and static selector before writing. Allocate the state and four stubs, populate all relocations, make the stubs executable, verify their bytes, and flush the instruction cache. Then install and verify all four jumps.

On failure, restore written hooks in reverse order. Free a stub only after its hook is confirmed restored. Free shared state only after every hook is safe. Preserve cleanup failures alongside the original error and do not resume a partially patched client.

The implementation's targeted `GameClientServiceTests` cover the 255-entry bound, all resolved helper and continuation targets, both Alt scan codes, static-selector preservation, and five- versus six-byte jump construction.
