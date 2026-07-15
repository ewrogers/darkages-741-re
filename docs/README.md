# Dark Ages 7.41 Reverse Engineering

This book documents an evidence-based Binary Ninja analysis of the Dark Ages client that reports version `741`.

Each chapter begins with direct evidence from the matching executable, inspected through Binary Ninja and Binary Ninja MCP. Reference material under `legacy/` may suggest where to look, but every result must be independently confirmed.

## Target

```text
File: Darkages.exe
Size: 3,112,960 bytes
SHA-256: 054A5D6ADC56099C6BFD9D2A58675AFF62DC788B63209A3D906492F5B89E96C6
Reported client version: 741
Architecture: 32-bit x86 Windows PE
```

Start with [Getting Started](getting-started.md), then read the [Analysis Method](methodology.md). Verified client analysis currently covers the [single-instance guard and intro videos](client/startup.md) plus [command-line behavior and the initial server connection](network/initial-connection.md).
