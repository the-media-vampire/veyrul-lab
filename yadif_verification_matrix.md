# yadif failure-mode test matrix

Source: art_01M6V6CAXJB89TN8NEH6VQXXDD r1  
Companion to: yadif_preflight.sh (artifact c63ba895-c1e0-4053-80e8-648ba2df231d)  
Execution status: **not_run** — commands are proposals until a receipt is supplied.

---

## How to use this matrix

1. Obtain a short (~5 s) interlaced test clip with known field order.
2. For each row, run the **Baseline command** first, then the **Test command**.
3. Record `ffprobe` output and a frame screenshot or comb-detection result.
4. A **Disproof observation** invalidates the claim from the source article.

---

## Failure mode 1 — Wrong field order → judder

**Claim (art_01M6V6CAXJB89TN8NEH6VQXXDD r1):**  
> "Symptom: jerky back-and-forth motion. Cause: wrong field order."

| Step | Command |
|------|----------|
| Baseline | `ffmpeg -i in.ts -vf "yadif=mode=0:parity=-1:deint=all" baseline.mp4` |
| Test (wrong parity) | `ffmpeg -i bff_clip.ts -vf "yadif=mode=0:parity=0:deint=all" wrong_parity.mp4` |
| Fix | `ffmpeg -i bff_clip.ts -vf "yadif=mode=0:parity=1:deint=all" correct_parity.mp4` |

**Expected observable outcome:**  
In `wrong_parity.mp4`, moving objects stutter or reverse direction between adjacent frames.  
In `correct_parity.mp4`, motion is smooth and matches `baseline.mp4`.

**Disconfirming observation:**  
If `wrong_parity.mp4` shows smooth motion indistinguishable from `correct_parity.mp4`, the claim that field-order mismatch causes judder is not supported for this clip.

**Minimum evidence needed:**  
Side-by-side screenshot of frame N and frame N+1 from each output on a moving edge, plus `ffprobe field_order` on the source.

---

## Failure mode 2 — Combing survives with deint=interlaced

**Claim (art_01M6V6CAXJB89TN8NEH6VQXXDD r1):**  
> "Symptom: combing remains on some frames. Cause: frames not marked interlaced when deint=interlaced."

| Step | Command |
|------|----------|
| Baseline | `ffmpeg -i in.ts -vf "yadif=mode=0:parity=-1:deint=all" baseline.mp4` |
| Test | `ffmpeg -i in.ts -vf "yadif=mode=0:parity=-1:deint=1" deint_flagged.mp4` |

**Probe step:**  
```
ffprobe -v error -select_streams v:0 \
  -show_entries frame=interlaced_frame,top_field_first \
  -of csv in.ts | head -20
```
If output shows `0,0` rows (not flagged as interlaced), `deint=interlaced` will leave those frames unprocessed.

**Expected observable outcome:**  
`deint_flagged.mp4` retains combing on any frames where `interlaced_frame=0` in the source. `baseline.mp4` does not.

**Disconfirming observation:**  
If all frames in the source are flagged `interlaced_frame=1`, both outputs should be identical. This would mean the failure mode is not triggered, not that the claim is wrong.

**Minimum evidence needed:**  
`ffprobe` frame-level interlace flags on the source, plus a screenshot of a combed frame from `deint_flagged.mp4`.

---

## Failure mode 3 — Unexpected frame rate doubling from mode 1 or 3

**Claim (art_01M6V6CAXJB89TN8NEH6VQXXDD r1):**  
> "Output frame rate doubles" when mode=send_field (1 or 3).  
> "Symptom: frame rate not as wanted. Cause: mode."

| Step | Command |
|------|----------|
| Baseline | `ffmpeg -i in.ts -vf "yadif=mode=0:parity=-1:deint=all" mode0.mp4` |
| Test | `ffmpeg -i in.ts -vf "yadif=mode=1:parity=-1:deint=all" mode1.mp4` |

**Verification:**  
```
ffprobe -v error -select_streams v:0 \
  -show_entries stream=r_frame_rate \
  -of default=noprint_wrappers=1:nokey=1 mode0.mp4

ffprobe -v error -select_streams v:0 \
  -show_entries stream=r_frame_rate \
  -of default=noprint_wrappers=1:nokey=1 mode1.mp4
```

**Expected observable outcome:**  
`mode1.mp4` reports exactly double the `r_frame_rate` of `mode0.mp4`. For 25 fps PAL input: 25/1 → 50/1.

**Disconfirming observation:**  
If `mode1.mp4` reports the same frame rate as `mode0.mp4`, the "fps doubles" claim from the article is not confirmed by that build of FFmpeg.

**Minimum evidence needed:**  
`ffprobe r_frame_rate` on both outputs. This is the cheapest executable test of a source-documented claim.

---

## Evidence status

| Column | Status |
|--------|--------|
| Failure modes and fixes | Source-documented (art_01M6V6CAXJB89TN8NEH6VQXXDD r1) |
| Commands | Derived; not executed |
| Any actual output | **not_run** — awaiting execution receipt |

## Next step

Run Failure mode 3 first: it needs only `ffprobe` on two files and produces a numeric, unambiguous result. Record the `r_frame_rate` values and FFmpeg version. That is the smallest step that moves any claim in this matrix from `source-documented` to `execution-confirmed`.