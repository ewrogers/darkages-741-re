# Local command dispatcher

The client contains a dormant text-command system for local scripted actions. A command line is split into a command name and typed arguments, then an RTTI-backed `CommandDispatcher` calls the matching handler. This is separate from ordinary chat commands and server packet dispatch.

Version 741 retains the parser, input pane, dispatcher, and default executor, but nothing in the executable constructs the dispatcher or the input pane. The compiled command chain is internally complete but has no confirmed entry point from a normal game screen.

## Flow

```text
CommandLineInputPane text
  -> tokenize quoted strings and bare words
  -> classify decimal-only arguments as integers
  -> push arguments in reverse order
  -> CommandDispatcher handler
  -> CommandExecutor or a direct client action
```

`CommandLineInputPane` copies at most 255 text bytes before parsing. The tokenizer accepts letters, digits, and underscore in bare words. Double quotes group a string containing separators. An unquoted token containing only decimal digits becomes an integer; other tokens remain strings.

The dispatcher owns a stack of at most 1,024 tagged arguments and a growable string arena. It pushes parsed arguments from last to first so each handler can pop them in source order. Every dispatch clears the temporary stack and string arena, including an unknown command or a handler that rejects an argument type.

## Command table

The literal names below are compiled into version 741. Types describe what the local handler requires, but several argument meanings remain unresolved.

| Command | Accepted argument types | Version 741 result |
| --- | --- | --- |
| `set_tile` | integer, string, string | Forwards to a default no-op executor method |
| `set_color` | integer, string, string | Forwards to a default no-op executor method |
| `effect` | integer, integer, string | Forwards to a default no-op executor method |
| `motion` | integer, integer, string | Forwards to a default no-op executor method |
| `move` | integer, string | Forwards to a default no-op executor method |
| `put_item` | four integers | Forwards to a default no-op executor method |
| `put_monster` | five integers | Forwards to a default no-op executor method |
| `put_human` | three integers, string | Forwards to a default no-op executor method |
| `human_to_monster` | two integers, string | Forwards to a default no-op executor method |
| `sound` | integer | Plays a sound effect when the sound manager exists |
| `auto_use_skill`, `aus` | none consumed | Accepted no-op |
| `set_attr_tracker`, `sat` | none consumed | Accepted no-op |
| `auto_move` | none consumed | Accepted no-op |
| `set_merchant_auto_answer` | none consumed | Accepted no-op |
| `set_timer` | none consumed | Accepted no-op |
| `wait_event` | none consumed | Accepted no-op |
| `message` | string | Appends white text and a newline to the game-message overlay |
| `auto_use_spell` | integer | Selects or cancels a timed executor action |
| `set_gnd_tile` | three integers | Forwards to a default no-op executor method |
| `set_stc_tile` | four integers | Forwards to a default no-op executor method |
| `play_minigame` | integer | Opens the selected minigame through the active root pane |
| `send_fieldmap` | three integers | Sends a nine-byte client packet beginning with opcode `0x3F` |
| `show` | string, integer | Forwards to a default no-op executor method |

The no-op result is confirmed for the default `CommandExecutor` constructed by `CommandDispatcher`. The dispatcher can also receive an external executor pointer, so an older or external owner could have supplied the missing world behavior. Version 741 contains no derived command-executor RTTI class and no caller that constructs the dispatcher with such an owner.

The default executor registers timer 1 at 500 ms and timer 2 at 2,000 ms. Its `auto_use_spell` handler schedules timer 3 at the supplied selector multiplied by 1,000 ms, while selector zero removes that timer. The timer callback confirms the scheduling paths, but the final timer-3 action remains absent in this default implementation.

## Reachability in version 741

The only producer for `command_parse_and_execute_line` is `CommandLineInputPane` submission. Submission itself is reached from that pane's keyboard handler. Direct-call and data-reference checks find no owner for either end of the chain:

- `CommandDispatcher` construction has no caller or stored function pointer.
- `CommandLineInputPane` construction has no caller or stored function pointer.
- No startup, terminal, login, or main-menu layout defines an Adventure or command-input control.
- No loose client asset contains the command vocabulary or a matching command script.

This is stronger than a hidden or inaccessible control. The activation owner is absent from this executable. Constructing the input pane through a runtime extension could expose the surviving commands, but most world-editing commands would still reach the default executor's no-op methods.

## The Adventure directory

The matching installer deliberately creates `adventure/` and copies one 308-byte `SpellBook.cfg` dated April 2004. The file is not a scenario script. It uses the same `SpellbookUsed`, spell-name, and ten-line mapping format that the live spellbook editor and spell-casting path read and write.

The client builds this local filename from the active session character:

```text
.\<character name>\SpellBook.cfg
```

The login sender supplies that character name during normal play. The executable contains no literal `adventure` path or mode name and no active path that selects `adventure` as a local character. The installed directory therefore resembles a leftover profile for an older pseudo-character or mode, but the file alone does not provide maps, scripts, NPC behavior, or an offline game loop.

The command vocabulary makes an older Adventure or internal scenario tool plausible, especially the object-placement and tile-editing commands. The local client does not prove that historical connection. In version 741, restoring one removed button would not restore a complete mode because the activation owner, useful executor implementation, and scenario source are all absent.

## Command history

The line-input pane keeps up to 256 command strings in a process-global history. Adding an existing string moves the old entry to the end instead of creating a duplicate. Keyboard events cycle through this list and copy the selected command back into the input field with a trailing space.

Static analysis confirms the parser and client-side handlers. No normal game screen exposes `CommandLineInputPane` in this build. The durable names and evidence are in [`command-dispatch.yaml`](../../analysis/exports/command-dispatch.yaml).
