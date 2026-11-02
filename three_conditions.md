# Three-condition keyframe table — save-confirmation panel

Extends Scout's two-condition table (artifact 17c08cad-3709-40cc-be8a-db78adc5cbec).
Computed by Tess; execution artifact: 5645a3d4-db80-459a-9e5a-c8d59965e288.
Source: art_01M6E3C6Y1V0AWGBX85844XT5M revision 1.

## Shared panel (all conditions)
- Travel: 24 px below → 0 px
- Duration: 300 ms
- Easing: cubic-bezier(0.2, 0, 0, 1)   [Corporate archetype]
- Panel settles < 0.1 px at **t ≈ 268 ms**

## Condition A — single arrival
- Supporting text locked to panel; no independent motion.

## Condition B — secondary settle (Scout/Iris brief)
- Extra travel: 9.6 px (40 % of panel travel)
- Delay: 75 ms
- Duration: 300 ms, ease-out cubic-bezier(0, 0, 0.58, 1)
- Text settles < 0.1 px at **t ≈ 375 ms**
- At delay start (t = 75 ms): panel has traveled 60.7 % of 24 px

## Condition B-tight — halved offset + tighter delay (Scout proposal)
- Extra travel: 4.8 px (20 % of panel travel)
- Delay: 40 ms
- Duration: 300 ms, ease-out cubic-bezier(0, 0, 0.58, 1)
- Text settles < 0.1 px at **t ≈ 325 ms**
- At delay start (t = 40 ms): panel has traveled 28.9 % of 24 px

## Discriminating measurement

Scout's key concern: at B's delay start, the panel is 60.7 % through its
travel. B-tight's delay start is at 28.9 % — less than a third traveled,
so the secondary motion begins while primary motion is still pronounced.
The perceptual question changes: does B-tight read as two simultaneous
arrivals at different speeds, or as a single softened arrival?

## 25 ms sample table

| t (ms) | Panel (px) | A text (px) | B text (px) | B−A (px) | B-tight text (px) | Bt−A (px) |
|--------|-----------|------------|------------|---------|------------------|----------|
| 0      | 24.00     | 24.00      | 33.60      |  9.60   | 28.80            |  4.80    |
| 25     | 21.61     | 21.61      | 31.21      |  9.60   | 26.41            |  4.80    |
| 50     | 14.25     | 14.25      | 23.85      |  9.60   | 18.78            |  4.53    |
| 75     | 9.43      | 9.43       | 19.03      |  9.60   | 13.33            |  3.91    |
| 100    | 6.43      | 6.43       | 14.74      |  8.31   |  9.75            |  3.32    |
| 125    | 4.39      | 4.39       | 11.49      |  7.10   |  7.16            |  2.77    |
| 150    | 2.93      | 2.93       |  8.90      |  5.97   |  5.19            |  2.25    |
| 175    | 1.88      | 1.88       |  6.79      |  4.91   |  3.65            |  1.78    |
| 200    | 1.12      | 1.12       |  5.05      |  3.93   |  2.46            |  1.35    |
| 225    | 0.59      | 0.59       |  3.62      |  3.03   |  1.55            |  0.96    |
| 250    | 0.25      | 0.25       |  2.46      |  2.21   |  0.87            |  0.62    |
| 275    | 0.06      | 0.06       |  1.56      |  1.50   |  0.40            |  0.35    |
| 300    | 0.00      | 0.00       |  0.90      |  0.90   |  0.14            |  0.14    |
| 325    | 0.00      | 0.00       |  0.43      |  0.43   |  0.02            |  0.02    |
| 350    | 0.00      | 0.00       |  0.12      |  0.12   |  0.00            |  0.00    |
| 375    | 0.00      | 0.00       |  0.00      |  0.00   |  0.00            |  0.00    |

## Settle summary

| Condition | Text settles < 0.1 px | Observation window needed |
|-----------|-----------------------|---------------------------|
| A         | ≈ 268 ms (panel)      | 300 ms sufficient         |
| B         | ≈ 375 ms              | 400 ms needed             |
| B-tight   | ≈ 325 ms              | 350 ms sufficient         |

Iris's brief specifies a 600 ms window — long enough for all three.
Scout's tighter 400 ms proposal captures B and B-tight but requires
confirming B (375 ms) is inside it before trimming.

## Review-protocol note
Add a fourth question when B-tight is included:
5. Did the heading and supporting line feel like one arrival or two?
Record answer order A → B → B-tight or B-tight → B → A, counterbalanced.