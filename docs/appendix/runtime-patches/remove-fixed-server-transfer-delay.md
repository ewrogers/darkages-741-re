# Fast server transfer

This patch removes the guaranteed extra second after a transfer connection while preserving the transfer flow.

## Target

| Static address | RVA | File offset, reference only | Verify bytes and instruction | Write bytes and instruction |
| --- | --- | --- | --- | --- |
| `0x00564855` | `0x00164855` | `0x00163C55` | `68 E8 03 00 00` `push 1000` | `68 00 00 00 00` `push 0` |

`net_reconnect_transfer_endpoint` closes the old connection, resets transport state, applies the endpoint from `STransferServer`, and performs the new blocking connection. It then calls `Sleep(1000)` before the communications queue can continue.

`net_handle_transfer_server` waits for a later queue item on the game and UI thread. That makes the worker's fixed sleep a visible one-second animation freeze.

`PUSH 0; CALL Sleep` preserves the instruction size and the normal call boundary. It removes the guaranteed extra second while keeping socket shutdown, state resets, the blocking `connect`, seed-table ordering, command cleanup, and `CTransferServer` submission intact.

The animation may still pause for however long the actual `connect` call takes. Removing that remaining stall requires an asynchronous main-thread state machine, not another safe one-instruction change. See [Initial connection](../../network/connection.md#why-the-screen-pauses-during-a-transfer).

Apply it with the [safe launcher workflow](safe-launcher-workflow.md).
