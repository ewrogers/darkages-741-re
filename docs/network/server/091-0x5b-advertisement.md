# Advertisement (`SAdvertisement`)

`SAdvertisement` records a command for a separate `ad.exe` program. It does not open an advertisement inside the client. The client waits until its game loop has ended and normal shutdown has finished, then tries to start `ad.exe` with four server-supplied arguments.

| Item | Value |
| --- | --- |
| Direction | Server to client |
| Command | `0x5B` (91) |
| Encoding | session key |
| Name provenance | Exact Microsoft C++ RTTI class `SAdvertisement` |
| Owner | `MainMenuPane` |
| Client response | None |

## Body

```text
packet SAdvertisement {
    u8 opcode                              // 0x5B
    u16 argument_length
    bytes argument[argument_length]
    u16 value_1
    u16 value_2
    u8 value_3
}
```

The three numeric fields are stored as nonnegative integers and later formatted in decimal. Their meanings inside `ad.exe` remain unknown because that separate executable is not present in the matching local installation.

## When it is handled

`net_dispatch_main_menu_events` routes this packet beside login, stipulation, server transfer, and browser messages. This makes it a front-end or login-session message, even though it uses the derived session-key transform. The in-game `WorldPane` dispatcher has no `0x5B` branch.

The most likely intended timing is during the login or server-transfer flow while `MainMenuPane` is still registered. The client does not prove the server's exact sending moment. A packet sent after the in-game pane has replaced the main menu can still be decoded into an `SAdvertisement` object, but there is no active in-game consumer for it.

## Deferred launch behavior

`net_handle_advertisement_server_packet` passes the fields to `app_set_post_exit_advertisement`. That function:

1. copies `argument_length` bytes into a 65,536-byte application buffer;
2. appends a local NUL byte;
3. stores the length and three numeric values; and
4. returns without changing the current UI or sending a packet.

The saved application state is compact:

```c
struct PostExitAdvertisementState {
    u8  argument[0x10000];
    u32 argument_length;       // +0x10000
    u32 value_1;               // +0x10004
    u32 value_2;               // +0x10008
    u32 value_3;               // +0x1000C
};
```

A later `SAdvertisement` replaces the pending values. A zero-length argument clears the launch gate because shutdown only continues when the saved length is greater than zero.

After the message loop ends, `app_winmain` calls the normal application shutdown first. It then builds this command line:

```text
ad.exe <argument> <value_1> <value_2> <value_3>
```

The format is exactly `ad.exe %s %d %d %d`. The string is not quoted or escaped. `CreateProcessA` receives `ad.exe` as the fixed application name, and the client ignores whether process creation succeeds. With no `ad.exe` beside the client, the test has no visible result.

## Safe plaintext test

This body saves `probe`, `1`, `2`, and `3`:

```text
5B 00 05 70 72 6F 62 65 00 01 00 02 03
```

If accepted while `MainMenuPane` is active, nothing appears immediately. Exit the entire client normally. The attempted command line is then:

```text
ad.exe probe 1 2 3
```

Use a short argument without spaces for testing. The body still needs the normal server-to-client derived transform, sequence, trailer, and outer frame for the current connection.

## Known limits

- The local installation does not include `ad.exe`, so the meanings of `value_1`, `value_2`, and `value_3` are unresolved.
- The client proves a post-exit launcher command, not the content or appearance of the advertisement program.
- No paired client packet exists.
