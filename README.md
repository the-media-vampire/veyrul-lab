# TIC-80 Lua Starter — README Constants Template

## What this is
A minimal TIC-80 Lua cartridge that encodes the limits stated in
the TIC-80 README (art_01M6Q7AXM1R42XNV7AW8BVSBCY rev 1) as named
Lua constants, with a draw loop and a run checklist.

## Why it matters
The README states specific numbers (240×136, 16 colors, 256 sprites,
4 channels, 4 controllers × 8 buttons) but says nothing about how to
write a game. Naming these as constants:
- Gives a team a single place to update if limits change.
- Provides a runnable baseline: printed values should match README.

## Files
| File | Purpose |
|---|---|
| `cart.lua` | Paste into TIC-80 code editor; Ctrl+R to run |
| `checklist.md` | Fill in Observed column after running |
| `README.md` | This file |

## Baseline vs. test
- **Baseline:** no input, 0 buttons lit, all constants printed.
- **Test:** press a gamepad button; corresponding slot turns bright.

## Next improvement
Add a memory-bank probe: write a value to bank 1 and read it back.
This would test the free-version claim (1 bank) vs. Pro (8 banks)
as a concrete, observable difference — the one split the README
documents but does not demonstrate.

## Licence
MIT. Source: TIC-80 README MIT Licence (LICENSE line 1, same repo).