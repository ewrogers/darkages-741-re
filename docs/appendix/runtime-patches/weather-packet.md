# Weather packet

Version 7.41 constructs and decodes `SChangeWeather`, then drops it because the gameplay dispatcher has no opcode `0x1F` branch. This runtime patch adds the missing bridge to the client's existing map-weather code.

It restores live None, Snow, and Darkness changes. It does not create rain because the native mode-2 branch performs no setup and no rain renderer was recovered.

## Behavior

The unmodified path stops after decoding:

```text
SChangeWeather 0x1F
  -> packet factory
  -> one-byte decoder
  -> gameplay dispatcher
  -> no matching branch
```

The injected branch treats the packet byte as the map's weather mode:

```text
packet value
  -> WorldPane_Impl + 0x264
  -> map_apply_weather_mode
  -> redraw WorldPane
  -> world_update_map_lighting
```

The lighting update is required. Entering Darkness forces black ambient color and zero intensity. `map_apply_weather_mode` clears the Darkness flags when another mode arrives, but it does not restore the normal ambient values. `world_update_map_lighting` reapplies the current map and `SChangeHour` state, matching the end of map setup.

This value mapping is a patch design based on the existing `SMapSize` path. The unmodified `SChangeWeather` packet has no native consumer that can confirm its intended enum.

## Hook site

The preferred image base is `0x00400000`. File offsets are reference information only. A launcher uses the loaded module base plus the RVA.

| Purpose | Static address | RVA | File offset | Verified original bytes | Replacement |
| --- | ---: | ---: | ---: | --- | --- |
| Intercept decoded weather before normal opcode dispatch | `0x005ED9B9` | `0x001ED9B9` | `0x001ECDB9` | `33 D2 74 05 E9 C3 07 00 00` | `E9 <rel32 to stub> 90 90 90 90` |

This site follows the native stores of the world pointer at `[ebp-0x0C]` and parsed packet pointer at `[ebp-0x04]`. The overwritten instructions are an always-taken opaque branch. The stub reproduces their `xor edx,edx` before returning non-weather packets to native dispatch at `0x005ED9C2`.

For the hook, write:

```text
rel32 = stub - (module_base + 0x001ED9BE)
```

## Injected stub template

Allocate and write at least `0x47` bytes. All zeroed external `rel32` operands below are relocation placeholders. The two local short branches are complete.

```text
000: 83 7D FC 00                | cmp dword [ebp-0x04],0       ; parsed packet?
004: 74 3A                      | je native_dispatch
006: 8B 4D FC                   | mov ecx,[ebp-0x04]
009: E8 00 00 00 00             | call net_get_server_packet_opcode
00E: 83 F8 1F                   | cmp eax,0x1F
011: 75 2D                      | jne native_dispatch

013: 8B 45 FC                   | mov eax,[ebp-0x04]
016: 8A 50 10                   | mov dl,[eax+0x10]            ; decoded value
019: 8B 4D F4                   | mov ecx,[ebp-0x0C]           ; WorldPane_Impl
01C: 88 91 64 02 00 00          | mov [ecx+0x264],dl          ; weather mode
022: E8 00 00 00 00             | call map_apply_weather_mode

027: 6A 00                      | push 0                       ; whole pane
029: 8B 4D F4                   | mov ecx,[ebp-0x0C]
02C: E8 00 00 00 00             | call ui_pane_invalidate
031: 8B 4D F4                   | mov ecx,[ebp-0x0C]
034: E8 00 00 00 00             | call world_update_map_lighting
039: 30 C0                      | xor al,al                    ; match map handler
03B: E9 00 00 00 00             | jmp native_epilogue

040: 31 D2                      | native_dispatch: xor edx,edx
042: E9 00 00 00 00             | jmp native_dispatch_continue
```

## Stub relocations

For each entry, write a signed little-endian displacement:

```text
rel32 = target - (stub + instruction_end)
```

| Operand offset | Instruction end | Target RVA | Target |
| ---: | ---: | ---: | --- |
| `0x00A` | `0x00E` | `0x00195A00` | `net_get_server_packet_opcode` |
| `0x023` | `0x027` | `0x001F26C0` | `map_apply_weather_mode` |
| `0x02D` | `0x031` | `0x00149F60` | `ui_pane_invalidate` |
| `0x035` | `0x039` | `0x001EF360` | `world_update_map_lighting` |
| `0x03C` | `0x040` | `0x001EE187` | Native dispatcher epilogue |
| `0x043` | `0x047` | `0x001ED9C2` | Native opcode dispatch |

Add the loaded module base to each target RVA. Validate that the allocated stub is within signed `rel32` range of the hook and every target before writing.

## Installation and removal

Use the [safe launcher](safe-launcher.md). Require the exact version-741 fingerprint and verify the nine original hook bytes before writing.

1. Start the process suspended.
2. Allocate at least `0x47` bytes in signed relative-branch range.
3. Copy the stub template and apply all six relocations.
4. Make the completed stub executable.
5. Replace the hook with its relocated jump and four padding bytes.
6. Restore page protections and flush the instruction cache for the stub and hook.
7. Resume only after every check and write succeeds.

If any step fails, restore the original hook bytes before resuming or terminate the suspended process. Removal restores those bytes, flushes the instruction cache, and releases the stub allocation.

This is an in-memory patch. It must never rewrite `Darkages.exe`.

## Test checklist

- Send `1F 01` after map setup and confirm that the 100 ms falling-snow animation starts.
- Send `1F 00` and confirm that the snow overlay stops.
- Send `1F 03` and confirm black ambient lighting and human light masks.
- Send `1F 00` again and confirm that the current map and hour lighting returns.
- Send `1F 02` and confirm that no rain overlay appears. This is the recovered native behavior.
- Enter another map and confirm that its `SMapSize` flags still replace the active weather normally.

## Known limits

- The hook site, packet field offset, native calls, continuations, and stub bytes are statically verified against the matching client. The complete patch still needs in-game runtime testing before it should be enabled by default.
- Values `0` through `3` are mapped to the existing map modes by the patch. That mapping is not proven by an original `SChangeWeather` handler in version 7.41.
- Rain remains unavailable. Implementing it would require a new renderer or a verified server-driven effect, not just packet dispatch.
- The patch changes the live weather mode only. Snow-covered ground and static art still require [`SMapSize`](../../network/server/021-0x15-map-size.md) flag `0x80`.
- Apply weather only through the normal decoded-packet event on the game thread. Do not call the native weather functions from an IPC or network worker.
