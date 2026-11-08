# Arm-failure diagnostic guide

Map observed symptoms to probable causes before adjusting parameters.
All causes reference [art_01M6WDX3GNS8TC4HTKQ670H49B, rev 1].

## Command-time failures

| Symptom | Probable cause | Fix |
|---|---|---|
| `Option atadenoise not found` | FFmpeg build lacks the filter | Rebuild with `--enable-avfilter`; verify with `ffmpeg -filters \| grep atadenoise` |
| `Value for s must be odd` or similar | Even value passed to s | Use odd values: 5, 9, 17 |
| `Value out of range` for 0b | 0b above 5 or below 0 | Clamp to 0–5 range |
| Non-zero exit, no specific error | Input codec unsupported | Add `-c:v libx264` probe step or use known-good input |

## Inspection-time symptoms

| Symptom | Probable cause | Discriminating test |
|---|---|---|
| Ghost trail on silhouette in `long` only | s=17 too wide for motion speed | Compare `long` vs `short`; if `short` is clean, s is implicated |
| Ghost trail in both `long` and `scout_0b` | Threshold 0b too high | Lower 0b; s is not the culprit |
| Ghost trail in all filtered arms | Threshold 0a too high for content | Lower 0a first; note hands and hairline separately |
| Background flicker unchanged in `short` | s=5 too narrow to average flicker | Try s=9 (default) |
| Background flicker unchanged in `scout_0b` | Flicker is abrupt (0a-type), not continuous | Raise 0a instead of 0b |
| No visible difference between any arm and control | Thresholds below noise floor | Check that input actually has detectable noise before filtering |

## Discriminating question (Scout's framing, preserved)

If `scout_0b` quiets the background without ghosting:
  → continuous-change threshold (0b) is a more surgical tool than window length.
If `scout_0b` ghosts equally to `long`:
  → 0b is not the culprit; window length is implicated.

Record which outcome you observe before drawing any conclusion about s vs 0b.