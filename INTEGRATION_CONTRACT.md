# Integration contract: Bitsy v0.2 sound + loop ↔ Web Audio API

## Sources
- Bitsy System API: art_01M6Q546ZG458Z26XTSCVA605K rev 1
  system.md @ ee412fa8c072d16af4aedd90d4ad3fb7306911b0
- Web Audio API: W3C living standard (browser-native; no additional licence)

## Interface boundary

| Bitsy call | Adapter action | Conversion |
|---|---|---|
| `bitsy.sound(ch, dur, freq, vol, pulse)` | OscillatorNode + GainNode | dHz÷10=Hz; vol÷15=gain; duration ms→s |
| `bitsy.loop(fn)` | `requestAnimationFrame` wrapper | timestamp diff → dt ms |

## Assumptions this adapter makes explicit
1. AudioContext available (browser only).
2. AudioContext created after a user gesture (browser autoplay policy).
3. Frequency unit is decihertz (system.md documents this).
4. Volume 0–15 is a linear scale — the page states the range but not linearity.
5. Pulse wave duty cycles (1/8, 1/4, 1/2) have no Web Audio native equivalent;
   all three map to 'square' with a console warning. This is a lossy mapping.
6. The API is flagged experimental (v0.2); any of these signatures may change.

## What is NOT covered
- Memory blocks, tiles, graphics modes, text modes, palette, textbox, button input.
- `getGameData()`, `getFontData()`, `log()`, `color()`, `graphicsMode()`, `textMode()`.

## Provenance and licence
- Bitsy repository: le-doux/bitsy, MIT Licence (LICENSE.md line 1, as archived).
  No legal conclusion is made; the full licence file was not read.
- This adapter: MIT (see repository licence).
- The archived GitHub repository is marked read-only; active project is on Codeberg.
  Verify the Codeberg repository for the current API before integrating.

## Open questions (see research queue entry)
- Does Bitsy v0.2 volume use linear or logarithmic scaling?
- Has the Codeberg migration changed any function signatures?
- Does bitsybox implement these the same way as the web system.js?