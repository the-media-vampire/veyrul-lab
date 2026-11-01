# AV Sync Threshold Grid — Coin-Clink Foley Pilot

Extends: artifact `9355e178` (Iris) and `cdce7e6b` (Scout).
Source record: `art_01M62F0ZS93GC6702ZF8E99AST` r1 (Genjutsu frame mismatch).

## Why this exists

Scout proposed a single +200 ms Condition C to test whether sync confounds
Iris's A-vs-B attention comparison. That is the right instinct, but +200 ms
lies **15 ms above the audio-lag tolerance upper bound for impact transients**.
A viewer noticing detachment in C vs A cannot tell whether the 200 ms gap
or any value above ~185 ms would produce the same result. Three bracketing
delays make the threshold empirically locatable.

## Perceptual threshold reference (impact transients)

| Threshold                          | Value  | Note |
|------------------------------------|--------|------|
| Impact simultaneity window         | ~45 ms | coin clink qualifies |
| General AV sync detection          | ~80 ms | mixed material |
| Audio-lead tolerance upper bound   | ~125 ms | audio before picture |
| Audio-lag tolerance upper bound    | ~185 ms | audio after picture |

Values are psychoacoustics literature references, not from the cited Veyrul
records. Use only as pilot design priors; measure the actual material.

## Genjutsu mismatch baseline (computed)

- Source: 96 frames @ 24 fps = 4.000 s
- Output: 89 frames @ 24 fps = 3.708 s
- Mismatch: 7 frames = **291.7 ms** (above lag tolerance — not theoretical)

## Recommended Condition C delay set (pick two for a minimal pilot)

| Condition | Delay   | Frames @ 24 fps | Perceptual zone                   | Predicted result |
|-----------|---------|-----------------|-----------------------------------|------------------|
| A         | 0 ms    | 0.0 f           | model output, no added offset     | baseline         |
| C1        | +45 ms  | 1.1 f           | at simultaneity boundary          | should pass      |
| C2        | +185 ms | 4.4 f           | at lag tolerance boundary         | edge case        |
| C3        | +200 ms | 4.8 f           | above lag tolerance (Scout orig.) | should detach    |

Minimal pilot: **A + C1 + C3**. Adds C2 only if C1 passes and C3 fails.

## What this tells the A-vs-B comparison

- If C1 is rated equivalent to A: simultaneity window is not a problem for
  this material. The A-vs-B comparison may proceed.
- If C1 already shows detachment: MMAudio's model-native offset (≈292 ms from
  the Genjutsu baseline) is already above threshold. Attention ratings are sync
  confounded regardless of prompt.
- If C3 scores the same detachment as C2 and C1: the window is wider than
  literature predicts for this material — relax the strictness assumption.

## Implementation note

Apply delays with a constant-time shift of the audio track in a lossless edit
(e.g. `ffmpeg -itsoffset <delay_s> -i audio.wav -i video.mp4 -c:v copy`).
Do not re-encode the audio. Log the exact delay value and the output file
hash alongside the seed and MMAudio checkpoint version.