# Event proxy skeleton

This is a C99-style architecture example for a 32-bit DLL loaded into the matching client. It is intentionally missing the detour backend and controller. It does not modify `Darkages.exe` on disk.

The skeleton demonstrates:

- guarded RVA resolution for the verified executable
- hooks for central event dispatch, plaintext client packet submission, and the main-thread dispatcher tick
- a local allow, observe, or block rule table
- a bounded main-thread command queue
- a duplex, local-only named pipe
- native construction of pointer, keyboard, text, and common IME events
- plaintext client-packet submission and decoded server-packet emulation

Use a tested x86 trampoline implementation behind `detour_backend.h`. A five-byte jump writer without instruction decoding is not sufficient because a trampoline must relocate complete overwritten instructions.

## Build boundary

Build this as a 32-bit Windows DLL. The compiler must support Microsoft `__thiscall` and `__fastcall`, because the target is 32-bit MSVC-style code. The launcher should verify the target SHA-256 before loading the DLL. The DLL separately verifies known hook prologues before installing detours.

The named pipe is:

```text
\\.\pipe\darkages-event-proxy-<process-id>
```

Each pipe message is one `proxy_message_header` followed by exactly `payload_size` bytes. Persistent controller configuration may use `rules.example.yaml`, but the IPC format is fixed binary so hooks never parse YAML.

## Construction examples

The controller fills the matching structure from `proxy_protocol.h`:

- Pointer move: `PROXY_COMMAND_POINTER` plus `proxy_pointer_payload` with `action = PROXY_POINTER_MOVE`, coordinates, and a Win32 message time.
- Click: send a pointer move first, then a left or right down command. Button producers use the coordinates already stored in `EventMan` and retain the client's double-click logic.
- Key: `PROXY_COMMAND_KEY` with a scan code, virtual-key value, composition state, and message time. The client updates its own modifier and held-key tables.
- Character: `PROXY_COMMAND_TEXT` with `PROXY_TEXT_CHARACTER` and one byte.
- Committed text: `PROXY_COMMAND_TEXT` with `PROXY_TEXT_COMMITTED` and at most `0x7F` bytes. The native producer copies the bytes into its `Event`.
- Application or IME state: `PROXY_COMMAND_APPLICATION` for open-status, composition start, composition end, or candidate-list close.
- Client packet: `PROXY_COMMAND_CLIENT_PACKET` with an opcode-first plaintext body. The normal send path adds framing and transformation.
- Server packet: `PROXY_COMMAND_SERVER_PACKET` with an opcode-first decoded body. The native receive-event producer allocates client-owned storage before normal parsing and pane dispatch.

Candidate-list data is deliberately absent. Type `0x10` contains pointers with special cleanup behavior, so it should only be created through the real Win32 IME path until its ownership contract is completely modeled.

## Safety properties

The pipe thread never invokes client code. It validates messages and copies them into a bounded queue. The tick hook executes at most 32 commands per client iteration. Event and send hooks never wait for IPC, allocate packet storage, or parse configuration. Telemetry is dropped when its bounded queue is full.

Rules are enforced inside the client. Disconnecting the controller does not pause the client. Defaults are fail-open. Synthetic traffic passes through rules unless the command explicitly sets `PROXY_FLAG_BYPASS_RULES`.

Decoded server injection is appropriate for testing packet handlers and UI behavior. It does not advance the receive cipher, transport sequence, or handshake state. Client-packet injection does use the live downstream send path and can therefore affect the active session sequence.

Call the exported `event_proxy_stop` and allow it to return before unloading the DLL with `FreeLibrary`. `DllMain` never waits during detach because waiting under the loader lock can deadlock.
