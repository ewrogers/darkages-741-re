# Exchange UI quality-of-life hooks

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

## Installation scope

The draggable-dialog change and the two no-alert changes are independent, same-size byte patches. Redirecting alert text to the floating message bar remains an optional detour.

No constructor hook, destructor hook, exchange pointer tracking, or `GUIBackPane` layout save and restore is required. The player can drag the exchange window away from the expanded inventory instead of temporarily forcing the small main-UI layout.

Apply all code changes with the [safe launcher workflow](safe-launcher-workflow.md). Resolve addresses from the loaded module base, and never wait for controller IPC from a text-redirection hook.
