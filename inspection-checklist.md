# Inspection checklist — A vs B attention-timing experiment

Ref: [art_01M6ABAW1XPPHFY83FJRMNPCJZ revision 1], [rpl_01M6AC9XBP83WAA4GAXNCS2A32]

## Structural verification (done in Python before publishing)
- Exactly 7 lines differ: composition ID, comment, data-start, data-duration, timeline offset, hold duration, __timelines key
- All else fixed: canvas, fonts, colors, positions, headline text, supporting text, fade duration (0.3 s)

## Frame checkpoints to inspect after rendering
| Frame | Time | What to check |
|-------|------|----------------|
| 0     | 0.00 s | Headline only in A; both lines in B (at opacity near 0 — watch for flash) |
| 9     | 0.30 s | B's supporting line fully visible; A still headline-only |
| 35    | 1.17 s | A: still headline-only (one frame before supporting starts) |
| 36    | 1.20 s | A: supporting begins fade |
| 45    | 1.50 s | A: supporting fully visible |
| 149   | 4.97 s | Both: final hold frame |

## Viewer probe questions (counterbalanced presentation order)
1. "What did you read first?"
2. "Did the second line feel reassuring, redundant, or late?"

## Discriminating test Iris identified but did not specify
The 1.2 s gap is the key variable. A rival hypothesis: the delay feels *sluggish* rather than *intentional* above ~0.8 s.
To test that, add version C with data-start="0.6" — half the delay. If C scores best on 'intentional', the effect is non-monotone and 1.2 s is too long. If A and C tie above B, delay itself is the driver.

## Decision rule (from Iris)
Prefer A only if delay preserves comprehension and feels intentional not sluggish. Otherwise retain B.