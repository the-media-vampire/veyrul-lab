# Stack-midpoint text label — two contrasting configurations

Source: art_01M6MH8DFE1KD1GQA0A0VTGENT revision 3 (checklist untested)

## Experiment intention

The checklist in the source article states: *"The stack midpoint output is meant for placing text on stacked bars."*  
That claim is flagged as our inference, untested. This package holds all variables fixed (same data, same colour, same font size) and changes only the text-channel binding to test whether `stackY2({y: 'midpoint'})` lands the label at the visual midpoint of the bar segment.

## Contrasting configurations

| Config | Text y-channel | Expected label position | Discriminating observation |
|--------|---------------|------------------------|----------------------------|
| A (control) | `y: 0` (baseline) | Label at bar bottom | Verifies that *not* using midpoint puts the label in the wrong place |
| B (treatment) | `stackY2({y: "midpoint"})` | Label at bar midpoint | Tests the documented claim |

If B lands at the midpoint and A does not, the documented claim holds.  
If both land at the same position, the midpoint output is not behaving as documented.  
Either result is informative.

## How to run

Open `index.html` in any modern browser with internet access (loads Plot from CDN). No build step.

## Variables held fixed
- Same three-row dataset (two groups, two stack layers each)
- Same `barY` mark with implicit stack
- Same font size (11px), same fill colours
- Only the `y` channel on the `text` mark changes between configs

## Technical observations (record separately from taste)
- The `dy` offset on the text mark shifts by pixels, not data units — note whether labels appear clipped at small bar heights.
- If the label is not visible, check that `fill: 'white'` has sufficient contrast against the bar fill. The source article notes no numeric contrast threshold was tested.
- Plot does not measure text width exactly (documented); labels may overlap at narrow bar widths.