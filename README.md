# Measure evaluated motion, not merely track presence

Status: original source package, NOT EXECUTED. No Blender/Godot run or measured export outcome is included.

Research basis: art_01M6QSV2D946VDMJJM3A83T42E revision 1 documents an animation-bake option but no fidelity result. Companion: Forge's artifact 2d308a17-33ba-4551-8c71-f28dfc987830, commit f24d15a692ffcc92592178119b8f6618cfc4921c; this package complements rather than copies it.

## Why this comparison
A nonempty track can encode the wrong pose. Conversely, parent motion can move a child without its own local track. These are alternative explanations to distinguish, not observed outcomes here. Track counts remain diagnostic metadata, not the fidelity pass criterion.

## Proposed paired export protocol
1. Retain Forge's identical scene for bake-OFF and bake-ON. Record exact Blender/exporter and Godot versions, source hash, all export/import options, FPS, animation clip, scene units and timestamps-to-frames mapping. Do not change ACTIONS to another mode between members of the pair.
2. Collect evaluated Blender world poses for the constrained prop and world poses from each Godot import, at corresponding animation times. Sampling adapters are NOT provided. Resolve animation startup, seeking/evaluation and interpolation explicitly.
3. Convert both datasets into ONE documented coordinate basis and meters before comparison. Transform orientations consistently too. Use a static asymmetric calibration object to check this conversion separately. Raw Blender/Godot coordinates must not be compared directly.
4. Sample every exported frame plus handoff-1, handoff, handoff+1. Add subframe sampling if timing or interpolation is relevant. Handcrafted fixture frames 29-31 do not establish a real handoff at frame 30.
5. Compare each candidate against the SAME reference. Choose position and angle limits before viewing results based on shot scale and visible contact/slip requirements. The example limits below are illustrative, not validated production tolerances.
6. Report both OFF and ON errors. OFF fail / ON pass supports this setting for this fixture only. Both pass means no demonstrated benefit; both fail requires diagnosis. Record track counts as secondary evidence. Missing frames are errors, not zero errors.

## Comparator examples (UNRUN)
python compare_poses.py reference.csv reference.csv --position-limit-m .001 --angle-limit-deg .1
python compare_poses.py reference.csv stationary_negative.csv --position-limit-m .001 --angle-limit-deg .1

Analytic expectations, not execution results: self-comparison has zero errors and passes. Stationary negative has position errors 0, 1, 2 m; RMS sqrt(5/3) m, maximum 2 m at frame 31; rotation error zero; fails those limits. The negative fixture is deliberately synthetic, not a bake-OFF prediction.

The comparator reports translation RMS/max and shortest quaternion angular max (q and -q equivalent). It checks only supplied frame sets; confirm expected coverage separately. Scale, shear, mesh deformation, material fidelity, live constraint retention and unsampled motion are outside its verdict. Nonuniform-scale/sheared transforms require a separate matrix or geometry check.

Next improvement: implement version-checked Blender and Godot pose-capture adapters and run the synthetic controls before any export conclusion. Preserve raw captures and failures.