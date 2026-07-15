# Analysis Method

Lead with what the version-741 client does, then show how the code supports the conclusion.

## Evidence order

Use evidence in this order:

1. Static code and data from the matching executable in Binary Ninja
2. Runtime behavior or captures from the matching client
3. Legacy project material, used only to identify leads
4. Related games, leaked names, and external implementations, used only as attributed context

A lower-ranked source can help explain a result, but it cannot override the matching client.

## Working from Binary Ninja

Start from a concrete anchor such as an import, string, opcode comparison, cross-reference, vtable, packet reader call, or runtime address. Follow callers, callees, and relevant data references before assigning intent.

HLIL and Pseudo C make control flow easier to read, but they are reconstructions. Check important constants, field widths, signedness, stack cleanup, loop bounds, and branch conditions in MLIL, LLIL, or disassembly.

Use Binary Ninja user symbols, comments, and types for conclusions that should persist. When automation applies those changes, prefer user APIs rather than auto-analysis APIs.

## Recording a result

A useful function record includes its user symbol, static virtual address, role, callers or callees when relevant, inferred signature, confidence, and evidence. Documentation should distinguish static image addresses from ASLR-adjusted runtime addresses and allocated pointers.

Update three layers together when they exist:

1. Local Binary Ninja user symbols, comments, and types
2. Deterministic export data under `analysis/exports/`
3. Human-readable explanation under `docs/`

## Using the archive

Search `legacy/` when it can shorten discovery, but re-run the analysis from the binary. Do not use an old friendly name or packet layout as proof. If the new result agrees, cite only the new Binary Ninja evidence in the main conclusion and mention legacy provenance only when it adds useful context.

## Uncertainty

Keep unknown fields, alternate branches, and contradictory observations visible. Use `maybe_` names in Binary Ninja or a trailing `?` in prose when a tentative name is useful. Replace uncertainty only when new evidence supports it.
