# 000 / 0x00: Version (`CVersion`)

- Direction: client to server
- Internal name: `CVersion`
- Local behavioral alias: `Version`
- Related-game enum name: `Version`
- Name provenance: Leaked company/engine class name corroborated by this client's opcode and local behavior.
- Evidence: concrete builder at `sub_579090` (`0x57993F` packet-build block)
- Send handling: no common encryption transform
- Wire frame after transformation: `0xAA, u16be body_size, body`

## Builder call sites

- `sub_579090` at `0x579090`; the CVersion build begins at `0x57993F` and is submitted at `0x5799E7`.

## Current structural notes

- The protocol version is hardcoded indirectly as the decorated ASCII string `"7D4E--1K"` at `0x579857`.
- The client copies only decimal digits from that string, producing `"741"`, calls `atoi`, and stores the result in `net_client_protocol_version` at `0x7505B8`.
- `741` is `0x02E5`; it is written big-endian.
- The executable's PE metadata reports file/product version `7.4.1.0`, but this packet builder does not query version resources. The matching digits are embedded directly in the code.
- `Darkages.cfg` contains `Version: 9728` (`0x2600`), but that is independently proven to be the settings-file schema revision used by `config_write_settings_file` and `config_read_settings_file`; it does not feed this packet.
- The same global is formatted elsewhere as `Version %1d.%02d`, so `741` appears in the UI as `Version 7.41`.

## Recovered untransformed body

| Offset | Type | Value / meaning |
|---:|---|---|
| `0` | `u8` | opcode `0x00` |
| `1` | `u16be` | protocol version `741` (`0x02E5`) |
| `3` | `u8` | literal `0x4C` (`'L'`), probably part of an SKU/variant marker (user hypothesis) |
| `4` | `u8` | literal `0x4B` (`'K'`), probably part of an SKU/variant marker (user hypothesis) |
| `5` | `u8` | NUL sentinel appended by `net_submit_client_packet` |

The resulting raw body is `00 02 E5 4C 4B 00`. Because opcode `0x00` bypasses the common transform, the framed wire bytes are `AA 00 06 00 02 E5 4C 4B 00`.

Immediately before CVersion, the same connection path submits a separate opcode-`0x62` body whose bytes spell `62 61 72 61 6D` (`0x62` followed by `"aram"`). `"baram"` is believed to be the client's codename. The producer then explicitly resets the outgoing encrypted-packet sequence to `0` before it queues CVersion. CVersion is raw and does not consume a sequence byte; see [Client packet send pipeline](../../client/network-send.md#outgoing-sequence-reset-and-the-pre-version-handshake) for the asynchronous ordering caveat.
