# ASS Timing Adapter — Interface Contract

## Upstream interface (alignment output)
- Unit: milliseconds (integer)
- Assumption: positive duration guaranteed in ms domain
- License: depends on aligner; not redistributed here

## Downstream interface (ASS converter)
- Unit: centiseconds (floor division by 10)
- Assumption: start_cs < end_cs; zero-duration events are dropped
- Source: words_to_ass.py rev 5496e6c (art_01M6V2D44ND0QGWCJW3GWYSKXF r1 Case 9)

## Adapter layer (this module)
- Sits between alignment output and ASS converter
- Makes collapse policy explicit: DROP | CLAMP | MERGE
- Precondition check: call check_collapse() before passing to converter
- Does NOT fix alignment accuracy or synthesis quality

## Known assumptions
1. Quantization is floor, not round — a [105, 115] ms word is safe (10→11 cs)
2. CLAMP may produce overlapping events if adjacent words share a centisecond bucket
3. MERGE changes word boundaries — downstream word-highlight timing will differ
4. This adapter addresses format boundary only; Cases 1–8 are separate mechanisms

## What this does NOT establish
- Karaoke alignment accuracy (Case 3)
- Vocal separation quality (Case 3)
- Any ACE-Step Studio behavior (upstream_report_not_reproduced per source)