# Random number generation

The client uses random values for presentation, minigames, installation identity, login masking, and packet encryption. Two unrelated generators supply those values. Most game code uses a predictable C runtime generator whose state can be replaced. Packet encryption uses Windows secure random bytes and does not share that state.

## Two independent paths

```text
crt_srand(seed)                  Windows SystemFunction036
       |                                  |
per-thread 32-bit state                   v
       |                            random 32-bit value
       v                                  |
   crt_rand()                    encrypted packet seeds
       |
UI, effects, fishing, login,
installation ID, dialog wrapper
```

The packet transform also has a seed-table selector, a character-name-derived MD5 source, and packet sequence bytes. Those values are separate from both random generators described here.

## C runtime generator

`crt_rand` is the older Microsoft C runtime linear-congruential generator. Each call updates a 32-bit state and returns 15 bits:

```c
state = state * 0x343FD + 0x269EC3;
return (state >> 16) & 0x7FFF;
```

The state is stored at offset `0x14` in the C runtime's per-thread data block. It is not one process-wide global. Calls made on different threads advance different sequences.

`crt_srand` replaces the calling thread's state directly. The matching client calls it from five places:

| Owner | Seed | When it happens |
|---|---:|---|
| Default endpoint and installation setup | Unix time in seconds | During configuration setup |
| Socket constructor | Unix time in seconds | While constructing the socket object |
| Motion-effect table loader | Unix time in seconds | On the loader's first initialization path |
| Fishing dialog constructor | Unix time in seconds plus `timeGetTime()` | Each time the fishing dialog is constructed |
| Login request builder | Unix time in seconds | Immediately before building each login installation block |

Several calls can therefore receive the same seed when they occur within one second. Fishing adds the millisecond uptime counter, which gives it finer variation.

### Confirmed consumers

Static cross-references find 46 `crt_rand` call instructions in 24 functions. Their confirmed or strongly bounded uses are:

| Area | Random behavior |
|---|---|
| Installation identity | Builds a persistent 32-bit installation ID from four low bytes and adds random padding to the related registry value when either value is missing. |
| Login request | Reseeds immediately, then creates two masking bytes and a four-byte nonce for the 16-byte installation block. |
| Merchant and pursuit responses | Adds two random bytes to the special inner wrapper before its length, CRC, and incrementing XOR transform. |
| Regional endpoint setup | Selects an offset within a configured endpoint range. This path belongs to the SK distribution branch. |
| Fishing | Chooses spawn chance, horizontal direction, vertical position, sprite, and speed. |
| Logo animation | Selects one of six palettes when the animation phase wraps. |
| UI scheduling | Chooses delays of 2 through 6 seconds and 5 through 11 seconds for two pane timers. |
| Moving and motion effects | Selects table entries, weighted branches, animation or direction variants, and bounded values used by effect instances. |
| Other visual helpers | Selects sprite variants, background variants, screen offsets, and bounded positions. Several owners in this group still lack confident project names. |

Character creation also starts with a time-derived gender and hair style. That behavior does not call `crt_rand`, so it is not part of this shared sequence.

## Secure packet generator

`crt_rand_s` dynamically resolves `SystemFunction036` from `ADVAPI32.DLL`. This is the Windows `RtlGenRandom` path. The client calls it only from `net_encrypt_client_packet`, once for each ordinary encrypted client packet.

The returned 32-bit value supplies the 16-bit and 8-bit values used to derive the nine-byte packet key and the three encoded trailer bytes. The client does not seed this generator and `crt_srand` cannot control it.

The wrapper clears its output before calling Windows. `net_encrypt_client_packet` does not check the wrapper's return code. If Windows random generation fails, the cleared zero value continues through the packet-seed mapping. This is a failure-path observation, not behavior seen during a normal connection.

## Can the seed be overwritten?

Yes, for `crt_rand`. Calling `crt_srand` on the target thread replaces the state immediately, and writing the per-thread state field has the same effect. Calling it from an injected worker thread would only change that worker's sequence, so a launcher or proxy would need to queue the call onto the client thread that owns the intended consumer.

Timing also matters. The fishing constructor and login builder reseed themselves. A value installed before either reseed is discarded. Login reseeds directly before consuming its random values, while fishing can be made deterministic by replacing the seed after construction and before its next update.

Use the function RVA and verify the executable fingerprint before calling into the client. The static addresses, RVAs, seed sites, and call-site inventory are retained in [`randomness.yaml`](../../analysis/exports/randomness.yaml).

The secure packet path has no corresponding client seed to overwrite. Controlling it would require replacing or intercepting the secure-random call or its output, which is a different and much broader change than setting `crt_srand`.

## Known limits

This is a static call-site inventory. Indirect calls to `crt_rand` would not appear in the direct cross-references, although no indirect wrapper has been identified. Several visual-effect helpers are behaviorally bounded but still unnamed, so their exact on-screen owners remain open.
