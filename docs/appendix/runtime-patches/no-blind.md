# No blind

This patch prevents `SStatus` from enabling the blinded world overlay while preserving the normal status update and redraw path.

It applies only to the version 741 target with SHA-256 `054A5D6ADC56099C6BFD9D2A58675AFF62DC788B63209A3D906492F5B89E96C6`.

## Target

At static address `0x005F1A2D` (RVA `0x001F1A2D`, file offset `0x001F0E2D` for reference), replace:

```diff
- 000: 83 F8 08 | cmp eax, 8  ; blind_code 0x08 enables the blinded state
+ 000: 83 F8 FF | cmp eax, -1 ; a zero-extended packet byte can never match
```

The handler first zero-extends `blind_code` into `EAX`, compares it with `0x08`, and passes the equality result to `ui_world_pane_set_blinded`. Changing only the comparison operand makes that result false for every possible packet byte. The existing setter still runs, so it clears the stored blinded state and requests the usual world redraw.

This does not discard the rest of the [`SStatus`](../../network/server/008-0x08-status.md) combat-modifier block. If the patch is installed after the client is already blinded, it takes effect when the next matching status update reaches the setter. A suspended-launch patch avoids that transient case.

Apply it with the [safe launcher workflow](safe-launcher.md).
