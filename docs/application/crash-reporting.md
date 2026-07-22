# Crash reporting

The client installs one application-wide Windows unhandled-exception filter during startup. If an exception reaches that top-level filter, the client writes a small text file named `LCrash.nfo`. It does not create a Windows minidump.

The saved report is not uploaded while the process is crashing. A later in-world server transfer attempts to send it through [`CException`](../network/client/066-0x42-exception.md), then deletes the file.

```text
startup
  -> SetUnhandledExceptionFilter
  -> unhandled Win32 exception
  -> StackWalk over the supplied x86 CONTEXT
  -> write LCrash.nfo
  -> chain to the previous top-level filter

later in-world STransferServer
  -> reconnect and send CTransferServer
  -> read at most 4096 bytes from LCrash.nfo
  -> send CException
  -> delete LCrash.nfo
```

## Exception-handler lifetime

Exact RTTI class `ExceptionHandler` is constructed early in application initialization, immediately after the memory manager. Its constructor calls `SetUnhandledExceptionFilter`, retains the previous filter pointer, registers `app_unhandled_exception_filter`, and publishes the application-wide singleton. Destruction clears that singleton after restoring the previous filter.

The filter receives the normal Win32 `EXCEPTION_POINTERS` pair. It writes the report, then calls the previous top-level filter when one was installed. Otherwise it returns `EXCEPTION_CONTINUE_SEARCH`. The `ExceptionHandler` destructor restores the previous filter.

This uses Windows structured exception handling at the process boundary. The many compiler-generated SEH frames around ordinary C++ functions are cleanup and language-exception machinery; they are not separate `LCrash.nfo` writers. The filename has only two references in the client: the report writer and the later uploader.

### Internal error objects

The client also has a small C++ `Error` hierarchy for ordinary runtime failures. This is separate from the top-level crash-file path. A process-wide bounded context stack contributes tags to each new `Error`, and the base object stores a fixed message that can be formatted into a caller buffer.

Exact RTTI `Win32Error`, `DDError`, and `DSError` retain an error code. Their formatters ask `FormatMessageA` for system text and fall back to the hexadecimal code. Exact RTTI `GeneralError` instead appends caller-supplied text. These objects explain how subsystems report recoverable Windows, DirectDraw, and DirectSound failures without implying that each one writes `LCrash.nfo`.

## File contents

`LCrash.nfo` is opened as text in the process working directory. The active writer produces a hardcoded build line followed by a raw stack walk:

```text
700.21.R <distribution>
<CS>:<EIP>
<CS>:<EIP>
...
```

The distribution selector is one character from `E`, `J`, `T`, `S`, or `K`. Only `J` is directly tied to the client's Japan distribution check. The `700`, `21`, and `R` values are crash-reporter build fields and do not match the normal protocol version value `741`.

The stack walker uses DbgHelp `StackWalk` for `IMAGE_FILE_MACHINE_I386`. It copies the crashing x86 `CONTEXT`, starts from its instruction, stack, and frame pointers, and formats each successful frame as `%04X:%08X`. The temporary trace buffer is 8192 bytes.

The executable also contains strings for exception codes, fault addresses, registers, and named exception values such as `ACCESS_VIOLATION`. The active writer resolves the exception name and faulting module section, but does not append either result to `LCrash.nfo`. Those strings appear to belong to a richer report form that is dormant or incomplete in this build.

There is no `MiniDumpWriteDump` import and no binary dump stream. This is a minimal address trace.

## Upload and deletion

Only the world-session `STransferServer` handler calls the saved-report uploader. The main-menu transfer handler does not. After reconnecting and sending `CTransferServer`, the world handler tries to open `LCrash.nfo` as text and reads at most 4096 bytes.

When bytes were read and both the exception-handler singleton and network connection exist, the client sends those bytes as `CException` report kind `1`. A report longer than 4096 bytes is therefore truncated even though the writer can build up to 8192 bytes.

The uploader calls `DeleteFileA` after the attempt regardless of whether opening, reading, or sending succeeded. The saved report is consequently one-shot and can be lost if that transfer occurs without a usable connection.

## Live speed-check report

`CException` has a second source that does not use `LCrash.nfo`. About every 100 ms, the main loop compares elapsed time from `timeGetTime`, `GetTickCount`, CRT time, and, when enabled, system `FILETIME`.

A disagreement greater than five seconds counts as a mismatch. After three earlier mismatches, the next mismatch builds text beginning with the split literal `SpeedHack`, followed by a key tag, four clock values, and an OS description. It sends that text once per process through the same `CException` report-kind-`1` builder.

This local check is separate from the server-driven [`SCheckTime`](../network/server/104-0x68-check-time.md) and [`CCheckTime`](../network/client/117-0x75-check-time.md) exchange. `CCheckTime` merely echoes the server value and samples `timeGetTime`; this main-loop path performs the client-side comparison.
