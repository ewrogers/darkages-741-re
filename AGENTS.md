# Agent instructions

These instructions apply to the entire repository.

Read the [contributor handbook](CONTRIBUTING.md) before making changes. Its linked [authoring guide](contributing/authoring.md), [research policy](contributing/research-policy.md), and [analysis policy](analysis/README.md) contain repository instructions, not optional background. Follow the authoring rules for documentation work and the general evidence rules plus every applicable subsystem section for research. Use the handbook's workflow and validation command.

Keep these requirements in view:

- The matching version-741 binary is the source of truth. Verify the [target fingerprint](contributing/research-policy.md#project-goal) before binary research. Legacy material and outside implementations supply leads, not conclusions.
- Preserve unrelated user changes and contradictory evidence. Do not make uncertain behavior sound confirmed.
- Preserve exact packet direction, ownership, bounds, ordering, units, timing, and name provenance. Keep the detailed subsystem requirements in the research policy.
- Do not patch executable bytes unless the user explicitly asks to apply a patch. Analysis or documentation of a patch does not authorize applying it. Naming, typing, and commenting the local analysis database are normal work.
- Never commit or distribute private client binaries, game assets, `.bndb` files, credentials, character data, or unsanitized captures. Follow the handbook's [repository hygiene](CONTRIBUTING.md#repository-hygiene), including its reviewed sanitized-fixture exception.
- Update durable evidence and the matching documentation together when research changes a finding. Run the relevant validation and report its limits before finishing.
- Do not commit or push unless the user asks.

Maintain each rule in its canonical guide. Keep this file and `CLAUDE.md` as routing instructions, and keep dated audit notes out of the reader's chapter sequence.
