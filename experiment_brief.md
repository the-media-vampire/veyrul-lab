# Per-Frame Displacement Experiment Brief

## Source
art_01M6QAFXM1NHAWKJGDSKRG0HWM revision 1 — documentary reading of eBook 45231
(Horstmann & Tousley, Motion Picture Operation, 1914, Gutenberg plain text)

## Discriminating Question
Does LTX image-to-video maintain approximately constant per-frame displacement
for subjects moving at different speeds, or does apparent motion degrade for
fast vs. slow subjects?

## Book Basis (documented claims, not our assertions)
- Lines 1546-1551: pictures of faster/slower objects should keep displacement
  between pictures "about the same or at least not any more."
- Lines 1536-1540: "a swiftly thrown ball appears slower" — fast subjects
  compress apparent motion; slow subjects elongate it.
- Lines 1543-1546: a walking person moves ~3 inches per 1/16s exposure; motion
  looks even unless the walker is too close.
- Lines 1574-1580: too long a bright (stationary) period causes flicker;
  the book uses a shutter. AI video has no shutter — model must learn this.

## Hypothesis
An AI model trained on natural video has implicitly learned speed-appropriate
displacement for common subjects. It may handle slow subjects (leaf, smoke)
better than fast subjects (thrown ball, sprinting figure) because fast-motion
training examples are rarer and motion blur is harder to render consistently.

## Two Contrasting Conditions (hold all other variables fixed)
| Condition | Subject | Expected displacement per frame |
|-----------|---------|--------------------------------|
| A: Slow | A single autumn leaf drifting downward in still air | Small, uniform |
| B: Fast | A baseball thrown across frame, mid-arc | Large, potentially inconsistent |

Same seed image (neutral grey background), same 5-second clip length,
same prompt structure — only subject and speed differ.

## What to Inspect (frame-by-frame, not taste)
1. Extract frames at regular intervals (e.g., every 8 frames at 24fps).
2. For each pair of consecutive sampled frames, estimate displacement of the
   subject's centroid (pixels).
3. Plot displacement over time: flat = uniform; spiky = inconsistent.
4. Note any luminance flicker (global brightness jump between frames) —
   the book's flicker is a light/dark alternation; model flicker is analogous.
5. Note smear, ghosting or positional stutter separately from taste.

## Informative Failure Definition
- Condition B shows non-uniform displacement (spiky plot) while Condition A
  does not: confirms the hypothesis.
- Both conditions fail equally: model does not learn speed-appropriate motion.
- Both succeed: null result for this test; try higher speed (sprinting, projectile).

## What This Cannot Show
- A single still frame shows only one settled position (book lines 1510-1514);
  flicker and apparent motion are frame-sequence phenomena only.
- No claim that the book's figures (1/16s, 4/80s, 1/80s) apply to AI video;
  they are reported as the book's own figures at its own time.
- No audio, voice, likeness or real person is involved.

## Curator Status
Checklist and hypothesis: untested curator analysis. No film viewed,
no execution at time of publication.