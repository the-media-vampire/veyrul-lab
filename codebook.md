# Codebook

Use only these codes in OBSERVED_* columns. Append a note in the NOTES column for anything that does not fit.

## Experiment A — unique_id stability

| Code | Meaning |
|------|---------|
| STABLE | URL hash is identical before and after headline rename + reload |
| CHANGED | URL hash differs after headline rename + reload |
| NOT_FOUND | Hash or element could not be located |

## Experiment B — repeat-per-strand

| Code | Meaning |
|------|---------|
| BOTH | Both group-row labels (e.g. "Strand-Alpha" and "Strand-Beta") appear in the navigation bar |
| ONE | Exactly one label appears |
| NONE | No group labels appear |
| DEDUP | Viewer renders only one slide for the shared event date (silent deduplication) |
| TWO_SLIDES | Both slides appear; each is independently selectable |

## Common

| Code | Meaning |
|------|---------|
| ERROR | Browser console shows a parse or runtime error |
| BLANK | Slide area is empty / no content rendered |