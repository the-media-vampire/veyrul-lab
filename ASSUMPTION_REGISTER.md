# Assumption Register

**Status:** source document only; nothing executed. Cite `artifact_id` (this artifact) when referencing.

## Closed assumptions (source-evidenced)

| # | Assumption | Evidence | Record |
|---|---|---|---|
| A1 | xfade needs identical resolution, pixel format, frame rate, timebase | filters.texi lines 25910-25911 | art_01M6QCH5HCZQAKZYA8969JTZ2X r1 |
| A2 | xfade duration range: 0–60 s | filters.texi lines 25983-25985 | art_01M6QCH5HCZQAKZYA8969JTZ2X r1 |
| A3 | blackdetect log line requires min_duration threshold; metadata does not | filters.texi lines 8682-8693 | art_01M6QCH5HCZQAKZYA8969JTZ2X r1 |
| A4 | freezedetect: freeze_start timestamp is from a different frame | filters.texi lines 14556-14561 | art_01M6QCH5HCZQAKZYA8969JTZ2X r1 |
| A5 | adjust_subs_for_join.py raises on negative cue start | source read of f7585111 at 9611ed61 | Theo, Veyrul |

## Open assumptions (unresolved)

| # | Assumption | Blocker | Required for |
|---|---|---|---|
| B1 | ffsubsync returns machine-readable offset or confidence | rqr_01M6RARG0V9XNQ4FTZYK8GC9SN (proposed, not authorized) | Deterministic failure detection in stage 3 |
| B2 | acrossfade placement can be aligned with xfade offset | No mechanism documented in filters.texi | Audio sync correctness across join |
| B3 | Cues with .start == offset_ms are correct to leave unshifted | Boundary behavior not documented in pysubs2 or FFmpeg docs | Edge-case subtitle correctness at join frame |
| B4 | int() truncation matches FFmpeg's internal ms rounding | Not tested | Millisecond-accurate cue placement |

## Recovery instructions

Another agent can verify this chain by:
1. Reading `art_01M6QCH5HCZQAKZYA8969JTZ2X r1` for FFmpeg filter claims.
2. Reading artifact `f7585111-bfd0-48be-8fc5-0f6c37f7c73a` at commit `9611ed61` for the subtitle-shift source.
3. Checking `rqr_01M6RARG0V9XNQ4FTZYK8GC9SN` state to learn if B1 resolved.
4. Treating B2–B4 as open until a source or test closes them.