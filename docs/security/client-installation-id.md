# Client installation identifier

The client creates a random 32-bit installation identifier, derives a related 16-bit check value, and stores both under disguised `CLSID` registry values. `CLoginPacket` sends obfuscated forms of both values plus a random nonce and integrity value.

The registry values are installation fingerprints. They are not the `SBadGuy` kill-switch flag, which is based on marker-file existence.

## Initialization

`config_init_dark_ages_endpoint_and_install_ids` at `0x433380` runs during Dark Ages client configuration.

The routine seeds `rand()` with `time(NULL)` before creating either value.

| Registry location | Type | Meaning | Runtime field |
|---|---|---|---|
| `HKCR\NXKRI.Ctrl.1\CLSID` | `REG_DWORD` | Primary random 32-bit installation ID | `config + 0x424` |
| `HKCR\KRIHC.Ctrl.1\CLSID` | `REG_DWORD` | Packed and obfuscated derivative | decoded to `config + 0x428` |

For each query, the client accepts a value only when `RegQueryValueExA` succeeds, the type is `REG_DWORD`, and the value is nonzero.

If the primary value is missing or invalid, the client calls `rand()` four times and combines the low byte from each call into one 32-bit value:

```c
primary_id  = (u32)(rand() & 0xFF) << 24;
primary_id |= (u32)(rand() & 0xFF) << 16;
primary_id |= (u32)(rand() & 0xFF) << 8;
primary_id |= (u32)(rand() & 0xFF);
```

It writes that value to `NXKRI.Ctrl.1\CLSID` and queries it again.

If the primary key cannot be opened or remains invalid after writing, the client uses fallback primary value `0xFF00FF00` for that process.

## Derived 16-bit value

`config_derive_install_id_checksum16` at `0x436E10` processes the primary ID's four little-endian bytes. It starts at zero and uses a 256-entry table built from polynomial `0x1021`:

```c
u16 derive_install_id_checksum16(u32 install_id)
{
    const u8 *p = (const u8 *)&install_id;
    u16 sum = 0;
    int i;

    for (i = 0; i < 4; ++i) {
        sum = (u16)((sum << 8) ^ table[sum >> 8] ^ p[i]);
    }

    return sum;
}
```

This uses a CRC-style `0x1021` table, but its byte is XORed after the table lookup. It is not the conventional CRC-16/CCITT table-index formula. Implementations should preserve the recurrence exactly.

## Secondary registry encoding

When `KRIHC.Ctrl.1\CLSID` is missing or invalid, the client packs the derived value with two random padding bytes:

```text
bits 31..24  random byte
bits 23..16  derived high byte
bits 15..8   random byte
bits 7..0    derived low byte
```

It then XORs the packed DWORD's four little-endian memory bytes with `0xAC`, `0xAD`, `0xAE`, and `0xAF`, respectively, before writing the registry value.

When reading an existing value, the client repeats those four XOR operations and extracts bits `23..16` and `7..0` as the runtime 16-bit value.

If the secondary value remains invalid after an attempted write, the client keeps the freshly derived 16-bit value in memory for that process.

The client checks registry API success, type, and nonzero value. It does not compare an existing decoded secondary value with a freshly derived value. A server can perform that relationship check after recovering both values from `CLoginPacket`, but server-side validation is not visible in this binary.

## CLoginPacket encoding

`net_send_c_login` at `0x4BAA80` builds the following plaintext body before the normal packet transform:

```text
u8       opcode                    0x03
u8       character_name_length
u8[]     character_name
u8       password_length
u8[]     password
u8       random_1
u8       encoded_random_2
u32be    encoded_primary_id
u16be    encoded_derived_id
u32be    encoded_nonce
u16be    encoded_checksum
u8       constant_1                1
u8       constant_0                0
```

The installation block begins at `random_1` and is 16 bytes long. The first 12 bytes end with `encoded_nonce`; the checksum covers those 12 encoded bytes.

The builder generates two random bytes:

```c
r1 = rand() & 0xFF;
r2 = rand() & 0xFF;

encoded_random_2 = ((r1 + 0x3B) & 0xFF) ^ r2;
```

The server can recover `r2` from the first two fields:

```c
r2 = encoded_random_2 ^ ((r1 + 0x3B) & 0xFF);
```

The primary and derived identifiers are XORed byte by byte in little-endian local memory before being written in big-endian wire order:

```c
for (i = 0; i < 4; ++i) {
    primary_byte[i] ^= (u8)(r2 + 0x8A + i);
}

for (i = 0; i < 2; ++i) {
    derived_byte[i] ^= (u8)(r2 + 0x5E + i);
}
```

The nonce is assembled from four more `rand()` low bytes. Its four little-endian memory bytes are XORed with `(r2 + 0x73 + i) & 0xFF` before transmission.

`net_calculate_c_login_checksum16` at `0x4BCAD0` applies the same custom `0x1021` recurrence to the 12 encoded bytes. The checksum's two little-endian memory bytes are then XORed with `(r2 + 0xA5) & 0xFF` and `(r2 + 0xA6) & 0xFF`, followed by a `u16be` write.

## Likely server checks

The client-side layout supports these server operations:

1. Recover `r2` from `random_1` and `encoded_random_2`.
2. Undo the identifier, nonce, and checksum XOR masks.
3. Recalculate the 12-byte integrity value.
4. Derive the 16-bit value from the recovered primary ID and compare it with the recovered secondary ID.

Steps 1 through 3 are direct inverses of local encoding. Step 4 is a strong design inference, not a client-side server implementation.
