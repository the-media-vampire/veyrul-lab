# ffmpeg colour-matrix mismatch validator

Numerically confirms the documented behaviour described in:
> EncodingGuidelines (Academy Software Foundation), colour preservation page  
> Summarised in: `art_01M6CQ0D711XXF9QTA7NVVMCJP` rev 2

## What it shows

ffmpeg treats untagged still images as BT.601 and encodes YCbCr accordingly.  
A modern browser or player expects BT.709 tags and decodes as such.  
The mismatch shifts chromatic values by up to **~0.086 on a 0-1 scale** (≈ 22 DN at 8-bit).
Neutral grey is unaffected (R=G=B values cancel in both matrices).

## Observed results (float-precision matrices)

| Patch  | Baseline ΔE | Fixed ΔE |
|--------|-------------|----------|
| red    | 0.066       | 0.000    |
| green  | 0.085       | 0.000    |
| blue   | 0.038       | 0.000    |
| yellow | 0.038       | 0.000    |
| purple | 0.026       | 0.000    |

## Practical fix (from source docs)

```bash
ffmpeg -i input.png \
  -colorspace bt709 -color_primaries bt709 -color_trc iec61966-2-1 \
  -vf scale=out_color_matrix=bt709 \
  output.mp4
```

For sRGB sources the docs recommend `-color_trc iec61966-2-1` (the sRGB flag),  
not `bt709`, as Safari interprets bt709 as camera gamma ~1.95.

## Limits

- Matrices are full-range; limited-range (studio swing) adds another layer.
- 8-bit quantisation compounds the error further; test at full precision.
- Run against real encodes to verify ffmpeg build behaviour.

## License
MIT — see repository root.