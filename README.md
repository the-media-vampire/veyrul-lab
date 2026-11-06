# FFmpeg xfade+acrossfade ↔ subtitle-sync: integration contract

Source: art_01M6QCH5HCZQAKZYA8969JTZ2X r1 (documented, not tested; nothing run, no clip viewed).
Prior pipeline proposal: Theo memory 08d48074 (untrusted peer context).

## The join problem

After an xfade join at `offset` seconds with `duration` seconds of overlap:
- Clip-1 subtitle cues past `offset` are early by `duration` seconds.
- Clip-2 subtitle cues are early by `offset` seconds.
Neither ffsubsync nor pysubs2 knows the join happened.

## Interface table

| Boundary | Signal | Failure mode |
|---|---|---|
| xfade offset | CLI float (seconds) | No cross-check with acrossfade placement (gap: filters.texi 575 vs 25988) |
| Joined video | Filesystem path | blackdetect skips log if black < 2.0 s default; metadata still added |
| freezedetect | Frame metadata | freeze_start key on one frame holds timestamp of another (filters.texi 14557) |
| ffsubsync output | SRT path | Exits zero when offset > max-offset-seconds; pysubs2 loads silently |
| Adjusted SRT | SRT path | No validation cues were shifted for the join |

## Preconditions

1. Both clips meet xfade constraints: same resolution, pixel format, frame rate, timebase, CFR.
2. xfade `offset` and `duration` are known before subtitle adjustment.
3. acrossfade alignment with xfade offset confirmed by builder (undocumented in source).
4. ffsubsync `--max-offset-seconds` covers the actual offset; default 60 s may be too small.
5. Subtitles synced to source clip timeline *before* the join, not after.

## Open gaps

- Transition list (filters.texi 25918-25979) not read in r1.
- afade curve types (line 593) not read.
- ffmpeg-utils manual (line 587) not read.
- COPYING files not read; licence coverage of filters.texi unknown.
- ffsubsync sync-confidence output: README documents none (prior proposal).