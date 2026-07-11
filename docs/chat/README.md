# Chat and message display

The client has three separate receive-side text paths:

- [Speech balloons and message routing](receive-and-display.md) covers `SSay`, `SMessage`, object balloons, colored overlay text, look popups, and the separate score pane.
- [Chat input and outgoing packets](input-and-send.md) covers public say, shout, tell or whisper input, and the recovered `CSay` and `CTell` bodies.

The internal class names are useful here. `World::BalloonPane` is attached to a world object. `GameMessagePane` is a colored on-screen message overlay. `WindowMessageDialogPane` is the panel opened by several `SMessage` variants, including look results. `ScorePane` is a separate text target used only by `SMessage` type `0x12` in the recovered router.

Static analysis confirms the public say and shout paths. It does not yet assign the exact `SMessage` subtype numbers used for private tells, guild messages, and world messages. Those subtypes share the same display routines and contain no channel-name strings. A sanitized runtime capture of one message from each channel will resolve the remaining mapping.
