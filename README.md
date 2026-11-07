# tiltandshift_trial.sh

Structured trial runner for the FFmpeg `tiltandshift` filter.
Source: `art_01M6VWG5T1ANCZWGNZ684437KP` rev 1.

## What it does

| Output file | Filter applied | What to look for |
|---|---|---|
| `00_baseline.mp4` | none (null) | Reference — no effect |
| `01_start_frame_end_frame.mp4` | `start=frame:end=frame` | Clean in/out, time-slice body |
| `02_start_none_end_frame.mp4` | `start=none:end=frame` | Jump/smear at start |
| `03_start_black_end_frame.mp4` | `start=black:end=frame` | Black leader, then effect |

## Usage

```bash
bash tiltandshift_trial.sh in.mp4
```

Outputs go to `results/YYYYMMDD_HHMMSS/` with a `run.log` that records
the FFmpeg version and each trial command.

## Verification checks (from article)

- Baseline differs visibly from trials 01–03: effect is active.
- 01 vs 02: 01 has a held first frame; 02 starts mid-build.
- 01 vs 03: 03 starts with black instead.
- In any trial: far objects move faster than near ones (inverted parallax).

## Limits

- Not executed; source publication only. Test on your own build.
- Output length is undocumented by the FFmpeg manual; measure per trial.
- Needs a suitable source (static background or fast wide-field motion).
- Windows: run under WSL or adapt for PowerShell.

## Next improvement

Add `hold` and `pad` column counts as script parameters so the user can
quickly sweep the transition width without editing the script.