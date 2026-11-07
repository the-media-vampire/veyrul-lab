# Guided filter — verifier's checklist

Source: art_01M6W2ZSB54BVKZ8GR448940YN r1  
Companion to: artifact 7838b593-60d6-4c31-9abc-c6c5c69abdea (commit 67aa909)

---

## Status of claims in the source (before any run)

| Claim | Source status | What would falsify it |
|---|---|---|
| `guided` filter exists in FFmpeg | Source-documented | `ffmpeg -filters \| grep guided` returns nothing |
| `radius` range is 1–20, default 3 | Source-documented | Filter accepts value 0 or 21 without error |
| `eps` range is 0–1, default 0.01 | Source-documented | Filter accepts value 1.1 without error |
| `mode=basic` does not subsample | Source-documented | Identical pixel output to `mode=basic:sub=4` on same input |
| `mode=fast` uses `sub`, default 4 | Source-documented | `mode=fast:sub=1` and `mode=fast:sub=4` produce identical output |
| Single input accepted (no guidance) | Source-documented | One-input command errors with `Too many inputs` |
| Guidance mode requires two matching inputs | Source-documented | Mismatched-resolution pair succeeds without error |
| Only first plane changed by default | Source-documented | Chroma-channel pixel values differ between input and output |

---

## Observations needed after a run of guided_trial.sh

### 1. Baseline sanity (out_baseline.png vs input)
- **Claim being tested:** At defaults the filter smooths without obvious edge blurring.
- **Observable check:** Compare a known hard edge. If PSNR at the edge region drops by more than 3 dB relative to flat-area PSNR gain, the filter may be blurring rather than smoothing.
- **Null result that would satisfy me:** Edge pixels within ±5 DN of source values; flat-area std-dev reduced.

### 2. Radius sweep legibility (out_r1 → out_r20)
- **Claim being tested:** Higher radius increases smoothing neighbourhood.
- **Observable check:** `out_r20_eps0.01.png` should show visibly broader smooth regions than `out_r1_eps0.01.png` on a textured crop.
- **What would disprove it:** No perceptible difference between r=1 and r=20 outputs.

### 3. eps sweep (out_r3_eps0.001 → out_r3_eps0.5)
- **Claim being tested:** Higher eps relaxes edge preservation.
- **Observable check:** A sharp edge present in `eps=0.001` output is blurred in `eps=0.5` output.
- **What would disprove it:** Identical edge sharpness across all eps values.

### 4. Fast mode output (out_fast_sub4.png)
- **Claim being tested:** Fast mode produces an approximation, not identical output.
- **Observable check:** `diff out_baseline.png out_fast_sub4.png` shows non-zero byte differences.
- **What would disprove it:** Byte-identical files.

### 5. Guidance mode (out_guided_mode.png)
- **Claim being tested:** Guidance image changes the filter output vs self-guided.
- **Observable check:** `out_guided_mode.png` differs from `out_baseline.png` when guidance != input.
- **What would disprove it:** Byte-identical output despite different guidance image.

---

## Error conditions to deliberately test

```bash
# Should error: guidance=on with one input
ffmpeg -i in.png -vf "guided=guidance=on" out_err.png
# Expected: 'Invalid option' or 'Too few inputs' error

# Should error: radius out of range
ffmpeg -i in.png -vf "guided=radius=21" out_err.png
# Expected: range rejection error
```

---

## What this checklist does not cover
- Visual quality judgment (taste, not a verifiable claim)
- How to produce a guidance image (the source defers to the Guided Image Filtering paper)
- Performance/timing (not in source claims)
- Specific FFmpeg build version — **record this with every run**

---

## Next improvement
For automated edge-preservation scoring without an eye test:  
`ffprobe` or ImageMagick `identify` can read per-channel std-dev inside a Sobel-detected edge mask.  
If edge-region std-dev changes by < threshold between input and output, edge preservation is machine-confirmed.  
That threshold needs calibration on a known test image — an open research item.