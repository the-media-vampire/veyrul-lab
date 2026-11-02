# Minimum test contract for Twee 3 CI integration

Status key:
  [D] = documented in source record (art_01M6CR2K2FYD0F71ZB5SPNR2AA r1), not run
  [U] = untested assumption in peer adapter (73bbe0b1), not run
  [?] = evidence gap, unresolved

## Build path
| Claim | Status | Evidence source |
|---|---|---|
| Extension bundles src/ + .storyformats/format.js → build/Story.html | [D] | art_01M6CR2K2FYD0F71ZB5SPNR2AA r1 |
| tt3.config.json overrides default paths | [D] | art_01M6CR2K2FYD0F71ZB5SPNR2AA r1 |
| tt3.config.json is in a published release | [?] | Gap 1 above |
| Tweego CLI replicates the same bundle | [U] | peer adapter 73bbe0b1 (not executed) |

## Passage tag handling
| Claim | Status | Evidence source |
|---|---|---|
| Twine.private omits passage from built HTML | [D] | art_01M6CR2K2FYD0F71ZB5SPNR2AA r1 |
| Tweego has no equivalent tag | [U] | peer adapter 73bbe0b1 |
| Line-oriented pre-filter correctly strips Twine.private passages | [U] | peer adapter 73bbe0b1; see Gap 3 |
| Pre-filter handles EOF-adjacent passages | [?] | not addressed in any artifact |

## Licensing
| Component | License | Evidence |
|---|---|---|
| twine-twee-language extension | MIT (named) | package.json + LICENSE @ 37c487df |
| Tweego | [?] | not read; Gap 2 above |