# KDP Paperback Font Pre-flight Spec

Source: `art_01M6PQJ1Q3CQPV252JPNSAN0SG` rev 2 (captured 2026-11-05).
Rules derived from the Amazon KDP Paperback Fonts help page; vendor text not covered by this MIT license.

## Baseline table

| ID | Local? | Observable failure |
|----|--------|-------------------|
| R01 | Yes | Font size field < 7 pt |
| R02 | Yes | Full page illegible |
| R03 | Yes | Font name mismatch |
| R04 | Yes | No full-page review done |
| R05 | Yes | No licence file found |
| R06 | Yes | Acrobat: not Embedded |
| R07 | Yes | Glyphs cut off at 400% |
| R08 | Yes | Word embed option off |
| R09 | No | Previewer font error |
| R10 | Yes | Bold name unchanged |

## Limits

Nothing here was executed or uploaded. R09 requires KDP Previewer and cannot be verified locally. The source page changes; re-verify before submitting.

## Next improvement

Walk a real .docx against this spec and report which rule produces an unexpected result. That closes the untested flag and surfaces any gap between documentation and runtime behaviour.