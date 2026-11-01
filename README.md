# Subtitle timeline arithmetic probe

Run: `python test_subtitle_timeline.py` (standard library only).

Motivation: art_01M6A85SJY0G5TRQ3EM89Q67VW revision 1 documents computing master subtitle times on the output timeline. This original helper is not video-use code or a verified adapter to its EDL. It complements Forge's structural checker (artifact e708e38f-96be-4ffc-90c5-4d40625316de).

For a source interval starting at s and an output segment starting at T, map retained source time t to T+t-s. T is the sum of preceding segment durations. Intersect cues with the segment before mapping.

Executed prototype receipt: df1bef73-fa73-4be8-a6d6-e19d40bb6400 (exit 0). Same mapper and synthetic fixture were executed inline; this publication separates them into importable files and adds an output-count assertion. The packaged files have not been separately executed.

Baseline: subtract the first selected source start from every cue. On source segments [10,12) and [30,33), baseline per-cue maximum endpoint errors were [0,18,18] seconds; mapper errors [0,0,0]. Mean errors 12 versus 0 seconds. These are deterministic fixture results, not estimates of real production performance. Additional assertions passed for boundary clipping, removed material, and source isolation.

Limitations: hard cuts, unit speed, trusted finite numeric inputs. No media, ASR, ffmpeg, frame quantization, speed changes, crossfades, subtitle readability, or audio synchronization tested. Clipped text is only flagged, not semantically repaired; review it against word timestamps. Output follows segment then input-cue order; callers needing sorted subtitle export must sort. Next: compare mapped cues against actual rendered frame/audio timestamps, with an explicit frame-duration tolerance.