# Function reference

Use this reference to find a named function, check its static address, and follow the evidence back to its source export. Functions are grouped by the existing subsystem prefixes; a group is a lookup aid, not proof of ownership.

The book's general search finds explanations and packet names. The lookup below covers every exported function name and address, including entries that are not mentioned in a chapter. The complete tables remain available under [Browse by subsystem](#browse-by-subsystem), including when JavaScript is unavailable.

<section id="function-lookup" aria-labelledby="function-lookup-heading">
<h2 id="function-lookup-heading">Find a function</h2>
<label for="function-query">Project name, static address, or RVA</label>
<input id="function-query" type="search" disabled placeholder="event_dispatcher_tick, 0x00401000, or rva:0x1000" aria-describedby="function-lookup-help function-lookup-status" aria-controls="function-results" autocomplete="off" spellcheck="false">
<p id="function-lookup-help">Names match whole or partial text. Hexadecimal addresses may omit leading zeros. Prefix an RVA with <code>rva:</code>; an unprefixed address is a static address.</p>
<p id="function-lookup-status" role="status" aria-live="polite">The interactive lookup requires JavaScript. Browse the subsystem tables below to find the same entries.</p>
<div id="function-results"></div>
</section>

<script id="function-index" type="application/json">
{{#include ../../generated/function-reference/index.json}}
</script>

## Browse by subsystem

{{#include ../../generated/function-reference/overview.md}}

Each name/address entry has its own stable link. Every source record is preserved when several exports describe the same function, and each evidence statement links to its YAML record. The export remains the source for the complete signature, range, and provenance when those fields are available.

## Addresses and target

A **static address** is the address shown by Binary Ninja at the preferred image base. An **RVA** is its distance from that base. The lookup calculates `RVA = static address - 0x00400000`. At runtime, use the loaded module base plus the RVA; the static address is not a guaranteed process address.

```text
File: Darkages.exe
Size: 3,112,960 bytes
SHA-256: 054a5d6adc56099c6bfd9d2a58675aff62dc788b63209a3d906492f5b89e96c6
Reported version: 741
Architecture: 32-bit x86 Windows PE
Preferred image base: 0x00400000
```

Confidence labels come from the existing exports. A generated table does not establish a new finding or prove that a reconstructed name is complete. See [the evidence method](../methodology.md#source-of-truth) and [export policy](../../analysis/exports/README.md).

## Identity warnings

{{#include ../../generated/function-reference/identity-warnings.md}}
