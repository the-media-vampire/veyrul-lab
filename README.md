# Caption pipeline provenance manifest template

Fill `caption_pipeline_provenance.json` once per caption-generation run.
Store the filled copy alongside the `.ass` output.

## Why this exists

Theo's quantization adapter (artifact `15a27d97`, commit `3edb60486f`) handles the
interface between the aligner and the ASS converter. It does not record *which*
revisions were active. Without that record, a future agent cannot determine whether
a changed converter SHA altered the drop behavior the adapter assumes.

This template closes that gap. It is not an execution record.

## Minimum fields to fill

| Field | Why it matters |
|---|---|
| `converter.git_sha` | Adapter assumes drop behavior of `5496e6c`; a changed SHA may change that |
| `adapter.policy_chosen` | DROP/CLAMP/MERGE have different overlap risks; must be traceable |
| `player.frame_rate_hz` | CLAMP overlap risk is frame-rate-dependent |
| `aligner.vocal_source` | Case 3 fix only applies when separator is active |

## Sources

- Atlas: `art_01M6V2D44ND0QGWCJW3GWYSKXF` r1
- Converter fixture: `rpl_01M6TVE4ZYHWK5D4FVKFS9ES21`
- Piper inspection: `rpl_01M6S9EFV5919ADJSB85VQSY5J`
- Adapter artifact: `15a27d97-a53f-4c2b-9818-dfe52caa40e3`