# pullup `sb` decision table

Source: art_01M6W95VGW89J83N9D1VQP2TPQ r1 (documentary review; no command run)

## Two-check protocol

Neither check alone is sufficient:

| Check | Tool | Signal | Limitation |
|---|---|---|---|
| Format compliance | `ffprobe` | `field_order=progressive`, `r_frame_rate=24000/1001` | Reports container metadata, not frame content |
| Frame-level combing | `ffmpeg -vf idet` | Residual interlaced frame ratio | Automated detector; does not capture motion damage |

**Minimum evidence pair:** both checks on the same bounded clip interval.

## Decision table

Record all three columns before changing `sb`. Prefer the first row that fits.

| Observed symptom | idet residual interlaced ratio | Motion discontinuities | Recommended sb | Rationale (source) |
|---|---|---|---|---|
| No combing, smooth motion | < 2 % | None noted | Keep current setting | No evidence of a problem |
| Leftover interlaced frames, smooth motion | ≥ 2 % | None noted | Try `sb=0` then `sb=1` | Stricter matching reduces mismatches |
| No combing, motion judder or frame jumps | < 2 % | Present | Try `sb=-1` | Easier matching reduces frame loss |
| Leftover frames AND motion judder | ≥ 2 % | Present | Re-examine source; mixed content likely | Trade-off is irreconcilable at a single sb value |

## Rationale for the 2 % threshold

This is a **proposed working threshold**, not a source-documented value. It is intended to distinguish incidental detector noise from systematic residual interlacing. Replace with a content-appropriate value once a baseline is measured.

## Collecting the idet count

```sh
# Probe a bounded interval (seconds 10–40 of the output)
ffmpeg -ss 10 -t 30 -i out.mp4 -vf idet -f null - 2>&1 | grep 'Multi\|Single\|Progressive'
```

Record the raw frame counts, not just the label. Compute the residual interlaced ratio as:

    (Single interlaced + Multi interlaced) / Total frames inspected

## Limits

- No command was run during authoring.
- `idet` can misclassify frames in low-motion scenes; count undecidable frames separately.
- Motion discontinuities require human inspection or a reference frame-difference metric; this table does not automate that check.
- The 2 % threshold is provisional; update it after measuring at least one baseline/candidate pair.

## Relationship to peer artifacts

- Forge artifact `7edb36e8-2fe1-4ee1-9861-1689bafbab82` (commit `8fed447`): wraps the ffprobe format check. This table adds the idet layer and the sb selection logic.
- Delta scorecard (inline, unrun): proposed the same two-check separation. This table operationalises that separation with a numeric threshold and a decision rule.