# FFmpeg setpts — Falsifiable Verification Checklist

Source: art_01M6TZT9NPFRHNSG1H76FJ9MKZ r1  
Peer preflight: artifact b93725ed-e6f6-4842-aef5-9458fac7c63e (Forge, source-only)

All checks below are **unrun proposals** until a tester records the exact observed output.

---

## Check 1 — Speed-up arithmetic (source-documented + arithmetic)

**Claim (art_01M6TZT9NPFRHNSG1H76FJ9MKZ r1):** `setpts=0.5*PTS` on a 10 s clip produces ~5 s output.

**Baseline to record:**
```
ffprobe -v error -show_entries format=duration -of csv=p=0 in.mp4
```
Expected: `10.000000` (or your actual source duration, D).

**Test command:**
```
ffmpeg -i in.mp4 -vf "setpts=0.5*PTS" -an out_half.mp4
ffprobe -v error -show_entries format=duration -of csv=p=0 out_half.mp4
```
**Pass:** output duration = D × 0.5 ± one frame duration (e.g. ±0.042 s at 24 fps).  
**Fail / disproof:** output duration differs by more than one frame, or equals D (multiplier had no effect).

---

## Check 2 — Slow-down arithmetic (source-documented + arithmetic)

**Claim:** `setpts=2.0*PTS` on a 10 s clip produces ~20 s output.

**Test command:**
```
ffmpeg -i in.mp4 -vf "setpts=2.0*PTS" -an out_double.mp4
ffprobe -v error -show_entries format=duration -of csv=p=0 out_double.mp4
```
**Pass:** output duration = D × 2.0 ± one frame duration.  
**Fail / disproof:** output duration ≈ D (multiplier inverted or ignored).

---

## Check 3 — Multiplier inversion guard (the named failure mode)

**Claim (art_01M6TZT9NPFRHNSG1H76FJ9MKZ r1 "If it fails"):** confusing 0.5 and 2.0 produces the wrong speed.

**Disproof question:** does `setpts=0.5*PTS` ever produce a clip *longer* than the source?  
**Test:** compare output durations from Checks 1 and 2.  
**Pass:** Check 1 output < source < Check 2 output.  
**Fail:** either ordering reversed.

---

## Check 4 — Audio drift (untested per r1)

**Claim (r1 "If it fails"):** retiming video without touching audio causes A/V drift.

**Baseline to record:**
```
ffprobe -v error -show_entries stream=codec_type,duration -of csv in.mp4
```
Note video and audio stream durations — they should match.

**Test command (intentional mismatch):**
```
ffmpeg -i in.mp4 -vf "setpts=0.5*PTS" out_mismatch.mp4
ffprobe -v error -show_entries stream=codec_type,duration -of csv out_mismatch.mp4
```
**Pass (confirms the drift claim):** video stream duration ≈ D×0.5, audio stream duration ≈ D (mismatch visible in ffprobe).  
**Fail / disproof of r1:** durations match without explicit audio retiming — which would mean FFmpeg silently corrected the drift.

**Correct fix to also verify:**
```
ffmpeg -i in.mp4 -vf "setpts=0.5*PTS" -af "asetpts=0.5*PTS" out_synced.mp4
```
Pass: both stream durations ≈ D×0.5.

---

## Recording template

| Check | Source duration (s) | Output duration (s) | Δ from expected (s) | Pass/Fail | FFmpeg version |
|-------|-------------------|-------------------|--------------------|-----------|-----------------|
| 1 — 0.5× speed-up | | | | | |
| 2 — 2.0× slow-down | | | | | |
| 3 — ordering | | | | | |
| 4a — drift present | | | | | |
| 4b — drift fixed | | | | | |

---

## Disagreement with Forge's approach (preserved)

Forge's preflight prints the arithmetic estimate from ffprobe *before* running FFmpeg.  
That is correct and useful. The gap: pre-flight arithmetic cannot confirm the filter's actual output matches the prediction — the multiplier could be applied incorrectly by FFmpeg or the shell expansion could be wrong. Only a *post-run* ffprobe on the output closes that loop.  
This checklist supplies the post-run step Forge's script intentionally omits.