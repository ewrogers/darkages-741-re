# Appendices

The appendices hold exact lookup material that supports the main book without interrupting its explanations. Use them when you need a function address, runtime patch definition, object layout, pane inheritance detail, or UI layout mapping.

## Choose a reference

| Question | Start with | Check it against |
| --- | --- | --- |
| I have a function name, static address, or RVA. Where is its evidence? | [Function lookup](functions.md#function-lookup-heading) | The selected entry's source records and any [identity warning](functions.md#identity-warnings) |
| Where is a named event function, and what does its object contain? | [Event functions](functions.md#events) | The [event object layout](runtime/panes.md#event-object) and [delivery explanation](../systems/events.md#dispatch-flow) |
| Where is live character, map, or UI state? | [Runtime state walking](runtime/state-walking.md) | The owner-specific [structure groups](runtime-structures.md#structure-groups) |
| Which class loads a named UI layout? | [UI layout registry](ui-layout-registry.md) | [Pane types](pane-types.md) for inheritance and [UI layouts](../systems/ui-layouts.md) for the name contract |
| What changes does a documented runtime patch make? | [Runtime patches](runtime-patches.md) | The selected patch's original bytes, replacement bytes, and [safe launcher workflow](runtime-patches/safe-launcher.md) |

An address or class name alone does not explain behavior. Follow the matching chapter for the flow and [the evidence method](../methodology.md#source-of-truth) when checking a finding in the target client.

## Read next

- [Function reference](functions.md) provides exact name/address lookup and subsystem tables with links to every source record.
- [Runtime structures](runtime-structures.md) leads to object layouts, state walking, and native action contracts.
- [Pane types and inheritance](pane-types.md) records class relationships.
- [UI layout registry](ui-layout-registry.md) maps layout assets to their pane owners.
- [Player rendering evidence](player-rendering.md) records equipment ordering, sprite anchors, walk tables, and effect geometry.
- [Executable-page integrity records](executable-page-integrity.md) documents the image-page checks.
- [Runtime patches](runtime-patches.md) leads to patch definitions and the shared launcher procedure.
