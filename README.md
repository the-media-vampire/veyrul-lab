# FFmpeg vibrance: intensity × alternate experiment brief

Source: art_01M6W6JQ5FA6YDBG4870H0VC7A revision 1

## The discriminating question

The guide states: *with negative intensity, `alternate=1` makes colours change; otherwise they become less saturated, toward gray.*  
That is an untested claim. This brief isolates it as a 2×2 matrix.

## Hypothesis pair

| Condition | Prediction |
|---|---|
| `intensity=-0.5`, `alternate=0` (default) | Colours move toward gray |
| `intensity=-0.5`, `alternate=1` | Colours shift (hue or value change, not mere desaturation) |

If both conditions produce identical output, the `alternate` flag has no observable effect at this intensity — that is a surprising, informative failure worth recording.

## Commands (assemble from documented options; no example exists in the manual)

```bash
# Record FFmpeg build first
ffmpeg -version > ffmpeg_version.txt

# A: baseline — no filter
ffmpeg -i in.mp4 -vf null out_A_baseline.mp4

# B: negative intensity, alternate off (default desaturation path)
ffmpeg -i in.mp4 -vf vibrance=intensity=-0.5:alternate=0 out_B_neg_no_alt.mp4

# C: negative intensity, alternate on (hue-shift path)
ffmpeg -i in.mp4 -vf vibrance=intensity=-0.5:alternate=1 out_C_neg_alt.mp4

# D: positive intensity as orientation check
ffmpeg -i in.mp4 -vf vibrance=intensity=0.5 out_D_pos.mp4
```

## What to measure

- Visually: compare a skin-tone region and a saturated primary between A, B, C.
- Numerically (optional): `ffprobe` or a histogram filter on each output to record mean chroma.
- Key discriminator: do B and C differ? If not, `alternate` is inert at this value.

## Control discipline

Change only one variable between B and C (`alternate`). Keep intensity, source clip, codec and container identical. This is the minimum test to attribute any observed difference to `alternate` alone.

## Suggested clip properties

- Contains skin tones AND a saturated colour patch (e.g. a coloured mug or plant).
- Short: 2–5 seconds is enough.
- Use a lossless or near-lossless intermediate to avoid re-encode artefacts masking the filter effect.

## Evidence status template (fill in after running)

| Condition | Observed result | Notes |
|---|---|---|
| A baseline | — | |
| B neg, alternate=0 | — | |
| C neg, alternate=1 | — | |
| D positive | — | |
| B vs C differ? | — | |

## Limits
- Commands assembled from documented options (art_01M6W6JQ5FA6YDBG4870H0VC7A r1); no command was run here.
- The manual gives no luma-coefficient ranges or worked examples.
- Results depend on FFmpeg build; record version with every trial.