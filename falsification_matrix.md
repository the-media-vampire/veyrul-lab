# avgblur Falsification Matrix

Source: art_01M6WGWVXNKPZGYE6MDK0PPWKB r1  
Status: **unexecuted checklist** — no FFmpeg output has been observed.

---

## How to use this

For each claim, run the stated command and compare the observed result to the
Disproof Condition. If the disproof condition is met, the claim is false for
your build. Record your FFmpeg version with every result; the source states
no manual version.

---

## Claim table

| # | Claim (from source) | Status in source | Test command | Disproof condition |
|---|---------------------|-----------------|--------------|--------------------|
| 1 | `sizeY=0` defaults to equal `sizeX` | Source-documented | `ffmpeg -i in.mp4 -vf avgblur=sizeX=20:sizeY=0 h.mp4 && ffmpeg -i in.mp4 -vf avgblur=sizeX=20 s.mp4` then `cmp h.mp4 s.mp4` | Files differ (encoding aside: compare raw decoded frames with `ffprobe -show_frames`) |
| 2 | Larger radius → softer picture | Expected check in source | Compare baseline (sizeX=1) vs sizeX=20 using detail_ratio from Delta's function | detail_ratio ≥ 1.0 (trial is not softer than baseline) |
| 3 | All planes blurred by default | Source-documented | Decode a chroma channel from filtered output; measure MAE vs unfiltered | MAE on chroma channel = 0 (chroma unchanged, so planes default is wrong) |
| 4 | Filter is present in the build | Prerequisite | `ffmpeg -filters 2>&1 \| grep avgblur` | No match — build lacks avgblur; sweep and measurement results are meaningless |
| 5 | `sizeX=1` is a minimal-effect baseline | Forge's structural choice | Visual + detail_ratio comparison of sizeX=1 vs raw input | detail_ratio(sizeX=1 vs raw) = 1.0 — identical to input, making it a true no-op, not a low-effect baseline |

---

## Important clarification on Claim 5

Forge treats `sizeX=1` as a baseline to detect filter absence.  
Delta correctly notes: **no visible difference does not prove filter absence.**  
My addition: `sizeX=1` is *itself* a filtered treatment. For a true unfiltered
baseline, compare against the raw input (or a passthrough `-vf null` output).
If `sizeX=1` produces detail_ratio < 1.0 vs raw, the filter is active but
subtle — not absent. Only a build check (Claim 4) definitively establishes
filter presence.

---

## Ordering recommendation

1. Run Claim 4 first (< 1 second, binary result).
2. If avgblur is absent, stop — all other results are meaningless.
3. Run Claim 1 next (confirms documented default before trusting sweep).
4. Run Claims 2 and 3 on matched raw frames before lossy encoding.
5. Claim 5 distinguishes a minimal-effect treatment from a true control.

---

## Limits

- This checklist is not executed; all disproof conditions are predictions.
- Error-condition tests (radius out of range, one-input guidance) are not
  listed here — see prior guided-filter falsification work in memory.
- Encoding can mask pixel-level differences; always compare decoded frames.