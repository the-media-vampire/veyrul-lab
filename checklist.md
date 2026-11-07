# TIC-80 README Limits — Run Checklist

Source: art_01M6Q7AXM1R42XNV7AW8BVSBCY rev 1 (lines 46-65).
Status: **unrun** — these are proposals until executed in TIC-80.

## Load test (cart.lua)
1. Open TIC-80 (free or Pro build).
2. Paste cart.lua into the code editor.
3. Press Ctrl+R to run.

## Pass / Fail rows

| Check | Expected | Observed | Pass? |
|---|---|---|---|
| Screen label shows | `240x136` | _fill in_ | |
| Palette count | `16 colors` | _fill in_ | |
| Sprites count | `256` | _fill in_ | |
| Channels count | `4` | _fill in_ | |
| Controller × buttons | `4 x 8btn` | _fill in_ | |
| BTN CTRL0 row present | 8 slots (0-7) | _fill in_ | |
| Press btn 0 on gamepad | slot 0 turns bright | _fill in_ | |

## What a failure means
- If any constant mismatches, the README claim for that line is
  not reflected in the running environment. Document the actual
  value as the corrected baseline.

## Limits
- Cart not executed; checklist is a proposal.
- Pro-only features (8 memory banks, text cartridges) not tested here.
- Languages other than Lua not covered.