# 035 / 0x23: Exit Editing Mode (`CExitEditingMode?`)

- Direction: client to server
- Internal name: `CExitEditingMode?`
- Local behavioral alias: `ExitEditingMode / EditNotepad (Paper)`
- Related-game enum name: `ExitEditingMode`
- Name provenance: Related-game internal enum name `ExitEditingMode` at the same opcode, strongly corroborated by this client's paper-editor submission builder; the C++ class spelling remains reconstructed.
- Evidence: 1 concrete builder/sender call site
- Send handling: default common transform mode 1
- Wire frame after transformation: `0xAA, u16be body_size, body`

## Builder call sites

- `0x54a7d0` : `net_send_c_exit_editing_mode`

## Current structural notes

The recovered body is:

| Offset | Type | Meaning |
|---:|---|---|
| 0 | `u8` | opcode `0x23` |
| 1 | `u8` | editing/paper mode from the editor object |
| 2 | `u16be` | text length |
| 4 | `bytes[text_length]` | submitted paper text |

- The builder reads up to `0x1F40` bytes from the active editor and converts carriage returns (`0x0D`) to tabs (`0x09`) before sending.
- This directly favors the same-opcode internal enum name `ExitEditingMode` over the earlier speculative `CScript` match.
- The paired editable server packet is [0x1B `EnterEditingMode`](../server/027-0x1b-enter-editing-mode.md). Its byte 1 editor-mode value is stored locally and echoed here as byte 1, while the edited text is returned after it.
- Read-only [0x35 `SShowPaper`](../server/053-0x35-show-paper.md) uses the same window with mode `1`. Closing it skips this builder entirely, so no `0x23` or other client packet is sent.
