# Distribution markers

The client still contains startup support for several regional and Korean ISP distributions. In this exact 7.41 executable, that support is dormant. The active selector always returns USA mode 1, whether or not a marker file is present.

## Active behavior

`app_get_distribution_mode` asks `app_select_distribution_mode` for a mode and caches it in the configuration object. The selector is only a constant return:

```c
u8 app_select_distribution_mode(void)
{
    return 1;
}
```

Mode 1 calls `net_configure_default_endpoint`, which prepares the normal `da0.kru.com` connection described in [Configuration](configuration.md). The local presence of `usa.nfo` does not cause this choice. It happens because the executable was compiled to return 1.

## Dormant marker scanner

`app_detect_distribution_mode_from_markers` contains the older file-based selection logic, but it has no code or data references in this executable. If another build called it, it would check markers in this order:

1. `usa.nfo`
2. `singapore.nfo`
3. an archived `taiwan.nfo` entry
4. `japan.nfo`
5. Korean ISP marker files

Most markers are presence tests. Japan is different. Its loose marker contains an `isp : %d` value, and an obfuscated `japan2.nfo` archive entry can supply a matching line of additional configuration text.

The matching local installation contains a zero-byte `usa.nfo`. That agrees with the code: the USA check only opens the file and closes it. It does not read a body.

## Compiled modes

The configuration constructor still has a switch for every returned mode. These paths show that the markers selected complete distribution integrations, not just a language or text encoding.

| Mode | Marker or label | Compiled behavior |
| ---: | --- | --- |
| 0 | none | Generic server-table path. |
| 1 | `usa.nfo` | Normal USA endpoint setup. This is the active mode. |
| 2 | `Unitel.nfo` | Empty initializer in this executable. |
| 3 | `LG.nfo` | Loads `chigamec.dll` and calls `WaitForSessionParameter` for connection data. |
| 4 | `SK.nfo` | Parses launcher data and uses a Netsgo-specific integration. |
| 5 | none found | No configuration handler. |
| 6 | `Thrunet.nfo` | Parses launcher or file data and uses `thrunet.clsURLCHK`. |
| 7 | `GameOK.nfo` | Expects a `/GameOK` launcher form and derives connection data from it. |
| 8 | `Bixel.nfo` | Loads `PrxyAuth.dll` and expects Bixel launcher data. |
| 9 | `mihosoft.nfo` | Loads `cjconnector.dll` and expects a `mihosoft` launcher record. |
| 10 | `Excitegame.nfo` | Uses an external launcher or COM-style source for endpoint data. |
| 11 | `KornetWorld.nfo` | Expects `/KWG`, resolves `game.kornetworld.com`, and selects port 9000. |
| 12 | none found | Sets connection flags but does not install an endpoint. |
| 13 | `japan.nfo` | Uses a fixed compiled IPv4 address and port 3460 unless a positional override succeeds. |
| 14 | archived `taiwan.nfo` | Loads `iplookup.tbl` or archived lookup data, then resolves the selected host. |
| 15 | `singapore.nfo` | Uses a fixed compiled IPv4 address and port 2610 unless a positional override succeeds. |

The Japan and Singapore initializers store four compiled address bytes directly. They correspond to `4.216.215.61` and `130.228.172.202` respectively. These are historical values in dormant code, not claims about current services.

The dormant ISP paths retain two distinct integration styles. Exact RTTI `UnitelPane` accepts an ampersand-delimited host, port, and identifier message, resolves the host, and writes the result into `Config`. The Thrunet and ExciteGame paths instead create registered COM services, exchange `BSTR` values, and recover endpoint fields through small COM-call wrappers. These paths are evidence of the old distribution integrations, but the hardcoded mode-1 selector does not construct them.

## Language selected by the distribution

The distribution choice also feeds a smaller four-value language selector. The default mode is Korean, modes 1 through 12 are English, mode 13 is Japanese, mode 14 is Taiwan, and mode 15 returns to English.

That selector chooses the bitmap font entry and retained message label. Korean records code page 949, Japanese records 932, and the other modes use the system ANSI environment. The complete drawing and asset behavior is in [Text and fonts](../rendering/text.md).

## What the markers do not control

The marker scanner does not select `ESC C` versus `ESC S` network framing. That choice comes from the server greeting after a connection is made. The printable frame is a transport encoding for normal opcode-first packet bodies, not a regional character encoding.

The compiled integrations strongly suggest a shared engine prepared for multiple publishers and access services. Their exact deployment history is outside what this client alone can confirm.
