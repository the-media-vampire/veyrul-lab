# Frame Rule Checker

Encode video-generation prompt rules as `Rule` objects, record still-frame observations as `FrameObs`, call `check()` to get MATCH / MISMATCH / AMBIGUOUS / NOT_VERIFIED.

## Source
Observations transcribed from **art_01M6A19D9WCBJFN6YNNXNTP570 r2** (stills only, no playback, no audio). Model labels as project pages declare; underlying models not verified. Upstream clip rights belong to their owners; no frames or full prompts reproduced.

## Baseline (execution receipt d12fe5e1-7ac7-439c-aa93-f67997dff1b4)
```
MATCH=5  MISMATCH=4  AMBIGUOUS=2  (11 rules, 4 clips)
```
Slip pattern: colour states, prop negations, lighting prohibitions, and person-count first-frame rules each produced a MISMATCH; cast lists and blocking held.

## Limits
- Stills cannot show motion, cuts or audio.
- AMBIGUOUS = partially visible; NOT_VERIFIED = state unreadable in still.
- These are this tool's encodings of the article, not the creators' own assertions.

## Next improvement
Add a new Rule+FrameObs pair for a reworded clause (e.g. positive prop description vs. `"no lid"`), run `score_clip`, compare MISMATCH rate to baseline.