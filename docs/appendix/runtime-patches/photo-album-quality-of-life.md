# Photo album

The portrait album has two client-owned annoyances: a fixed one-hour capture delay and a low-quality JPEG default. Both can be changed without modifying `album.dat` or network packets.

These addresses and bytes apply only to the documented 7.41 executable:

```text
SHA-256: 054A5D6ADC56099C6BFD9D2A58675AFF62DC788B63209A3D906492F5B89E96C6
preferred image base: 0x00400000
```

Use the loaded module base plus the RVA. Verify the fingerprint and original bytes before writing.

## Bypass the one-hour cooldown

`ui_world_capture_self_portrait_to_album` passes zero for a normal capture. The callee already treats a nonzero argument as an intentional cooldown bypass.

| Static address | RVA | Original bytes and instruction | Replacement bytes and instruction |
| --- | --- | --- | --- |
| `0x005F9B07` | `0x001F9B07` | `6A 00` `push 0` | `6A 01` `push 1` |

This changes only the wrapper argument from `push 0` to `push 1`. Capacity checks, capture rendering, captions, file writes, and failure messages remain native.

## Raise JPEG quality

The bundled IJG compressor installs quality 75 in `jpeg_set_defaults`. A same-size immediate change can select another quality. This example selects 95:

| Static address | RVA | Original bytes and instruction | Replacement bytes and instruction |
| --- | --- | --- | --- |
| `0x0060D6E3` | `0x0020D6E3` | `6A 4B` `push 75` | `6A 5F` `push 95` |

`0x64` would select quality 100. The portrait uploader rejects JPEG files of 8,000 bytes or more, so every chosen quality should be tested against complex portraits before it becomes a launcher default.

## Disable chroma subsampling

The RGB compressor converts to YCbCr. Its default setup places the value 2 in both luma sampling factors, while both chroma components use 1. Changing that shared value to 1 produces 4:4:4 sampling:

| Static address | RVA | Original bytes and instruction | Replacement bytes and instruction |
| --- | --- | --- | --- |
| `0x0060DA08` | `0x0020DA08` | `BA 02 00 00 00` `mov edx, 2` | `BA 01 00 00 00` `mov edx, 1` |

The default-quality and sampling helpers are reached through the client's JPEG compressor. This includes both album Save implementations and the generic canvas JPEG writer. It does not affect the `lodNNN.bmp` screenshot writer or JPEG decoding.

Quality 95 and 4:4:4 should be evaluated together. Either change can increase the file size.

## EPF is not a patch branch

Neither album Save implementation contains an EPF choice. Redirecting Save to EPF needs a new encoder and palette-index conversion, so it cannot be expressed as a same-size branch change. The existing EPF code only loads, displays, and uploads an already-created portrait file.

Follow the [safe launcher workflow](safe-launcher-workflow.md) for suspended launch, byte verification, page protection, instruction-cache flushing, and fail-closed cleanup.
