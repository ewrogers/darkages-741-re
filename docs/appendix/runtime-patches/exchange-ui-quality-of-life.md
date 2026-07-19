# Exchange UI quality-of-life hooks

These changes make `ExchangeDialog` draggable, optionally suppress its final alerts, and provide lifecycle hooks for temporarily using the small main-UI layout while an expanded item inventory is visible.

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

| Static address | RVA | File offset, reference only | Verify | Write |
| --- | --- | --- | --- | --- |
| `0x00469E33` | `0x00069E33` | `0x00069233` | `C7 82 2C 06 00 00 00 00 00 00` | `C7 82 2C 06 00 00 01 00 00 00` |

This does not add a custom drag handler. Controls keep their normal hit testing, while unused dialog background can start a drag through primary-vtable slot `+0x48`.

## Suppress the two final alerts

Both close paths allocate a `0x634`-byte one-button alert and already handle allocation failure by skipping construction. Replacing the allocation sequence with `EAX = 0` takes that existing no-alert branch without allocating or leaking an object. The exchange-removal call remains unchanged.

| Result | Static address | RVA | File offset, reference only | Verify |
| --- | --- | --- | --- | --- |
| Cancelled event `0x04` | `0x0046AA81` | `0x0006AA81` | `0x00069E81` | `6A 00 68 34 06 00 00 E8 43 9A 04 00` |
| Final Accepted event `0x05` | `0x0046AC57` | `0x0006AC57` | `0x0006A057` | `6A 00 68 34 06 00 00 E8 6D 98 04 00` |

The same-size replacement for either row is:

```text
31 C0 90 90 90 90 90 90 90 90 90 90
```

Apply both rows to suppress both messages. Event `0x05` reaches its patched block only after both parties are accepted. Earlier acceptance updates still redraw the acknowledgement state and keep the dialog open.

## Redirect the text to the floating message bar

Redirection needs a detour because the visible text is packet data. The narrow design combines the no-alert patches above with hooks at the two event handlers:

| Role | Static address | RVA | First five bytes |
| --- | --- | --- | --- |
| Cancelled handler | `0x0046A9E0` | `0x0006A9E0` | `55 8B EC 6A FF` |
| Accepted handler | `0x0046AB20` | `0x0006AB20` | `55 8B EC 6A FF` |
| Floating palette append | `0x004803A0` | `0x000803A0` | `55 8B EC 51 8D` |

For Cancelled, the decoded body is:

```text
[0] opcode, [1] event, [2] party, [3] length, [4..] message
```

For Accepted, append only when the incoming party will complete the pair. Party zero will complete when `other_accepted` at `ExchangeDialog +0x636` is already one. A nonzero party will complete when `local_accepted` at `+0x635` is already one.

Copy at most 130 bytes to a hook-owned stack buffer, add a null terminator, append it with palette `0x58`, then append the normal newline. Afterward run the original handler through its trampoline. With the no-alert patch installed, the native handler still updates state and removes the exchange but creates no popup.

This mirrors only the floating `SMessage` type `0x00` display branch. Do not call the network parser recursively. If persistent history is also required, queue a bounded synthetic message event for the normal main-thread dispatcher.

## Detect and track ExchangeDialog

There is no exchange singleton. The general modal count at `0x006FCFF8` is not specific enough.

| Role | Static address | RVA | First five bytes |
| --- | --- | --- | --- |
| `ui_exchange_dialog_ctor` | `0x00469560` | `0x00069560` | `55 8B EC 6A FF` |
| `ui_exchange_dialog_dtor` | `0x00469E70` | `0x00069E70` | `55 8B EC 6A FF` |
| Exact primary vtable | `0x0067442C` | `0x0027442C` | Not a code hook |

Retain the exact object pointer after the constructor trampoline returns. Clear it after the destructor trampoline returns. Use a generation token so a delayed cleanup for an older object cannot restore state for a newer exchange.

## Force the small layout and restore it safely

The relevant `GUIBackPane` fields are:

```c
s32 layout_index;       // +0x4DF0: 0 _nbk_s.txt, 1 _nbk_l.txt
s32 current_page;       // +0x4FA8: 0 item inventory
u8  page_is_expanded;   // +0x4FB0
```

The native helpers are:

| Role | Static address | RVA |
| --- | --- | --- |
| `ui_gui_back_select_page_mode` | `0x005A2FB0` | `0x001A2FB0` |
| `ui_gui_back_apply_layout` | `0x005A3900` | `0x001A3900` |
| `ui_get_gui_back_pane` | `0x005A9C40` | `0x001A9C40` |

`ui_gui_back_select_page_mode` is a method of the secondary controller at `GUIBackPane +0x194`. Its call shape for this use is page `0`, expanded `1`.

Before calling the exchange constructor trampoline:

```c
gui = ui_get_gui_back_pane();

if (gui != NULL &&
    gui->layout_index == 1 &&
    gui->current_page == 0 &&
    gui->page_is_expanded != 0) {
    save_hook_generation_and_exchange_state();
    ui_gui_back_apply_layout(gui, 0);
    ui_gui_back_select_page_mode((u8 *)gui + 0x194, 0, 1);
}
```

Calling the page method after the layout method matters. The layout change first applies the normal item rectangle; the page call then selects the small layout's expanded item rectangle.

After the matching exchange destructor finishes, restore layout `1` and re-apply page `0`, expanded `1`, only when the generation still matches and all three UI fields still describe the hook-installed state. If the player changed layout, page, or expansion, discard the saved state and leave the newer choice untouched.

The constructor hook runs on the main event thread and is reached only when the native start handler creates the dialog. A refused exchange therefore cannot change the layout. The destructor hook covers every verified pane-removal path.

Apply all code changes with the [safe launcher workflow](safe-launcher-workflow.md). Keep hook state bounded and local, resolve addresses from the loaded module base, and never wait for controller IPC from these hooks.
