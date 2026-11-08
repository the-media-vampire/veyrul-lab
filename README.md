# graph_check.sh

A shell wrapper for the FFmpeg `signalstats + drawgraph` workflow documented in
**art_01M6WKQRQ6EZX1MWKZ4H6AF7MM r1** (Veyrul).

## What it adds

The source article's check is visual only: "read for spikes".
This wrapper adds a numeric pre-pass:

1. **ffprobe probe** — reads every frame's `lavfi.signalstats.YAVG` value and
   prints the observed min and max.
2. **Range warning** — compares observed range to your chosen `min`/`max`
   before rendering, so a misconfigured range is caught before you wait for
   a full render.
3. **Confirm gate** — asks before writing output.

## Baseline comparison pattern

| Signal | What you see | What it means |
|--------|-------------|---------------|
| Observed min/max matches graph min/max | Line fills the frame | Range is correct |
| Observed max > graph max | Line clips at top | Increase max |
| Observed min < graph min | Line clips at bottom | Decrease min |
| `No YAVG values found` | ffprobe error | Input path wrong or signalstats not built |

## Usage

```bash
chmod +x graph_check.sh
./graph_check.sh input.mp4           # defaults: min=0 max=255 output=graph.mp4
./graph_check.sh input.mp4 10 240   # custom range
./graph_check.sh input.mp4 0 255 out.mp4
```

## Requirements

- FFmpeg and ffprobe with `signalstats` and `drawgraph` compiled in.
- Record your FFmpeg version with results (the article notes the manual has no page version).

## Limits

- Not executed during authoring; source-documented behaviour only.
- `ffprobe -f lavfi movie=` input method may differ across FFmpeg versions —
  test with `ffprobe -filters | grep signalstats` first.
- The probe pass reads every frame, which is slow on long clips.
- Interactive confirm gate requires a TTY; pipe with `echo y |` to skip.

## Next improvement

Add a histogram of YAVG values (not just min/max) so bimodal distributions
(e.g. flicker between two levels) are visible in the probe output before
the graph is rendered.