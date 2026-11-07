# Experiment Brief: Circular vs. Linear Heading Interpolation

**Source:** art_01M6VDTP1SRA5R2KX5NW9H0D13 revision 1  
**Lens:** Which *smallest* test most changes our belief about the bug?

## Intention
Isolate interpolation strategy as the single variable.  
All other fixture values are identical between conditions.

## Contrasting Alternatives
| Strategy | RMSE for +179 vs -179 pair | Midpoint at t=0.25 |
|---|---|---|
| Linear subtraction | ~358 deg | 0 deg (wrong) |
| Shortest-arc wrap | ~2 deg | ~179 deg (correct) |

## Discriminating Question
If we observe RMSE ≠ 358 under linear strategy, the fixture is wrong.  
If circular RMSE ≠ 2, the wrap formula is wrong. Each failure points differently.

## What This Does NOT Test
- Phase-matched sampling (separate variable)
- Missing-data masking (separate variable)
- Nonperiodic capture guard (separate variable)
- Blender, rig, or animation assets (out of scope)

## How to Run
```
python heading_interp_experiment.py
```
Requires: Python 3.8+, NumPy. Runtime ~0.01s.

## Technical Observation (documented, not taste)
The midpoint error is the more surprising diagnostic: 179 and -179 average to 0  
under linear blend, not to 180. This is a silent magnitude error, not just an  
outlier—it would corrupt interpolated comparison traces at every phase step.

## Taste Note (separated)
The circular fix is elegant. That is not evidence it is correct; the regression  
tests in the upstream PR are the actual check.