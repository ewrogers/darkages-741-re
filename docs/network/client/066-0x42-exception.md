# Exception (`CException`)

`CException` sends length-prefixed diagnostic text. It has two confirmed sources: a saved `LCrash.nfo` address trace and a live client-side clock-consistency report.

| Item | Value |
| --- | --- |
| Direction | Client to server |
| Opcode | `0x42` |
| Transform | `static` |
| Name provenance | Project-owner protocol vocabulary, confirmed by both local builders |
| Owner | Application crash reporting and main-loop clock consistency |

## Body

```text
packet CException {
    u8 opcode                    // 0x42
    u8 report_kind               // 1 in both local builders
    u16 report_length
    bytes report[report_length]
    u8 report_terminator         // 0, written explicitly by the builder
    u8 terminator                // 0, appended by net_submit_client_packet
}
```

`report_length` counts only the bytes in `report`. The first trailing zero is part of the builder's submitted body. The common submission layer appends a second transmitted zero before applying the static transform.

For example, report text `ABC` produces this complete plaintext body:

```text
42 01 00 03 41 42 43 00 00
```

No local builder emits another `report_kind`.

## Saved crash report

The client-wide unhandled-exception filter writes [`LCrash.nfo`](../../application/crash-reporting.md) in the process working directory. The file contains one build/distribution line and raw `CS:EIP` stack frames from DbgHelp `StackWalk`.

The file is not sent from the exception filter. The world-session `STransferServer` handler attempts the upload after reconnecting and sending `CTransferServer`. It reads at most 4096 text bytes, sends them as report kind `1`, closes the file, and calls `DeleteFileA`.

Deletion occurs after the attempt even when the report could not be opened, contained no bytes, or could not be submitted. A saved trace is therefore one-shot. The main-menu server-transfer handler has no call to this uploader.

## Live speed-check report

The second builder accepts an in-memory string whose length is from 1 through 4095 bytes. The application main loop reaches it from a local clock comparison that samples about every 100 ms. After repeated disagreements greater than five seconds, it sends a one-per-process report beginning with `SpeedHack` and containing the sampled clock values and client OS description.

This does not create or consume `LCrash.nfo`. It also does not depend on the server-driven [`SCheckTime`](../server/104-0x68-check-time.md) request.

## Limits

- `LCrash.nfo` can be built in an 8192-byte trace buffer, but the uploader reads only its first 4096 bytes.
- Text mode can apply normal Windows CRT newline translation.
- The stock report contains raw addresses, not function names or a minidump.
- There is no confirmed server acknowledgement packet for `CException`.
