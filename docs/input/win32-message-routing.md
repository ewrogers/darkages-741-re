# Win32 message routing

## Message pump

`input_run_message_pump` at `0x4AC750` is a nonblocking `PeekMessageA` loop. It records the main thread ID in `app_main_thread_id` at `0x740400`, removes one message at a time, optionally runs a filter callback stored at application offset `+0x1014C`, then calls `TranslateMessage` and `DispatchMessageA`.

The filter consumes a message by returning zero. When the queue is empty, the client runs its guarded idle or frame callback and checks its exit fields.

Equivalent control flow:

```c
for (;;) {
    while (PeekMessageA(&msg, 0, 0, 0, PM_REMOVE)) {
        if (app->message_filter != 0 && !app->message_filter(&msg))
            continue;

        TranslateMessage(&msg);
        DispatchMessageA(&msg);
    }

    run_guarded_idle_tick();

    if (app->exit_requested || global_exit_requested)
        break;
}
```

## Window procedure

`input_client_window_proc` at `0x4A9C30` calls `input_translate_win32_message` first. If the translator supplies a final result, the procedure returns it. Otherwise the procedure continues with its window, socket, and custom-message cases.

| Message | Value | Client behavior |
|---|---:|---|
| `WM_DESTROY` | `0x0002` | Calls `PostQuitMessage`, performs window cleanup, and sets exit flags |
| `WM_MOVE` | `0x0003` | Recomputes client geometry |
| `WM_SIZE` | `0x0005` | Recomputes client geometry |
| `WM_ACTIVATE` | `0x0006` | Updates active state and restores the window when appropriate |
| `WM_CLOSE` | `0x0010` | Starts shutdown and sets exit flags |
| Winsock event | `0x0401` | `FD_READ` value `1` enters socket receive; `FD_CLOSE` value `0x20` closes the transport |
| Custom | `0x0472` | Runs a guarded client maintenance callback; exact purpose is not yet named |
| Custom dispatch | `0x073C` | Dispatches the message object passed in `wParam` on the main thread, then releases it |

The main HWND is stored at `0x73D938`. A proxy can register its own private window message, post it to this HWND, and handle it in a window-procedure detour to execute bounded commands on the main thread. The existing `0x073C` message takes ownership of a client-allocated event object and should not be reused with foreign allocations.

## Win32 input translator

`input_translate_win32_message` at `0x48E980` handles the following messages directly:

| Message | Value | Internal action |
|---|---:|---|
| `WM_CLOSE` | `0x0010` | Closes and destroys the active IME context before normal shutdown continues |
| `WM_INPUTLANGCHANGE` | `0x0051` | Rebuilds the IME context for the new input language |
| `WM_KEYDOWN` | `0x0100` | Converts the scan code and emits key-down event type `8` |
| `WM_KEYUP` | `0x0101` | Clears key state and emits key-up event type `9` |
| `WM_CHAR` | `0x0102` | Emits character event type `0x0B` for supported text characters |
| `WM_SYSKEYDOWN` | `0x0104` | Handles the Alt key path, including an Alt+S special case, then follows key-down handling |
| `WM_SYSKEYUP` | `0x0105` | Handles the matching Alt key release path |
| `WM_IME_STARTCOMPOSITION` | `0x010D` | Starts an internal IME composition event |
| `WM_IME_ENDCOMPOSITION` | `0x010E` | Ends internal IME composition |
| `WM_IME_COMPOSITION` | `0x010F` | Reads result and composition strings with `ImmGetCompositionStringA` |
| `WM_MOUSEMOVE` | `0x0200` | Emits pointer event type `0` |
| `WM_LBUTTONDOWN` | `0x0201` | Emits type `1`, or type `2` for a detected double-click |
| `WM_LBUTTONUP` | `0x0202` | Emits type `3` |
| `WM_RBUTTONDOWN` | `0x0204` | Emits type `4`, or type `5` for a detected double-click |
| `WM_RBUTTONUP` | `0x0205` | Emits type `6` |
| `WM_MOUSEWHEEL` | `0x020A` | Emits type `7` with the signed wheel delta |
| `WM_IME_SETCONTEXT` | `0x0281` | Calls `DefWindowProcA` with the client-controlled IME context flags |
| `WM_IME_NOTIFY` | `0x0282` | Updates IME open state and candidate-list state |
| `WM_IME_KEYDOWN` | `0x0290` | Marks an IME key transition as handled |
| `WM_IME_KEYUP` | `0x0291` | Marks an IME key transition as handled |
| Custom IME control | `0x05E2` | Changes IME conversion or context association state |

Middle-button messages are accepted by the surrounding switch but no internal middle-button event was recovered. `WM_SYSCHAR` and nearby unlisted keyboard messages also have no recovered special conversion.

## Coordinates

Mouse coordinates come from the low and high 16-bit halves of `lParam`. In the client's scaled display mode, both coordinates are divided by two. The logical X coordinate is clamped to `0..639`, and renderer cursor state is updated under a critical section before the event is submitted.
