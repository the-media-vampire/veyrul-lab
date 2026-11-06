# Godot 4.6 import checklist — constraint bake validation

Source: art_01M6QSV2D946VDMJJM3A83T42E rev 1  
Script: export_gltf_constraint_test.py

## Setup (record before each run)
| Field | Value |
|---|---|
| Blender version | |
| Godot version | |
| Exporter sampling rate | 1 |
| GLB file hash (sha256) | |
| Import date | |

## Baseline — `constraint_test_bake_OFF.glb`

1. Import GLB into Godot 4.6 project (Project → Import…).
2. Open scene in Scene dock.
3. Select `ConstrainedProp` node.
4. Check AnimationPlayer → List animations.

| Check | Expected (baseline) | Observed |
|---|---|---|
| AnimationPlayer present | Possibly absent or empty | |
| Track count on ConstrainedProp | 0 (no baked motion) | |
| Transform at frame 60 matches Blender viewport | Unlikely without bake | |

## Test — `constraint_test_bake_ON.glb`

Same steps with the bake_ON file.

| Check | Expected (test) | Observed |
|---|---|---|
| AnimationPlayer present | Yes | |
| Track count on ConstrainedProp | ≥1 (position/rotation keys) | |
| Transform at frame 1 | Matches Blender frame 1 pose | |
| Transform at frame 60 | Matches Blender frame 60 pose | |
| emissive_strength extension present | N/A for plain diffuse | |

## Material spot-check (same import)
| Check | Expected | Observed |
|---|---|---|
| ConstrainedProp base color correct | Yes (Principled node) | |
| No shader errors in Godot console | Yes | |

## Result
- [ ] PASS: bake_ON shows ≥1 track, bake_OFF shows 0 — claim confirmed.
- [ ] FAIL: describe what differed.
- [ ] PARTIAL: note which checks passed.

## Preserve
- Both GLB files
- Blender source .blend
- This completed checklist
- Godot console log (Help → Copy System Info)