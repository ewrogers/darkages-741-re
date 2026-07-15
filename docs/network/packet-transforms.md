# Packet transforms

The common packet transform is an XOR pipeline with three policies: raw, static-key, and derived-key. The opcode chooses the policy, and the client-to-server and server-to-client opcode sets are different.

The project owner identified the two transformed modes as the older static-key form and the newer MD5-derived form. Binary Ninja confirms both modes, the default static key, the 9-byte derived key, the MD5 salt construction, and the separate 256-entry seed table.

All addresses are static virtual addresses for preferred image base `0x00400000`.

## Terminology

| Term | Meaning |
| --- | --- |
| Static key | Runtime-replaceable byte string used by transform mode 0. The default initialization produces a 9-byte key, but `net_set_static_key` stores an explicit runtime length. |
| Derived key | A 9-byte per-packet key used by transform mode 1. |
| MD5 salt source | A 1024-byte string built by repeated lowercase MD5-hex expansion. It supplies bytes for the derived key. |
| Seed XOR table | 256 repeated-byte `u32` values generated from one selector in the range 0 through 9. This is a second XOR layer, not the 9-byte key. |
| Rolling selector | One outbound byte incremented for each transformed packet. It selects a seed-table entry and affects block processing. |

Keeping these names separate matters. The 1024-byte MD5 salt source, the 9-byte key, and the 256-entry seed XOR table are three different objects.

## Direction-specific policy

### Client to server

| Policy | Opcodes |
| --- | --- |
| Raw | `0x00`, `0x10`, `0x48` |
| Static key | `0x02`, `0x03`, `0x04`, `0x0B`, `0x26`, `0x2D`, `0x3A`, `0x42`, `0x43`, `0x4B`, `0x57`, `0x62`, `0x68`, `0x71`, `0x73`, `0x7B` |
| Derived key | Every other opcode reaching `net_send_client_packet` |

### Server to client

| Policy | Opcodes |
| --- | --- |
| Raw | `0x00`, `0x03`, `0x40` |
| Static key | `0x01`, `0x02`, `0x0A`, `0x56`, `0x60`, `0x62`, `0x66`, `0x6F` |
| Derived key | Every other opcode reaching `net_receive_frames` |

These tables are transport policy, not proof that every listed opcode has a registered packet class or a recovered builder.

## Default static key

`net_socket_ctor` at `0x00563910` starts with the readable string `UrkcnItnI`, changes bytes 3 and 7, measures the nine-byte result, and copies that result four times into `net_static_key_expanded`.

The actual working default key is:

```text
55 72 6B E5 6E 49 74 A3 49
 U  r  k  .  n  I  t  .  I
```

The writes are at `0x005639C9` for byte 7 and `0x005639E9` for byte 3. The constructor restores the readable source buffer after the expanded copy, so inspecting `net_static_key_bytes` later can misleadingly show `UrkcnItnI`. The expanded buffer retains the working bytes shown above until the server replaces the key.

## Derived 9-byte key

`net_build_md5_salt_source` at `0x005684B0` expands the active character name into the 1024-byte MD5 salt source. `net_send_login_request` at `0x004BAA80` stores the submitted login name in `session_character_name` at `0x0073D910`. The session setup path passes that same global to the salt-source builder at `0x004B77A8`. This confirms the project owner's protocol knowledge that the character name is the seed. The underlying hash functions use the standard MD5 state constants.

`net_derive_packet_key` at `0x00568540` derives nine bytes from a 16-bit seed, an 8-bit seed, and that source:

```c
for (i = 0; i < 9; i++) {
    index = (seed16 + (seed8 * seed8 + i * 9) * i) % 1024;
    key[i] = md5_salt_source[index];
}
```

The routine copies those nine bytes four times into an expanded buffer so the common 32-bit XOR engine can cycle through the key without reading beyond it.

## Seed XOR table

`net_build_seed_xor_table` at `0x00568650` accepts selectors `0` through `9`. Each selector defines a deterministic byte mapping for input index `i` from `0` through `255`. Some mappings contain duplicate values, so they are not all permutations.

In the formulas below, casts to `u8` wrap modulo 256. Signed division uses C99 behavior and truncates toward zero.

| Selector | Result byte `b` | Shape |
| ---: | --- | --- |
| 0 | `i` | identity |
| 1 | `0x80 + ((i & 1) ? -((i + 1) / 2) : ((i + 1) / 2))` | center-out from 128 |
| 2 | `0xFF - i` | reverse |
| 3 | `0x80 + ((i & 1) ? -((0xFF - i) / 2) : ((0xFF - i) / 2))` | outside-in toward 128 |
| 4 | `(i / 16) * (i / 16)` | sixteen-value bands squared |
| 5 | `(u8)(i * 2)` | doubled modulo 256 |
| 6 | `0xFF - (u8)(i * 2)` | inverted doubled value |
| 7 | `i <= 0x7F ? 0xFF - 2 * i : 2 * i - 0x100` | descending odds, then ascending evens |
| 8 | `i <= 0x7F ? 2 * i : 0x1FF - 2 * i` | ascending evens, then descending odds |
| 9 | `0xFF - (u8)(((i - 0x80) / 8) * ((i - 0x80) / 8))` | inverted square of signed distance bands |

Every result byte is expanded to a repeated-byte word:

```text
b -> 0xBBBBBBBB
```

The transformed payload passes through the selected whole-packet table entry and additional block-index entries. Decryption applies the same XOR operations in reverse order.

The executable's initial `net_seed_xor_table` at `0x006D11E0` is selector 0, the identity mapping. Selector 0 is therefore the compiled default. It is not a fixed session choice because the server can replace it during bootstrap. Selectors outside `0` through `9` reach an undefined path in the client and must be rejected by compatible implementations.

## Outbound transformed body

`net_encrypt_client_packet` at `0x00567FB0` produces:

```text
opcode:u8
rolling_selector:u8
encrypted_payload:bytes
md5_selection:4 bytes
encoded_seed_material:3 bytes
```

The MD5 is computed over the opcode, selector, and transformed payload. Digest bytes `13`, `3`, `11`, and `7` are appended. Three direction-specific masked seed bytes follow. A transformed outbound body is eight bytes longer than its plaintext opcode-first body.

Opcodes `0x39` and `0x3A` also receive a separate randomized CRC-bearing wrapper in `net_submit_client_packet` before this common transform. That wrapper is packet-specific framing and should not be confused with the common MD5 trailer.

## Inbound transformed body

`net_decrypt_server_packet` at `0x00567DE0` preserves the opcode, reads the selector, recovers two seed values from the final three bytes, derives the mode-1 key when needed, and reverses the seed-table and key XOR passes.

The decoded opcode-first body is four bytes shorter than the transformed server body. The server direction does not use the same four selected MD5 bytes appended by the client direction.

## Negotiated state

Raw server opcode `0x00` (`SVersionCheck`), subtype `0`, installs both values through `net_handle_version_check` at `0x004B7F80`:

```text
offset  size  field
0       1     opcode = 0x00
1       1     subtype = 0
2       4     configuration_crc:u32be
6       1     seed_table_selector:u8
7       1     static_key_length:u8
8       n     static_key[static_key_length]
```

The handler queues the selector at `0x004B8038` and the replacement key at `0x004B806A`. The socket path later calls `net_build_seed_xor_table` and `net_set_static_key`. The selector observed in a live session therefore depends on the server. A capture should record the active key, seed selector, direction, opcode, and rolling selector together.
