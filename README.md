# guided_trial.sh

Reusable shell script for the FFmpeg `guided` filter.  
**Source:** art_01M6W2ZSB54BVKZ8GR448940YN r1  
**Status:** Source-only. Not executed. No output or timing observed.

## What it does

1. **Build check** — exits with a named error if `guided` is absent from the build.  
2. **Baseline first** — runs plain `guided` with all defaults. If edges blur here, something is wrong upstream before you touch any parameter.  
3. **Radius sweep** — holds eps fixed, varies radius across the full documented range (1–20). One parameter at a time.  
4. **Eps sweep** — holds radius fixed, varies eps from tight (0.001) to loose (0.5).  
5. **Fast mode** — one run with `mode=fast:sub=4` for speed comparison.  
6. **Guidance mode** — optional second input; invoked only when a guidance image is supplied.

## Usage

```bash
# Plain smoothing sweep
./guided_trial.sh input.png

# With guidance image (must match resolution + pixel format)
./guided_trial.sh input.png guidance.png
```

## Verification condition

The baseline (`out_baseline.png`) is the control. A working run shows flat areas smoother than the source and edges at the same position. If chroma noise survives, re-run with `:planes=7`.

## Limits

- Not executed — no output, timing or visual result observed.
- FFmpeg build version must include `guided`; check with `ffmpeg -filters | grep guided`.
- Guidance image production is not covered here (see the Guided Image Filtering paper cited in the FFmpeg manual).
- Parameter values in the sweep are illustrative per the source; calibrate to your material.

## Next improvement

Add `ffprobe` readback of edge-pixel variance between `input.png` and `out_baseline.png`. If variance at detected edges is within tolerance, edge preservation is machine-readable rather than eye-checked.