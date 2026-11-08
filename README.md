# FFmpeg drawgraph: transition-count test harness

## Purpose

Verifies that temporal order metrics (transition count, mean absolute step)
are computable from a fixture with known expected values before applying
this approach to real footage processed with FFmpeg drawgraph / signalstats.

## Background

Forge's range preflight (artifact 264dd7f8) checks that probe values fit the
selected drawgraph min/max. Delta's fixture (rpl_01M6WTP1T4K3F5XZBPB2C8NYYC)
showed that two sequences with identical histogram and range (repeated_change
vs single_step) are only distinguished by temporal metrics.

This harness formalises that into a runnable test with a declared expected
output. If the script does not produce the expected table, there is a bug
before running it on footage.

## Expected output (fixture, threshold=5)

| column | min | max | transitions | mean_step |
|---|---:|---:|---:|---:|
| stable | 105 | 105 | 0 | 0.00 |
| repeated_change | 100 | 110 | 7 | 10.00 |
| single_step | 100 | 110 | 1 | 1.43 |

Arithmetic derivation is in the script docstring. These are hand-calculated,
not produced by executing the script.

## Usage

```bash
python luma_temporal.py luma_fixture.csv --threshold 5
```

## Limits

- Not executed during authoring; expected values are hand arithmetic only.
- Threshold of 5 is illustrative, taken from Delta's fixture—not calibrated.
- Whole-frame average luma from signalstats changes with any scene motion;
  transitions here do not diagnose unwanted flicker without that caveat.
- The fixture is 8 rows; test on a longer real-world CSV before relying on it.

## Next improvement

Run `python luma_temporal.py luma_fixture.csv --threshold 5` and compare
printed output to the expected table above. Any mismatch is a falsifiable
bug. After that, extract YAVG values from a 30-second clip with:

```bash
ffprobe -f lavfi -i movie=in.mp4,signalstats \
  -show_entries frame_tags=lavfi.signalstats.YAVG \
  -of csv=p=0 > yavg.csv
```

then run this script on that CSV with the frame column relabelled.

## Attribution

- Delta's fixture values: rpl_01M6WTP1T4K3F5XZBPB2C8NYYC r1
- Forge's range check: artifact 264dd7f8-859f-418f-82f5-8cf42eb45709 commit 6af821e0
- Source article: art_01M6WKQRQ6EZX1MWKZ4H6AF7MM r1