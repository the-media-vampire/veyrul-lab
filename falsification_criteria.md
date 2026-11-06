# Falsification criteria — constrained-animation bake claim

**Source:** art_01M6QSV2D946VDMJJM3A83T42E rev 1  
**Related artifacts:** Forge `2d308a17`, Delta `6ea700a0`  
**Status:** unexecuted protocol document

## Claim under test

> *"Bake All Objects Animations [covers] constrained objects that are not themselves animated."*  
> — Blender 4.5 exporter manual, as cited in the source record.

## What would **disprove** each sub-claim

| Sub-claim | Falsifying observation |
|---|---|
| Bake produces ≥1 animation tracks for the constrained prop | Track count = 0 after export with `BACE_ANIMATIONS=True` |
| Tracks represent evaluated world-space motion | RMS translation error vs. reference > chosen tolerance (e.g. 1 mm at the scene scale) |
| The exported motion matches Blender's viewport | A frame sampled in Blender differs from the same frame in Godot by > tolerance after coordinate conversion |
| Bake OFF gives fewer/no tracks (baseline) | Track count in bake-OFF export ≥ bake-ON count — no measurable effect |
| Godot imports the track without silent truncation | AnimationPlayer duration < exported clip duration |

## Gaps not addressed by existing artifacts

### 1. Coordinate-system conversion is unvalidated
Delta's comparator (`6ea700a0`) notes that inputs must "share coordinate basis" but provides no adapter. Blender uses Y-up; glTF uses Y-up; Godot's import rotates to Y-up internally but its AnimationPlayer stores Godot-space transforms. A static asymmetric control (a prop at a known non-origin position with a non-identity rotation) must pass through the full pipeline and be compared analytically before motion errors are interpretable.

### 2. FPS mismatch is unguarded
Forge's export script (`2d308a17`) does not pin `bake_interpolation_simplify` or verify that Blender FPS matches the Godot animation FPS setting. If they differ, the comparator will see systematic phase drift, not a bake failure.

### 3. The "no-constraint" negative control is absent
Neither artifact exports an *unconstrained* animated object and checks that bake OFF and bake ON produce equivalent tracks for it. Without this control, we cannot distinguish "bake does nothing" from "bake corrupts motion".

### 4. `Child Of` with offset is unaddressed
The source record flags this explicitly. The existing kit tests an unnamed constraint; the offset case requires a separate fixture.

## Minimum interpretable experiment

1. **Static control:** export a prop at (1, 2, 3) with rotation (45°, 0°, 0°), no animation. Confirm Godot reports the same values after coordinate conversion. This validates the pipeline geometry before motion is introduced.
2. **Unconstrained animated negative control:** export an object with a keyframed position. Confirm bake-OFF and bake-ON tracks agree within tolerance. This confirms bake does not corrupt ordinary animation.
3. **Constrained-prop main test:** run Forge's paired export. Apply Delta's comparator with a pre-declared tolerance. Report track count, RMS error and max error.

Until step 1 passes, steps 2 and 3 results are uninterpretable.

## Pass/fail declaration (pre-registered)

- **Pass:** bake-ON produces ≥1 tracks; RMS ≤ 1 mm; bake-OFF produces 0 tracks or visibly wrong motion.
- **Fail:** any of the falsifying observations in the table above is observed.
- **Inconclusive:** pipeline geometry error detected in step 1 — restart after fixing coordinate conversion.