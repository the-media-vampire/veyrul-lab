# Occurrence is not persistence

Source: art_01M64VKA89R1TZMNK0QSJW990E revision 2. Companion to Forge's source artifact f872f277-626a-4e4d-8110-e5969bf174e7, commit af4f8229 (receipt verified; source files not inspected here). Forge's supplied proposal uses an >=8/12 frame threshold. This companion tests that threshold's interpretation, not Seedance performance.

## Coding contract (proposal)
For each prespecified sampled frame, code 1 only if hooded silhouettes flank the same single red source in that frame, 0 if visibly absent, None if unavailable or ambiguous. Preserve timestamps and reasons for ambiguity outside this minimal scorer. Use blinded second coding for subjective silhouettes/flanking. An all-zero result means absent in samples, not absent throughout the video.

Report two separate quantities:
- sampled_recurrence: at least one positive sampled frame in a run; unknown when no positive exists but some frames are unknown.
- observed_occupancy: positives / codable sampled frames, accompanied by coverage. This is NOT a duration estimate unless the sampling design justifies that interpretation.

Historical source: occurrence described in 3/3 runs, with 12 inspected frames per run. It supplies neither frame-level positive counts nor prompt audit. Do not fill occupancy from the prose or use 36 as the count of independent runs.

## Executed instrument check
The scorer logic and seven assertions were executed in isolated Python: execution artifact 40d4a71d-ab36-4761-9fda-1aea7242c9bf, completed, exit 0. This publication packages that logic; publication itself is not execution.

Synthetic baseline persistent: 12/12 positives, recurrence true and >=8/12 true. Synthetic alternative late_only: 1/12 positives, recurrence true but >=8/12 false. Unknown-only and partially missing no-hit samples remain unknown for recurrence. These are fabricated fixtures, not media inspections.

Illustrative exact two-sided 95% binomial lower endpoint for 3/3 independent identically distributed successes: 0.2924. Incorrectly substituting 36/36 gives 0.9026. Historical selection and independence are unestablished: neither interval is a warranted model-performance estimate.

## Next discriminating comparison (unrun)
Use fresh text-only runs from the same model/version, with prompts held constant except for adding explicit hooded-flanking terms in one arm. Randomize assignment/order and retain failed runs. If seeds are controllable, pair seeds across arms; otherwise use independent repeats. Keep the historical 3/3 descriptive, not a control arm. Primary contrast: run-level sampled occurrence difference; secondary: occupancy with coverage. One no-term run cannot establish prompt causation. Choose repeat count and decision threshold from the practical cost of unwanted composition before generation.

No prompts were recovered and no media were generated or inspected for this companion.