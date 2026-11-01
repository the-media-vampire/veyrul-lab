# Seedance look-target branch contract

## What this is

A composable adapter keyed on Seedance 2.5 `look_target`.
Two branches: `3d_cinematic` and `anime_first`.

Source observation: **art_01M64VK50F7QM10TWFSS9HRXBQ r2**  
Execution verified: run **931fad90-7ab9-4908-8cb1-f7340c271fbb**  
Missing-evidence request: **rqr_01M6BVS0SR836JZKM0MQSY0J3H**

## The mechanism

The source article documents that the same five-beat scene structure appears across both look-target settings. The only confirmed change is the surface shading regime. This contract exposes that branch condition as an explicit interface so a downstream compositor can declare which shading path it expects.

## Interface

```python
from look_branch_contract import adapter
params = adapter("anime_first")
# params["shading_mode"]      -> "flat_cel"
# params["compositing_hint"] -> "posterize_before_key"
# params["face_geometry"]    -> "planar"
# params["open_assumptions"] -> [...]
```

## Open assumptions (not resolved by source)

| # | Assumption | Branch |
|---|-----------|--------|
| 1 | Pixel format at output boundary not stated | both |
| 2 | Alpha channel export not stated | 3d_cinematic |
| 3 | No model-output license stated | both |
| 4 | Flatness degree not quantified | anime_first |
| 5 | No seed set — intra-group variance unknown | anime_first |
| 6 | Audio not reviewed | both |

Assumptions 1 and 3 are blocking for production use.
Research request rqr_01M6BVS0SR836JZKM0MQSY0J3H covers both.

## What this is NOT

- Not a confirmed Seedance output specification
- Not a benchmark; the article is seven historical founder tests
- Not independent of the source article's cautions (1.7 s sampling interval)