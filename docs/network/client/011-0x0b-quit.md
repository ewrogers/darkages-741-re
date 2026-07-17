# Quit (`CQuit`)

`CQuit` either leaves the current connection immediately or performs the two-step safe-quit handshake used by the in-game options UI. Its optional byte identifies the safe-quit phase. It is not a general "in session" flag.

| Item | Value |
| --- | --- |
| Direction | Client to server |
| Command | `0x0B` (11) |
| Transform | static |
| Runtime owners | `OptionPane`, `SafeQuitAlert`, `MainMenuPane`, and `AgreementDialogPane` |
| Paired packet | [`SQuit`](../server/076-0x4c-quit.md) |
| Name provenance | Project-owner protocol name matched to the locally confirmed builders |

## Plaintext body

```text
packet CQuit {
    u8      opcode                    // 0x0B
    if safe_quit_flow {
        u8  phase
    }
}
```

The client has three confirmed bodies:

| Body | Producer | Meaning |
| --- | --- | --- |
| `0B` | `net_send_quit` | Leave without the safe-quit handshake |
| `0B 01` | `SafeQuitAlert` constructor | Begin a safe-quit request |
| `0B 00` | `SafeQuitAlert` after `SQuit` value `1` | Acknowledge the server's approval |

The packet length therefore identifies whether `phase` is present. The one-byte body does not contain an implicit zero.

## Safe-quit flow

`OptionPane` opens the exact RTTI class `SafeQuitAlert` for its safe-quit action. The X and x keyboard routes reach the same alert, and the pane's shared alert factory constructs it for alert type `4`.

Construction immediately sends `CQuit` with phase `1`. The alert then waits for [`SQuit`](../server/076-0x4c-quit.md). When that packet's consumed value is `1`, the alert marks the request as approved, sends phase `0`, replaces its displayed text, and refreshes its control.

A project-owner capture of the UI action confirms the complete exchange:

```text
C> 0B 01
S> 4C 01 00 00
C> 0B 00
```

The response's final two zero bytes are not inputs to the client decision. The `SQuit` deserializer consumes only the first byte after its opcode.

## Immediate quit flow

`net_send_quit` always submits a one-byte body containing only `0x0B`. There is no state-dependent payload branch in this builder.

After sending, the function closes the current pane and tears down the active network state. A separate local configuration byte then chooses between constructing `TerminalPane2`, which begins the startup connection path, and posting `WM_CLOSE` to end the process. This post-send choice is local client behavior and is not selected by a `CQuit` payload byte.

Known static callers include `MainMenuPane`, `AgreementDialogPane`, and a connection-initialization cleanup path.

## Known limits

The safe-quit phase meanings are confirmed by the client builders, the `SQuit` handler, and the capture above. The client does not assign a meaning to other phase values.

The local branch that creates `TerminalPane2` can lead back through connection startup, but no evidence ties that choice to the `SQuit` value. The exact server-side rule for granting or delaying safe quit is outside the client.
