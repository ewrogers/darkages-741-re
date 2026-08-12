# Bootstrap sequence race

This patch prevents a timing-dependent disconnect during the first server selection. It resets the outgoing encrypted-packet sequence before `CHello` is given to the communications worker, so `CHello` always uses sequence `0` and the later `CMulti` always uses sequence `1`.

The failure happens before a server transfer is received. It can look like a transfer problem because the server closes the bootstrap connection instead of sending `STransferServer`.

## Why it happens

The game and communications worker share `net_client_packet_sequence`. The game thread performs these operations:

```text
queue CHello
reset outgoing sequence to 0
queue raw CVersion
```

Queuing does not encrypt the packet immediately. The communications worker encrypts `CHello` later, and either thread may reach the shared counter first.

```text
Working order                         Failing order
reset sequence to 0                  worker sends CHello with sequence 0
worker sends CHello with sequence 0  worker advances sequence to 1
worker advances sequence to 1        game thread resets sequence to 0
CMulti uses sequence 1               CMulti reuses sequence 0
```

`CVersion` is raw, so it does not advance the counter. `SVersionCheck` installs the negotiated seed-table selector and key, but it does not repair the outgoing sequence.

In a captured failure, both `CHello` and `CMulti` carried sequence `0`. The `CMulti` transform and MD5 bytes were otherwise valid. The server acknowledged the TCP data and closed the connection without sending `STransferServer`. A proxy with its own correctly ordered counter sent `CHello` as `0` and `CMulti` as `1`, which explains why redirecting the client through that proxy works.

Restarting the machine does not reset hidden protocol state on the server. A cold start changes thread scheduling, paging, caches, background load, and possibly virtual-machine translation state. Those changes can make the game thread win this race on the first launch. The exact cold-start bias has not been isolated, so the first successful run after reboot should be treated as favorable timing, not a guaranteed reset mechanism.

## Patch design

The safe fix moves the reset before the asynchronous submission. Merely removing the reset is not sufficient because a reconnect may begin with a nonzero counter.

The executable uses preferred image base `0x00400000`.

| Role | Static address | RVA | File offset | Verified bytes |
| --- | --- | --- | --- | --- |
| `CHello` submit call | `0x00579849` | `0x00179849` | `0x00178C49` | `E8 B2 A5 FE FF` |
| Late sequence reset call | `0x0057993A` | `0x0017993A` | `0x00178D3A` | `E8 A1 A4 FE FF` |
| `net_reset_client_packet_sequence` | `0x00563DE0` | `0x00163DE0` | `0x001631E0` | helper target |
| `net_submit_client_packet` | `0x00563E00` | `0x00163E00` | `0x00163200` | original call target |

Allocate at least 12 executable bytes within signed `rel32` reach of the main module and build this stub at `stub_base`:

```text
000: 51                | push ecx        ; preserve the Socket* this pointer
001: E8 00 00 00 00    | call reset      ; reset before CHello enters the worker queue
006: 59                | pop ecx         ; restore the Socket* this pointer
007: E9 00 00 00 00    | jmp submit      ; tail-call the displaced submission target
```

`net_submit_client_packet` is a `__thiscall` function. Its socket pointer arrives in `ECX`, while its body pointer and length are already on the stack. The balanced `PUSH` and `POP` preserve that calling contract. The final `JMP` leaves the original return address and stack arguments unchanged.

Write each displacement as a signed little-endian 32-bit integer:

| Operand | Value |
| --- | --- |
| Replacement `CALL` at RVA `0x00179849` | `stub_base - (module_base + 0x0017984E)` |
| Stub offset `0x02`, `CALL reset` | `(module_base + 0x00163DE0) - (stub_base + 0x06)` |
| Stub offset `0x08`, `JMP submit` | `(module_base + 0x00163E00) - (stub_base + 0x0C)` |

Replace the original `CHello` submission call with `E8 <rel32-to-stub>`. Replace the late reset call as a complete five-byte instruction:

```diff
- 000: E8 A1 A4 FE FF | call net_reset_client_packet_sequence
+ 000: 90 90 90 90 90 | nop; nop; nop; nop; nop
```

Reject installation if any displacement is outside the signed 32-bit range.

## Installation and validation

Install this only through the [safe launcher workflow](safe-launcher.md):

1. Verify the exact executable size, SHA-256, and both original five-byte calls.
2. Launch suspended and resolve the loaded main-module base.
3. Allocate the stub, fill its relocations, write it, change it to executable protection, and verify all 12 bytes.
4. Write the replacement `CHello` call and the five NOPs while the process remains suspended.
5. Verify both sites and their surrounding bytes, restore page protections, and flush the instruction cache for all three regions.
6. Resume only after every check succeeds. Terminate the suspended child if any check fails.

The call sites, original bytes, helper addresses, asynchronous queue behavior, and failing wire sequence were rechecked against the local version-741 client. The injected form has not yet been validated in a patched runtime capture. A final validation should confirm `CHello` sequence `0`, `CMulti` sequence `1`, and receipt of `STransferServer` without a proxy.
