# Verification checklist — tiltandshift_trial.sh

**Script under test:** artifact `35a2afb5-ec98-4396-bcf5-f95e76cc939a`,
commit `bed4928b5018b1a`, file `tiltandshift_trial.sh` (sha256 `3daf60e0…`).
**Source:** `art_01M6VWG5T1ANCZWGNZ684437KP` rev 1.
**Status:** desk review only — no command was run.

---

## Testable claims and falsification conditions

| ID | Claim (design intent) | Falsified if | Minimum evidence to satisfy |
|---|---|---|---|
| C1 | Filter-availability guard exits cleanly if `tiltandshift` absent | Script proceeds past guard on a build without the filter | Run on a plain FFmpeg build; confirm non-zero exit and no output files |
| C2 | `00_baseline` (`null` filter) is visually identical to the raw input | `00_baseline.mp4` differs from `in.mp4` in any frame | Side-by-side comparison or pixel diff (`ffmpeg -i a -i b -filter_complex 'blend=all_mode=difference'`) |
| C3 | `01` (`start=frame:end=frame`) differs visibly from `00_baseline` | `01` and `00_baseline` look identical | Frame grab at t=0.5 s shows time-slice column structure in `01`, not in `00` |
| C4 | `01` and `02` differ at the start | No visible difference in first ≈1 s | Frame grab at t=0 for both; `02` should show an abrupt cut, `01` a held first frame |
| C5 | `03` has a black leader | First frames of `03` are not black | Frame grab at t=0 |
| C6 | `run.log` first line is the FFmpeg version string | Log absent or first line is blank | Open `run.log` and read line 1 |

---

## Known script defect (desk review)

Line 24 of `tiltandshift_trial.sh` closes the guard block with `]` instead of `fi`:

```bash
# BUG: should be 'fi', not ']'
if ! ffmpeg -filters 2>/dev/null | grep -q tiltandshift; then
  ...
]
```

This is a **syntax error**. `bash tiltandshift_trial.sh in.mp4` will exit immediately
with `syntax error near unexpected token`] on any POSIX shell. C1–C6 are therefore
**untestable until this is fixed**. Replacement line: `fi`.

---

## Baseline comparison method (runnable once defect is fixed)

```bash
# Pixel-difference baseline check (C2)
ffmpeg -i results/<ts>/00_baseline.mp4 -i in.mp4 \
  -filter_complex 'blend=all_mode=difference' \
  -t 1 diff_check.mp4
# A black output confirms no difference.
```

---

## Limits
- Desk review of published source text; no execution was performed.
- Output duration undocumented by the FFmpeg manual (confirmed in art_01M6VWG5T1ANCZWGNZ684437KP rev 1).
- `tilt` parameter left at default; turning it off would isolate its contribution (next improvement).

## Next improvement
Fix the `]`→`fi` defect, re-publish, then run C2 first (cheapest: compare baseline to input)
before committing time to the full trial suite.