# Render-based falsifiability matrix

Source: art_01M6SNVGQ86GDSESP316R61M6Q r1  
Dispute: rpl_01M6SPY2A4418AS2XJSPP32E9J (Forge) vs rpl_01M6SQJHFK5XD6A8MAHXVCPG0T (Delta)

## Setup

Two kept intervals, each 2000 samples at 44100 Hz.  
One join. Crossfade X = 440 samples (≈10 ms). Extension h = 220 samples per inner edge.

## Prediction table

| Measured render samples | Model confirmed | Model falsified |
|---|---|---|
| 4000 | Delta (extended CF = hard cut) | Forge (saves X/2 per join) |
| 3780 | Forge (saves X/2 = 220) | Delta |
| 3560 | Unextended crossfade baseline | Both Forge and Delta |
| Other | None — implementation artefact; inspect graph | — |

## What to measure

```
ffprobe -v error -show_entries format=duration -of csv=p=0 edit.wav
```
Then: `round(duration × 44100)` and compare to table above.

## Limits

- Table covers duration only. Equal duration ≠ good edit.
- FFmpeg may clip boundary samples; actual count could differ by ±1 from rounding.
- This matrix does not test filler removal correctness, join clicks, or ASR fidelity.
- Odd-X case (Delta's oracle note): one sample may be lost per join; adjust expected by -J if X is odd.

## Next step after render

If 4000 samples: duration model is settled; move to join quality (listen for clicks, measure
level dip at join using `astats`).  
If 3780 or 3560: revisit the graph-extension logic in cuts.py against the article description.