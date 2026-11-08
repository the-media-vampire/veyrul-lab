# Variable control log

One variable changes between arms. Everything else stays fixed.

| Parameter | Arm A | Arm B | Arm C |
|-----------|-------|-------|-------|
| Input image | sheet_5x5.png | sheet_5x5.png | sheet_5x5.png |
| Actual grid | 5x5 | 5x5 | 5x5 |
| Declared layout | 5x5 ✓ | 4x5 (wrong cols) | 3x5 (non-dividing) |
| Input -r | 1 | 1 | 1 |
| Encoder | FFV1 (mkv) | FFV1 (mkv) | FFV1 (mkv) |
| **Variable** | — | column count | divisibility |

## Why three arms instead of two

Arm B (wrong but integer-dividing) and Arm C (non-integer-dividing) test
distinct conditions. Collapsing them into one arm would prevent distinguishing
whether FFmpeg detects non-divisibility specifically or just misaligns silently
in both cases.

## Do not change between arms

- Do not swap the input image.
- Do not change the encoder.
- Do not change -r on the input.
- Record FFmpeg version once; it must be the same for all three arms.