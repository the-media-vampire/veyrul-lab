# TIC-80 README Claim Falsification Map

Source: art_01M6Q7AXM1R42XNV7AW8BVSBCY rev 1  
Companion to: artifact 94fb16a1-fb04-493e-ad11-63ecd9c836ec (Forge, cart.lua)  
Author: Vera (Veyrul Verifier)  
Status: **unrun — proposals until executed in TIC-80**

---

## Three Verifiability Tiers

### Tier 1 — Tautological (cart.lua prints a hardcoded constant)
These checks pass even if TIC-80 is completely wrong about its own limits.
A passing screen print is NOT evidence the runtime limit matches.

| README Claim (art rev 1) | Hardcoded in cart.lua | What would falsify it |
|---|---|---|
| Display: 240×136 px (line 46) | `SCREEN_W=240, SCREEN_H=136` | Draw a pixel at (239,135); if TIC-80 clips it to a smaller canvas, the claim fails. Draw at (240,136); if it renders without error, claim fails. |
| 16 color palette (line 46) | `PALETTE_N=16` | Call `poke(0x3FC0 + 16*3, 0)` (byte past palette); if readable/writable as palette, the 16-color count is wrong. |
| 256 sprites (line 46) | `SPRITES_N=256` | Call `spr(255,0,0)` and `spr(256,0,0)`; if 256 renders without an error/blank, the upper bound claim fails. |

### Tier 2 — Partial Runtime (cart.lua's btn() loop is a genuine probe)
These use real TIC-80 API calls and can produce meaningful pass/fail.

| README Claim (art rev 1) | Runtime probe in cart.lua | What would falsify it |
|---|---|---|
| Up to 4 controllers (line 64) | `btn(b)` on ctrl 0 only | `btnp(0,0,4)` returning true for ctrl index 4 or higher would falsify the "up to 4" claim. |
| Up to 8 buttons each (line 65) | Loop b=0..7 | `btn(8)` returning true (non-nil, non-false) would falsify the "up to 8" claim. |
| 4 channel sound (line 46) | Not probed at all | `sfx(0,0,30,0,15,4)` (channel 4) completing without error would falsify the "4 channel" claim. |

### Tier 3 — Not Probed (Forge noted; confirmed absent)
These README claims have zero test coverage in the current artifact.

| README Claim (art rev 1) | Why untested | Minimum falsifying observation |
|---|---|---|
| 1 memory bank free / 8 Pro (lines 67, 90) | No bank write/read probe | Write to bank 1 (`sync(1,1,false)`) in a free build; if it succeeds without error, the "1 bank" claim is in question. |
| Nine languages (lines 55-63) | Lua only | Load a Wren or Squirrel cartridge; failure to parse = that language claim is not satisfied by that build. |
| Text-format cartridges (Pro, line 91) | Not in free build scope | Save a cartridge in free build as text; if it succeeds, the Pro-exclusivity claim fails. |
| Works on "all popular platforms" (line 48) | No build tested | One failed official-build platform = claim narrowed. |

---

## Summary Gap

Forge's cart.lua is a useful starting scaffold. Its Tier 1 checks
(hardcoded constants printed to screen) cannot distinguish a correct
TIC-80 implementation from a broken one with the same numbers.
Tier 2 (btn loop) is the only genuine runtime probe present.

The next concrete improvement Forge identified — a memory-bank write/read
probe — is the highest-value Tier 3 gap: it tests the one documented
free-vs-Pro difference and requires a real API call that could fail.

---

## Limits
- This file is unexecuted; all probes are proposals.
- Memory addresses cited (0x3FC0) are from TIC-80 public documentation,
  not independently verified here.
- Falsification conditions assume the API call returns a usable value;
  silent failures (no error, no output) may not distinguish pass from fail.