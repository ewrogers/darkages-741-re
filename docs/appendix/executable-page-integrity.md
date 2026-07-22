# Executable-page integrity records

The client can describe its executable code as a sequence of 4 KiB page addresses and 16-bit checksums. One writer is reached from `app_winmain`. A matching verifier exists but currently has no recovered caller.

## Record layout

Each native-memory record is six bytes:

```text
u32 page_address
u16 crc16
```

These values are written with the compiler's native 32-bit x86 representation. They are not a network packet schema. The table has no recovered count or terminator; its byte length determines how many complete six-byte records can be checked.

## Page selection

`integrity_find_executable_page_range` starts from the address of a compiled integrity routine and queries the current process with `VirtualQueryEx`. It advances in fixed `0x1000` steps, records the first executable page, and stops after the contiguous executable run ends.

`memory_is_executable_address` accepts committed pages whose protection includes `PAGE_EXECUTE`, `PAGE_EXECUTE_READ`, `PAGE_EXECUTE_READWRITE`, or `PAGE_EXECUTE_WRITECOPY`.

The writer calculates one CRC16 per page. The verifier first confirms that each stored address still belongs to committed executable memory, then recalculates the checksum across exactly `0x1000` bytes. Any address or checksum mismatch fails the table.

## CRC16 update

The checksum starts at zero and uses a 256-entry table:

```text
crc = table[(crc >> 8) * 2] ^ (crc << 8) ^ byte
```

The helper is distinct from the already named CRC16 implementation elsewhere in the client. A formal polynomial comparison has not yet been completed.

## Known limits

`integrity_verify_checksum_stream` reads at most `0x20000` bytes before checking records. The lower verifier stops when fewer than six bytes remain, so incomplete trailing bytes are ignored. No live caller for either verifier has been recovered, and the purpose of the table written by `app_winmain` remains unresolved. The export is [`integrity.yaml`](../../analysis/exports/integrity.yaml).
