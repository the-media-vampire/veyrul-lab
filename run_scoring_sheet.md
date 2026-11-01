# Red-light Flanking Composition — Run Scoring Sheet

**Source:** `art_01M64VKA89R1TZMNK0QSJW990E` revision 2  
**Claim under test:** Three text-only Seedance 2.5 runs each opened on a single red light source (slab / line / wheel) flanked by hooded black silhouettes.  
**Status of claim:** Retrospective observation (H01, sampled frames). Not a benchmark. No seed set recorded.

---

## Run metadata

| Field | Value |
|---|---|
| Run date (UTC) | |
| Model / version | |
| Prompt hash or label | |
| Seed (if set) | |
| Frame sample method | |

---

## Prompt anatomy (fill before scoring frames)

| Element | Present? | Exact wording used |
|---|---|---|
| Red light type named (slab / line / wheel / other) | Y / N | |
| Hooded figures explicitly named | Y / N | |
| Silhouette darkness explicitly named | Y / N | |
| Flanking / framing position named | Y / N | |
| Dark background / forest / mist named | Y / N | |
| Anime / cinematic style named | Y / N | |

**Hypothesis:** Rows where all six are N form the baseline (emergent). Rows where 1–3 are Y test partial guidance. Rows where 4–6 are Y test full specification.

---

## Per-frame observation table

Fill one row per sampled frame.

| Frame # | Timestamp (s) | Light source visible? | Light source type | Silhouette(s) visible? | Count | Flanking position (L/R/both/none) | Notes |
|---|---|---|---|---|---|---|---|
| 1 | | | | | | | |
| 2 | | | | | | | |
| 3 | | | | | | | |
| 4 | | | | | | | |
| 5 | | | | | | | |
| 6 | | | | | | | |
| 7 | | | | | | | |
| 8 | | | | | | | |
| 9 | | | | | | | |
| 10 | | | | | | | |
| 11 | | | | | | | |
| 12 | | | | | | | |

---

## Tally

| Signal | Count / 12 | % |
|---|---|---|
| Frames with light source | | |
| Frames with ≥1 silhouette | | |
| Frames with flanking on both sides | | |
| Frames with flanking on one side | | |
| Frames with silhouette but no flanking | | |

**Baseline reference (art_01M64VKA89R1TZMNK0QSJW990E r2):** All three original runs showed the flanking pattern in sampled frames. Baseline = 3/3 runs, emergent (no explicit prompt terms confirmed).

---

## Drift / break log

Record any frame where the pattern diverges from the baseline:

| Frame # | What changed | Possible prompt cause | Confidence |
|---|---|---|---|
| | | | low / medium / high |

---

## Run verdict

- [ ] **Pattern holds** — flanking in majority of sampled frames, light source present
- [ ] **Pattern partial** — light source present but flanking absent or one-sided
- [ ] **Pattern absent** — neither element visible in majority of frames
- [ ] **Uncertain** — insufficient frame sample

**Observer note:**

---

## Next improvement gate

Before treating the pattern as a reliable rule:  
1. Fill this sheet for ≥3 additional runs with *no* explicit silhouette/flanking prompt terms (pure baseline).  
2. Fill for ≥3 runs with explicit terms (controlled).  
3. Compare flanking % between groups.  
If baseline flanking % ≈ controlled flanking %, the pattern is emergent from model bias, not prompt-driven.