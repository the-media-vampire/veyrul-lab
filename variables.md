# Variable isolation record

Use this file to track which parameter changed in each arm. Fill in before running.

| File | r | s | p | Changed from previous |
|---|---|---|---|---|
| control.mkv | — | — | — | baseline |
| luma_only.mkv | 3 | 128 | 1 (default) | filter applied, luma only |
| all_planes.mkv | 3 | 128 | 7 | planes only |

**Rule:** Only one cell should change per row. If you need to vary sigma AND planes, add a new arm and a new row — do not combine changes.