# Game systems

The game systems turn window events, player input, assets, and server updates into the parts of Dark Ages that a player can see and use. Each page follows one focused mechanism so the UI, game state, and network behavior remain easy to distinguish.

## Choose a starting point

| Question | Start with | Then follow |
| --- | --- | --- |
| How does input reach a control? | [Event delivery](events.md#dispatch-flow) | [Pane state](ui.md#pane-state), then [dialog controls](ui.md#dialog-controls) |
| How does an NPC conversation work? | [NPC dialogs](npc-dialogs.md) | The separate [screen-menu and pursuit packet pairs](../network/README.md#npc-conversations) |
| How do assets become character art? | [Asset loading](asset-loading.md) | The [EPF reader](../file-formats/epf.md), then [player rendering](../rendering/players.md) |
| How can existing UI be repositioned or reskinned? | [UI layout files](ui-layouts.md) | [Native controls](ui-controls.md) and the [layout registry](../appendix/ui-layout-registry.md) |

The groups below cover the remaining systems. Rendering, audio, file formats, and networking have their own guides; a system page links to them where its flow crosses into those subjects.

## Shared foundations

Start with [Events](events.md) for dispatch, [UI and panes](ui.md) for registration and propagation, and [Native UI controls](ui-controls.md) for buttons and text fields. [UI layout files](ui-layouts.md) explains how named asset entries supply their geometry and art.

[Asset loading and lifetime](asset-loading.md) follows shared resources into each subsystem. [Random number generation](randomness.md) distinguishes the generators used by game code and packet encryption.

## Maps and player actions

- [Map loading](map-loading.md) follows local cache reuse and server row transfers.
- [Movement and swimming](movement-and-swimming.md) explains tile restrictions and swimming appearance.
- [World interactions](world-interactions.md) covers clicks on living objects and static map art.
- [Pathfinding and following](pathfinding-and-pursuit.md) covers local routes and pursuit.
- [Inventory drag actions](inventory-drag-actions.md) follows item and gold drops or transfers.
- [Skill and spell action delays](action-delays.md) explains local cooldown displays and input restrictions.
- [Fishing minigame](fishing.md) follows its simulation, hook collisions, and timing gauge.

## Dialogs and conversations

- [Player popup menu](player-popup-menu.md) and [Player exchange](player-exchange.md) cover interactions with other players.
- [Bulletin boards and mail](bulletin-and-mail.md) covers lists, message details, composition, and pagination.
- [Manufacturing manuals](manufacturing.md) follows recipe browsing and crafting requests.
- [NPC dialogs](npc-dialogs.md) explains screen menus and pursuit conversations; [NPC dialog illustrations](npc-dialog-illustrations.md) covers their larger speaker images.
- [Server message dialogs](message-dialogs.md) covers wrapped messages with optional art and actions.

## Character, settings, and text

- [Character creation](character-creation.md) and [Changing a password](change-password.md) follow the lobby account flows.
- [Game settings](game-settings.md) separates server-managed choices from local preferences.
- [Item and ability descriptions](item-and-ability-descriptions.md) and [Messages and history](messages-and-history.md) explain the different text displays.
- [Korean text input](korean-text-input.md) covers character composition; [Text color markup](text-color-markup.md) covers inline palette selection.
- [Screenshots and the photo album](screenshots-and-photo-album.md) separates window captures from rendered portraits. [Portraits and profiles](portraits-and-profiles.md) follows local storage and server-requested uploads.

## Local command interfaces

[Local command dispatcher](local-command-dispatcher.md) documents a dormant compiled interface. [Event proxy design](event-proxy.md) describes a proposed adapter for external commands and event observation. Its design status is separate from the client behavior established elsewhere in this section.

Continue with [Rendering](../rendering/README.md), [Audio](../audio/README.md), or [Network](../network/README.md) for the systems that draw, play, and exchange this state.
