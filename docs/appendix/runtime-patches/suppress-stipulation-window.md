# Hide stipulation

This patch hides the agreement window while preserving `SStipulation` processing and the normal main-menu continuation.

## Targets

| Path | Static address | RVA | File offset, reference only | Verify bytes and instruction | Write bytes and instruction |
| --- | --- | --- | --- | --- | --- |
| Cached greeting CRC matches | `0x004B897C` | `0x000B897C` | `0x000B7D7C` | `75 6C` `jne skip_agreement` | `EB 6C` `jmp skip_agreement` |
| Replacement greeting was inflated and saved | `0x004B8ACF` | `0x000B8ACF` | `0x000B7ECF` | `75 6D` `jne skip_agreement` | `EB 6D` `jmp skip_agreement` |

These two same-size jump changes hide the agreement window without skipping [`SStipulation`](../../network/server/096-0x60-stipulation.md) processing.

Each original `JNE` skips `AgreementDialogPane` only in Japan distribution mode. Replacing opcode byte `75` with `EB` turns it into an unconditional jump to the same existing continuation. The displacement byte is unchanged.

That continuation clears `MainMenuPane +0x500`. The main-menu pointer and keyboard handlers reject input only while this value is nonzero, so Login remains enabled and clickable. The agreement pane's OK action sends no packet, which means there is no acknowledgement to emulate.

Apply both changes. One covers a matching cached greeting and the other covers a newly received replacement. Homepage requesting, CRC mismatch recovery, zlib inflation, table saving, and the final menu-state update all run normally.

Apply them with the [safe launcher workflow](safe-launcher-workflow.md).
