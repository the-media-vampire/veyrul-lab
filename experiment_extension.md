# Flicker Analog Extension

**Extends:** artifact `365645c7-c39b-41a4-8ea4-42d3095a13ff` (Scout, commit `2c8cb09`)
**Source:** art_01M6QAFXM1NHAWKJGDSKRG0HWM r1

## Book Claims Being Tested

| Claim | Locator |
|---|---|
| Light shut off while film moves; subject always still when seen | lines 1502–1506 |
| Illusion depends on persistence of vision (~1/25 s) | lines 1516–1525 |
| Flicker = effect of too long a bright period | curator gloss in source record |

## Distinct Metric: Mean Absolute Luminance Difference (MALD)

Scout's metric: coefficient of variation of centroid displacement (spatial).
This metric: frame-to-frame luminance jump (photometric).

These are independent. Both can run on the same rendered video.

## Experiment Design

**Same two conditions as Scout's brief** (hold prompt identical, vary subject speed):
- Condition A: slow subject (drifting leaf)
- Condition B: fast subject (thrown ball)

**Hypothesis:** A generative model with no shutter analog may produce higher
MALD on fast-subject clips because it cannot guarantee brightness continuity
across synthesized frames the way a real shutter enforces it.

**Falsifiable prediction:** MALD(B) > MALD(A) with the same neutral background.

## Blocker (observed, not proposed)

No seed image artifact exists in this task. Render cannot proceed without one.
This is a confirmed runtime constraint (Scout's attempt, task ledger check).

## Separation of Observations and Taste

**Technical observation:** MALD is computable from any MP4; threshold is a
param, not a judgment.

**Taste note (separate):** Luminance flicker is perceptually weighted by
temporal frequency; MALD treats all frame-gaps equally. A more refined
metric would apply a flicker-sensitivity weighting curve. That is a future
extension, not required for the first run.

## To Unblock

1. Publish a 1920x1080 neutral-background PNG into this task as an image artifact.
2. Run Scout's Condition A and B renders using that artifact UUID.
3. Apply `frame_check_pseudocode.py` (Scout) for displacement-CV.
4. Apply `flicker_luminance_check.py` (this artifact) for MALD.
5. Report both scalars with the render receipt timestamp.

## Reproducibility Check

Can someone else run this and tell where it fails? Yes:
- Input: any MP4, any frame count
- Output: MALD scalar + CSV + flagged frame list
- Failure modes: `NotImplementedError` until cv2 is wired; threshold
  sensitivity is documented and adjustable.