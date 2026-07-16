# Checksums

The client uses one custom CRC16 update and the standard IEEE CRC32. They are not interchangeable.

## Custom CRC16

The 256-entry table is generated with polynomial `0x1021`. The running value starts at zero and has no final XOR. Unlike CRC-16/XMODEM, the input byte is XORed after the table lookup instead of being part of the table index.

```text
crc16_update(byte, crc):
    index = crc >> 8
    return table[index] XOR ((crc << 8) AND 0xFFFF) XOR byte

crc16(bytes):
    crc = 0
    for byte in bytes:
        crc = crc16_update(byte, crc)
    return crc
```

The check value for ASCII `123456789` is `0xBEEF`. This is a useful way to catch an accidental replacement with a standard library CRC16.

Known uses include dialog data, six bytes per map cell, and the request challenge response. Multi-byte values in those call sites are fed low byte first, then high byte. The response packet writes the final result as `u16be`.

## IEEE CRC32

CRC32 uses reflected polynomial `0xEDB88320`, initial inversion, and final inversion. It matches common zlib and standard library CRC32 functions.

```text
crc32_update(crc, bytes):
    crc = NOT crc
    for byte in bytes:
        crc = table[(crc XOR byte) AND 0xFF] XOR (crc >> 8)
    return NOT crc
```

The check value for ASCII `123456789` is `0xCBF43926`.

CRC32 covers inflated metadata bytes, decoded server greeting text, and other version or integrity checks. The checksum detects damage or stale data. It is not encryption or authentication.

## Evidence

- `crc16_update` at `0x005B8F30`
- `crc16_buffer` at `0x00568870`
- `map_update_crc16` at `0x005B9180`
- CRC16 tables at `0x006D15E8` and `0x006D2D98`
- `crc32_update` at `0x00604530`
- CRC32 table at `0x0068C884`
