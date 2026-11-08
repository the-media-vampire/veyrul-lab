# atadenoise: decision-log template and arm-failure diagnostic guide

Companion to Scout artifact `5751f70b` (commit `7b755486`).
All commands assemble from documented options in [art_01M6WDX3GNS8TC4HTKQ670H49B, rev 1].
No commands were run; no outputs were observed.

## Purpose

Scout's four-arm experiment leaves open the question: once you have outputs,
how do you fill in `variables.md` without letting taste contaminate observations?
This package answers that with:

1. `run_log.md` — per-arm recording template (fill in before watching)
2. `inspect_protocol.md` — inspection order and crop list
3. `diagnostics.md` — symptom-to-cause table for each failure mode

## Prerequisite check (run before the experiment)

```sh
ffmpeg -version > ffmpeg-version.txt
ffprobe -v error -select_streams v:0 \
  -show_entries stream=width,height,r_frame_rate,pix_fmt \
  -of default=noprint_wrappers=1 input.mp4 > input-probe.txt
```

Record both files. If either command fails, stop — the experiment has no baseline.

## Arm definitions (unchanged from Scout)

| Label | Filter string | Variable changed |
|---|---|---|
| control | (none) | — |
| short | `atadenoise=0a=0.02:0b=0.04:s=5:a=p` | s=5 |
| long | `atadenoise=0a=0.02:0b=0.04:s=17:a=p` | s=17 |
| scout_0b | `atadenoise=0a=0.02:0b=0.12:s=9:a=p` | 0b raised |

All use FFV1 lossless output (`-c:v ffv1`) so comparison is not codec-compressed.