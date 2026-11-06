# KDP Font Disproof Criteria
Supplement to Forge artifact 043efff5 commit 245b33d.
Source: art_01M6PQJ1Q3CQPV252JPNSAN0SG rev 2 (captured 2026-11-05).
Not executed. No acceptance guaranteed.

| ID | Falsifying observation | Method | Confidence |
|----|------------------------|--------|------------|
| R01 | Body-text run < 7pt in Word size field | Select All; check size field | High |
| R02 | Reviewer cannot read full page at final size | Print one page; log reviewer+size | Low (subjective) |
| R03 | PDF font name not in R03 list AND no licence URL on record | Acrobat props; compare list | Medium (list drifts) |
| R04 | No dated log entry before export | Process log; absence falsifies | Medium (process gap) |
| R05 | No licence URL/file for >=1 font used | Collect one URL per family | Medium |
| R06 | Acrobat Fonts tab: any font lacks Embedded/Embedded Subset | Single-font test PDF; Acrobat props | High |
| R07 | Any glyph cut off or misaligned at 400% PDF zoom | Zoom 400%; inspect all glyphs | High |
| R08 | Word Save: embed off OR either sub-option checked | Screenshot Word > Options > Save | High |
| R09 | KDP Previewer returns a font error anywhere in file | Run Previewer; named error falsifies | High (Previewer required) |
| R10 | Bold/italic run shows same font family name as base weight | Word: select bold run; check name | High |

## Calibration notes
- R02: unfalsifiable without logging reviewer identity and print size.
- R04: a process gap, not a file property; a pre-flight log is the only satisfying evidence.
- R03: 12-font list from 2026-11-05; re-verify against live page before each submission.
- R09: cannot be tested locally; exclude from any local-only pass.

## Next improvement
Run R01, R06, R07, R08, R10 against a real .docx; record exact values observed.
One unexpected result overrides all documentation inferences.