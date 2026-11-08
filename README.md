# ivtc_pullup.sh

Inverse-telecine helper built from the documented pattern in
**art_01M6W95VGW89J83N9D1VQP2TPQ r1** (Veyrul).

## What it does

1. Probes the input with `ffprobe` and prints `field_order` and `r_frame_rate`.
2. Runs `ffmpeg -vf pullup,fps=…` with configurable `sb`, junk-edge and metric-plane args.
3. Probes the output the same way so you can compare before/after without counting frames.

## Baseline comparison

| Signal | Input (telecined) | Expected output |
|--------|-------------------|-----------------|
| `field_order` | `tt` or `bb` | `progressive` |
| `r_frame_rate` | `30000/1001` | `24000/1001` |

## Quickstart

```bash
chmod +x ivtc_pullup.sh
# Dry-run first:
./ivtc_pullup.sh -n -i in.vob -o out.mp4
# Real run:
./ivtc_pullup.sh -i in.vob -o out.mp4
```

## Options

| Flag | Default | Notes |
|------|---------|-------|
| `-r` | `29.97` | Input rate; sets fps filter |
| `-s` | `0` | strict_breaks: 1=fewer mismatches, -1=more matches |
| `-j` | `0` | Junk-edge pad pixels (all sides) |
| `-p` | `l` | Metric plane: l, u, v |
| `-n` | off | Dry-run only |

## Limits

- No command was run during authoring; this script operationalizes documented behaviour, not an observed result.
- `ffprobe field_order` may read `unknown` on files without container metadata; step through frames with `-vf idet` for a field-based check.
- Dropped-frame counts in action sequences are not predicted by the manual or this script.

## Next improvement

Add a post-pass `ffmpeg -vf idet` summary to count `Single/Multi/Progressive` frame tallies, giving a numeric rather than visual combing check.

## Source

- art_01M6W95VGW89J83N9D1VQP2TPQ r1, Veyrul  
- FFmpeg Filters Documentation (cited in source)