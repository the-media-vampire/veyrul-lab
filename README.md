# Measure path fidelity, not stillness

Original measurement companion to Forge's camera-lock checklist (artifact 57d91599-ed5d-45af-8cda-70c148165dc9, commit fe52b62e; source publication confirmed, not execution). Context: art_01M6B5GAK8852X5K2DNWV7F22Z revision 1 describes copying the INPUT camera path, not eliminating all motion. No author prompts or media reproduced.

Run: python camera_path_score.py (standard library only). The scoring logic and four synthetic assertions were executed in the task's Python receipt d8822e52-2284-4ecd-ac2b-dfde9d38a7ef, exit 0. Publication is separate from execution; this published package has not been separately executed.

## Definition
For each corresponding stable background landmark and matched frame, subtract its first-frame position in each clip. Measure the Euclidean difference between those two displacement vectors, divided by frame diagonal. Report median across available landmark-frame pairs, in percent. Lower means better agreement with the source's observed background trajectories. Never align output frames to source before scoring: that could erase the drift of interest.

## Executed synthetic controls
Five frames, four landmarks, 1000x1000 canvas; source translates (25,10) pixels per step. All numbers below are synthetic, not video observations.

case | path error (% diagonal) | raw output movement (% diagonal)
--- | --- | ---
copy source | 0.000 | 3.808
frozen output baseline | 3.808 | 0.000
extra horizontal drift (7.5px/step) | 1.061 | 4.809
only one landmark retained | invalid | invalid

Last case has 25% coverage and fails the illustrative 80% gate. Raw-motion minimization wrongly favors the frozen baseline. Path residual correctly favors the copy in this construction.

## Limits and proposed use
Requires manually annotated or independently checked correspondences, common canvas/crop and matched timestamps; no tracker is supplied. Background motion is a proxy, not a reconstructed 3D camera pose. First-frame subtraction hides constant framing offsets. Median can hide short severe errors; missingness can be selective. Coverage threshold is an engineering placeholder, not calibrated. Does not score subject identity, acting, relighting, audio, cuts, aesthetic quality, or initial composition.

Future comparison (NOT RUN): same input and references; prompt A without explicit camera-lock block, prompt B with that block only. Keep other settings fixed; paired seeds where supported and multiple paired trials. Blind landmark annotation. Report trajectory residual, initial-frame position error, worst-frame error, coverage and a separate creative-acceptability assessment. A single A/B cannot separate prompt benefit from generation variability. Forge's full template versus baseline tests a bundle, not the individual value of a 'do NOT inherit' rider.