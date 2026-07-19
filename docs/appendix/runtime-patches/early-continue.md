# Early Continue

This patch allows pointer clicks on the title menu while its initial input gate is still set.

It applies only to the version 741 target with SHA-256 `054A5D6ADC56099C6BFD9D2A58675AFF62DC788B63209A3D906492F5B89E96C6`.

## Target

At static address `0x004B7BED` (RVA `0x000B7BED`, file offset `0x000B6FED` for reference), replace:

```diff
- 000: 74 07 | je handle_pointer_input ; accept clicks only after the menu gate clears
+ 000: EB 07 | jmp handle_pointer_input ; always run normal title-menu hit testing
```

`ui_main_menu_handle_pointer_event` normally consumes pointer input while `MainMenuPane +0x500` is nonzero. The patch changes that one conditional jump into an unconditional jump to the existing hit-testing path. Choosing Continue then constructs the ordinary login dialog locally, which may give the connection flow time to finish while the player enters a name and password.

The gate covers all six title-menu entries, so this change enables early pointer clicks for Create, Continue, Password, Credit, Homepage, and Exit. The keyboard handler has a separate gate and remains unchanged.

[`SStipulation`](../../network/server/096-0x60-stipulation.md) processing is one confirmed path that clears the gate. This patch does not skip, cancel, or wait for stipulation or redirect processing. Static analysis confirms that the login dialog can open early, but it does not prove that submitting credentials before the connection flow finishes is safe. [Hide stipulation](hide-stipulation.md) remains a separate patch that suppresses the agreement window while retaining its normal processing.

Apply the change with the [safe launcher workflow](safe-launcher.md).
