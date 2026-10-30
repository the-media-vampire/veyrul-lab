# disc_prompt_scorer

A lightweight prompt discipline checker for Seedance single-prop scene coverage.

## Source
Derived from observations in **art_01M64VKZ36V70FHZ5PHSM9651S revision 2** (Veyrul).  
Eight Seedance 2.5 runs on 25 September 2026 showed that one named place and one  
explicit single-disc reference across all prompts kept the prop count stable.

## Checks (0–4)
| Flag | What it looks for |
|---|---|
| `place` | Named location token (ramp, red-brick school, railing…) |
| `single_disc` | Explicit singular disc phrasing |
| `no_multi` | Absence of "discs", "two discs", etc. |
| `anchor_char` | Anchor character marker (orange tee/tank top) |

**Score < 3 → warning.** Score 4 = fully disciplined.

## Baseline comparison (executed)
- Unconstrained baseline ("A man throws a frisbee…"): **2/4**
- Four disciplined shot prompts: **3.75/4 mean**
- Delta: **+1.75 points**

## Limits
- Text heuristic only; does not predict rendering fidelity.
- Token lists are scene-specific; extend for other props/places.
- No multi-shot sequencing logic; each prompt scored independently.

## Next improvement
Add a shot-type field (throw / pickup / arrival / vault) and check that  
all four appear across a prompt set before submission.