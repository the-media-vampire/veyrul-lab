# lenscorrect_trial.sh

Operationalises **art_01M6V5QZG15J2GQABEBQVQ8GBK r1** (FFmpeg lenscorrection guide).

## What it does

1. **Baseline pass** – runs `lenscorrection=k1=0:k2=0` (documented no-op) so you have a reference output identical to source.
2. **Correction pass** – runs with your chosen k1/k2 and bilinear interpolation.
3. Prints verification prompts: side-by-side playback, sign-flip hint, edge-fill note.

## Usage

```bash
chmod +x lenscorrect_trial.sh
./lenscorrect_trial.sh clip.mp4            # uses k1=-0.2 k2=0 (illustrative)
./lenscorrect_trial.sh clip.mp4 -0.3 0    # explicit trial
./lenscorrect_trial.sh clip.mp4 -0.15 0.02 # two-coefficient trial
```

## Baseline comparison logic

| Output | Filter | Expected result |
|---|---|---|
| `baseline_<input>` | k1=0, k2=0 | Identical to source (documented default = no correction) |
| `corrected_k1_<k1>_k2_<k2>_<input>` | Your values | Reduced barrel/pincushion |

If baseline differs from source, something else in the pipeline is active — check your ffmpeg version and filter chain.

## Limits

- Trial k1/k2 values are illustrative; the article documents the range (-1 to 1) not optimal values.
- No command was run during authoring; test against your own clip.
- Lens-profile correction via lensfun is not covered (see source article).
- Record your ffmpeg version with every result — the manual carries no page version.

## Sources

- art_01M6V5QZG15J2GQABEBQVQ8GBK r1 (Veyrul)
- FFmpeg Filters Documentation (https://ffmpeg.org/ffmpeg-filters.html), captured 2026-11-07