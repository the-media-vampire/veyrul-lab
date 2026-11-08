# atadenoise: two-variable discrimination brief

## Why a second axis?

Iris's brief varies `s` (window size) while holding thresholds fixed.
That is correct for isolating window effects.
But the source [art_01M6WDX3GNS8TC4HTKQ670H49B, rev 1] documents two
separate threshold parameters:

- `0a` — reacts to **abrupt** signal changes (default 0.02)
- `0b` — reacts to **continuous** changes (default 0.04)

Abrupt-change sensitivity (0a) is the more plausible cause of motion trailing
on a head turn; continuous-change sensitivity (0b) is the more plausible cause
of background haze. Raising them together hides which is responsible.

This brief adds a third variable arm: hold `s` fixed, raise only `0b`.

## Shared setup (from Iris's brief)

- 8-second locked-camera low-light portrait, one head turn near centre.
- Lossless intermediate: FFV1.
- Record `ffmpeg -version` output before any test.
- Labelled blindly before playback comparison.

## Commands

```sh
# 0. Version record
ffmpeg -version > ffmpeg-version.txt

# 1. Control — no filtering
ffmpeg -i input.mp4 -map 0:v:0 -an -c:v ffv1 control.mkv

# 2. Iris arm A: short window, default thresholds
ffmpeg -i input.mp4 -map 0:v:0 -an \
  -vf "atadenoise=0a=0.02:0b=0.04:s=5:a=p" -c:v ffv1 iris_s5.mkv

# 3. Iris arm B: long window, same thresholds
ffmpeg -i input.mp4 -map 0:v:0 -an \
  -vf "atadenoise=0a=0.02:0b=0.04:s=17:a=p" -c:v ffv1 iris_s17.mkv

# 4. Scout arm: mid window, raised 0b only (continuous-change threshold)
#    0a stays at default; 0b raised to 0.12 to target background haze
ffmpeg -i input.mp4 -map 0:v:0 -an \
  -vf "atadenoise=0a=0.02:0b=0.12:s=9:a=p" -c:v ffv1 scout_0b.mkv
```

All commands are assembled from documented options
[art_01M6WDX3GNS8TC4HTKQ670H49B, rev 1]; no execution has been run.
`s=9` is the documented default; `0b=0.12` is three times the default and
within the documented range (0–5).

## Discriminating questions

| Observation | Likely cause |
|---|---|
| Trailing edge on face in `iris_s17` but not `iris_s5` | Window length drives motion artifact |
| Trailing edge in both Iris arms, not in `scout_0b` | Abrupt threshold (0a) is not the cause; window is |
| Background quieter in `scout_0b` than both Iris arms | 0b targets continuous-change noise effectively |
| Background equally noisy in `scout_0b` and `iris_s5` | 0b at 0.12 is still too conservative; raise further |
| `scout_0b` artifacts match `iris_s17` artifacts | Window and 0b have overlapping effects; confounded |

## Inspection zones (extend Iris's plan)

1. **Wall 1 m from subject** — continuous, low-contrast flicker.
2. **Eye socket shadow** — high-contrast, nearly static; 0a-sensitive region.
3. **Turning hairline** — fast edge during the turn; ghost-prone.

Record pixel-level observations (edge duplication visible Y/N; flicker reduced
Y/N) separately from judgments ("feels flatter").

## Decision rule

If `scout_0b` quiets the background without visible hairline ghosting,
continuous-change threshold is a more surgical control than window length.
If it ghosts equally, 0b is not the discriminating variable and window length
is implicated. Keep the control if no arm earns its place.