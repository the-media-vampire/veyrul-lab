# Verified keyframe values

Derived from execution artifact `50069672-3c2d-4143-a8be-99d16bfb328c`.
Source: art_01M6E3C6Y1V0AWGBX85844XT5M revision 1.

## Shared panel (both A and B)
- Travel: 24 px below → 0 px
- Duration: 300 ms
- Easing: cubic-bezier(0.2, 0, 0, 1) (Corporate, per repository table)
- Panel settles < 0.1 px at **t ≈ 268 ms**

## Version B — supporting-text secondary motion
- Additional travel: 9.6 px (40 % of panel travel)
- Delay: 75 ms
- Duration: 300 ms, ease-out = cubic-bezier(0, 0, 0.58, 1)
- Text settles < 0.1 px at **t ≈ 352 ms** (84 ms after panel)
- Peak B–A displacement: 9.60 px at t = 0 ms

## 25 ms sample table

| t (ms) | Panel Y (px) | A text Y (px) | B text Y (px) | B−A (px) |
|--------|-------------|--------------|--------------|----------|
| 0      | 24.00       | 24.00        | 33.60        | 9.60     |
| 25     | 21.61       | 21.61        | 31.21        | 9.60     |
| 50     | 14.25       | 14.25        | 23.85        | 9.60     |
| 75     | 9.43        | 9.43         | 19.03        | 9.60     |
| 100    | 6.43        | 6.43         | 14.74        | 8.31     |
| 125    | 4.39        | 4.39         | 11.49        | 7.10     |
| 150    | 2.93        | 2.93         | 8.90         | 5.97     |
| 175    | 1.88        | 1.88         | 6.79         | 4.91     |
| 200    | 1.12        | 1.12         | 5.05         | 3.93     |
| 225    | 0.59        | 0.59         | 3.62         | 3.03     |
| 250    | 0.25        | 0.25         | 2.46         | 2.21     |
| 275    | 0.06        | 0.06         | 1.56         | 1.50     |
| 300    | 0.00        | 0.00         | 0.90         | 0.90     |
| 325    | 0.00        | 0.00         | 0.43         | 0.43     |
| 350    | 0.00        | 0.00         | 0.12         | 0.12     |
| 375    | 0.00        | 0.00         | 0.00         | 0.00     |

## Discriminating question
At t = 75 ms the panel has already moved 14.57 px (61 %) of its travel
but the secondary motion has not yet begun. Does a user perceive the
supporting text as "behind" the panel at that moment?
If yes, B reads as two arrivals; the brief's decision rule favors A.