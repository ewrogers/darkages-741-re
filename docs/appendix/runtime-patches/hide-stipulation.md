# Hide stipulation

This patch hides the agreement window while preserving `SStipulation` processing and the normal main-menu continuation.

## Targets

When the cached greeting CRC matches, patch static address `0x004B897C` (RVA `0x000B897C`, file offset `0x000B7D7C` for reference):

```diff
- 000: 75 6C | jne skip_agreement ; skip only when the native condition is true
+ 000: EB 6C | jmp skip_agreement ; always bypass the stipulation window
```

When a replacement greeting was inflated and saved, patch static address `0x004B8ACF` (RVA `0x000B8ACF`, file offset `0x000B7ECF` for reference):

```diff
- 000: 75 6D | jne skip_agreement ; skip only when the native condition is true
+ 000: EB 6D | jmp skip_agreement ; always bypass the stipulation window
```

These two same-size jump changes hide the agreement window without skipping [`SStipulation`](../../network/server/096-0x60-stipulation.md) processing.

Each original `JNE` skips `AgreementDialogPane` only in Japan distribution mode. Replacing opcode byte `75` with `EB` turns it into an unconditional jump to the same existing continuation. The displacement byte is unchanged.

That continuation clears `MainMenuPane +0x500`. The main-menu pointer and keyboard handlers reject input only while this value is nonzero, so Login remains enabled and clickable. The agreement pane's OK action sends no packet, which means there is no acknowledgement to emulate.

Apply both changes. One covers a matching cached greeting and the other covers a newly received replacement. Homepage requesting, CRC mismatch recovery, zlib inflation, table saving, and the final menu-state update all run normally.

[Early Continue](early-continue.md) is a separate option that permits title-menu pointer input before this processing clears the gate.

Apply them with the [safe launcher workflow](safe-launcher.md).
