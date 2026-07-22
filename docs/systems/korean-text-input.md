# Korean text input

The client contains its own Korean text composer inside the exact RTTI class `KeyboardMan`. Text-entry dialogs enable this shared manager before accepting characters. It turns keyboard keys into CP949 Hangul syllable bytes and keeps enough composition history to replace or split the current syllable as the user types or presses Backspace.

This is a local input system. The client is not converting the text to Unicode before placing it in controls or packets.

## Input flow

```text
keyboard key and modifier flags
            |
            v
language-toggle and layout checks
            |
            v
initial, medial, and final component state
            |
            v
precomposed CP949 syllable or Jamo fallback
            |
            v
replace the active character or append a new one
```

`input_keyboard_manager_translate_key` owns the composition state machine. It recognizes initial consonants, medial vowels, and optional final consonants. Valid follow-up keys can form a doubled consonant, compound vowel, or compound final consonant. A key that cannot join the active syllable commits that syllable and starts or emits the next character.

The manager retains packed CP949 values for the active composition. Backspace walks that history so a compound syllable can step back through earlier forms instead of disappearing in one operation. A pending-output field lets one key commit the old syllable and also begin a new one.

## CP949 component tables

The client does not calculate modern Unicode Hangul code points. It uses fixed CP949-oriented tables.

`input_hangul_decode_cp949_components` handles the 2,350 precomposed syllables in the `0xB0A1` through `0xC8FE` Wansung grid. Each pair maps to three small indexes:

- initial consonant
- medial vowel
- final consonant, including the no-final state

Forty additional pairs use a separate exception table. An unmatched pair is retained behind an `0xFF` marker so it can pass through without being mistaken for a known syllable.

`input_hangul_encode_cp949_components` performs the reverse lookup. It returns one two-byte CP949 syllable when the component triple exists in the precomposed or exception table. Otherwise it builds an eight-byte compatibility-Jamo fallback beginning with `0xA4D4`, followed by the separately encoded initial, medial, and final components.

The helper names use CP949 because that describes the client byte strings and Windows DBCS behavior. The main 2,350-entry grid is the older Wansung subset, not every extended Unified Hangul Code syllable.

## Layout and lifecycle

`KeyboardMan` is constructed once and published through a global singleton pointer. The `KeyBoard: <number>` configuration entry selects its numeric layout. The manager also owns a secondary language-mode flag and a configured key-plus-modifier chord that can toggle composition.

Text dialogs such as Login, Change Password, Birthdate, Friends, and block-list inputs retrieve the singleton and enable the internal composition path while they are active. Enabling or changing modes resets the current initial, medial, final, pending-output, and history fields so composition does not leak between controls.

The client also contains an 88-byte state serializer and matching loader for 22 big-endian `u32` values. No static caller was recovered for those three serialization helpers, so their intended persistence or transfer owner remains unknown.

## Known limits

- The confirmed output is CP949 byte text, not UTF-8 or UTF-16.
- The precomposed table covers 2,350 Wansung syllables plus 40 explicit exceptions.
- Unsupported component triples use the compatibility-Jamo fallback rather than an extended CP949 syllable.
- The exact user-facing names of the numeric keyboard layouts have not been recovered.
- Several addresses inside the main translator are compiler-split views of one routine. They are recorded as split continuations in the function export, not as separate input features.
