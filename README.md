# avgblur_trial.sh

A focused trial harness for FFmpeg `avgblur` based on
**art_01M6WGWVXNKPZGYE6MDK0PPWKB r1** (documentary review, no run recorded).

## What it does

1. **Baseline** (`sizeX=1`) — minimum-effect reference. If this is indistinguishable
   from input, something is wrong before tuning starts (wrong build, wrong filter).
2. **Radius sweep** (`sizeX` = 5, 10, 20; symmetric) — one variable at a time.
3. **Anisotropic test** (optional `aniso` arg) — `sizeX=20:sizeY=1`, horizontal-dominant blur.
   Marked as inference in the source article.

## Usage

```bash
bash avgblur_trial.sh input.mp4
bash avgblur_trial.sh input.mp4 aniso
```

Outputs: `avgblur_baseline_sx1.mp4`, `avgblur_sx5_sym.mp4`, etc.

## Record with your results

```bash
ffmpeg -version | head -1
```

The manual states no radius range or default; results will vary by content.

## Evidence status

| Item | Status |
|------|--------|
| sizeX, sizeY=0 default, planes default | Source-documented (art_01M6WGWVXNKPZGYE6MDK0PPWKB r1) |
| Command assembly | Assembled from documented options |
| Anisotropic use | Inference (noted in source) |
| Any real output | **Not run — no result observed** |

## Verification condition

The fix worked if: `avgblur_sx20_sym.mp4` is visibly softer than
`avgblur_baseline_sx1.mp4`, and baseline is distinguishable from raw input.
If not: raise `sizeX` or restrict `planes` to isolate chroma smear.

## License
MIT