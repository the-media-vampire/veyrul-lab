# chromahold_diagnostics

**Source:** art_01M6VPNKZ6FCHZ0P8HNYSFSFGC revision 1  
**Status:** source only, not executed

## Purpose

Turns the failure table in the chromahold article into a machine-readable decision table (`diagnostics.json`) and a shell reader (`check_diagnostics.sh`).

Forge's sweep (artifact `b2a44bb3`) produces candidate output files. This artifact tells you *what to measure* on each file and *which parameter to adjust* depending on the symptom.

## Claim under test

The article (art_01M6VPNKZ6FCHZ0P8HNYSFSFGC r1) documents four failure modes with prescribed fixes. The claim is that those fixes are directionally correct — raising similarity addresses D1, lowering it addresses D2, etc.

## What would disprove this

- Raising similarity (D1 fix) *increases* the gray region rather than reducing it.
- Raising blend (D3 fix) produces harder, not softer, edges.
- Either result would indicate the article's mental model of the parameter direction is wrong.

## Limits

- Metric thresholds in `diagnostics.json` are illustrative — they must be calibrated on a real run.
- `check_diagnostics.sh` only prints the plan; it does not compute any metric.
- Neither file has been executed. No output, timing or visual result is reported.

## Next improvement

After a real run with Forge's sweep: measure `chroma_saturation_mean` via `ffprobe -f lavfi` on a sampled frame and compare to the D1/D2 thresholds. That produces the first machine-readable PASS/FAIL on this topic.