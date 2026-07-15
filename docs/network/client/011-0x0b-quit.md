# Quit (`CQuit`)

| Field | Value |
| --- | --- |
| Direction | Client to server |
| Opcode | `0x0B` (11) |
| Common transform | static |
| Representative builder | `0x004B79C0` |
| Name provenance | The class name comes from related class vocabulary matched to the locally confirmed builder behavior. |

## Current evidence

The representative builder at `0x004B79C0` writes opcode `0x0B` as body byte 0 and reaches `net_submit_client_packet`.

No concrete derived client packet RTTI class exists in this binary. The display name is therefore kept separate from the locally verified opcode evidence.

## Known send sites

- `0x4B7578` in `sub_4b7520`, reachable from `Pane::MainMenuPane`.
- `0x4B7B6B` in `sub_4b7b40`; nearest RTTI owner not yet identified.
- `0x4BC9C0` in `sub_4bc9b0`, reachable from `DialogPane::AgreementDialogPane`.

## Plaintext body

```text
opcode:u8
... fields pending
```

Field order, variants, state effects, and paired packets remain to be traced.
