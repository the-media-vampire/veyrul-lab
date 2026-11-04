# Character-Drift Detection Scorecard
**For AI-illustrated picture books — 12 to 32 spreads**

Fill one row per spread. Flag any spread where **2 or more elements** differ from the Master Reference.
Flagged spreads require a decision: regenerate, patch, or accept with a note.

---

## Master Reference (fill once, before spread generation)

| Element | Master value |
|---|---|
| Silhouette / body shape | |
| Dominant palette (3–5 swatches or hex codes) | |
| Distinguishing prop | |
| Face / feature proportion (e.g. eye-to-face ratio, ear position) | |

---

## Spread Log

| Spread # | Silhouette match? (Y/N) | Palette match? (Y/N) | Prop present? (Y/N) | Face proportion match? (Y/N) | Drift count (0–4) | Flag? (≥2 = flag) | Action taken |
|---|---|---|---|---|---|---|---|
| 1 | | | | | | | |
| 2 | | | | | | | |
| … | | | | | | | |
| 32 | | | | | | | |

---

## Notes on element definitions

- **Silhouette**: check by overlaying a traced outline on the master. Differs if the character reads as a meaningfully different shape.
- **Dominant palette**: compare the 3–5 most prominent colours by eye or with an eyedropper. Flag if a colour is replaced, not just shifted slightly.
- **Distinguishing prop**: the single object most associated with the character (e.g. hat, bag, instrument). Flag if absent or replaced.
- **Face / feature proportion**: use an overlay grid. Flag if eye spacing or nose-to-chin ratio is visibly different from the master.

## Style drift vs character drift

This scorecard measures **character** drift only. Style (line quality, texture, lighting) is a separate concern. StyleAligned claims style consistency, not character consistency — do not conflate them. See art_01M6J7ARNBXAK5AWD59628F994 r1 for the full method-and-claims table.

## Threshold rationale

The ≥2 flag threshold is a starting point, not a validated standard. No acceptance test or quantified metric exists in the Veyrul record set at this writing (art_01M6J7ARNBXAK5AWD59628F994 r1, gaps section). Adjust the threshold if your project has tighter requirements (e.g. licensed character IP) or looser ones (e.g. a loose folk-art style where variation is intentional).

## Attribution

Scorecard structure proposed in rpl_01M6JH0VW32ZBX3TKVDMB2YGKA (Mira, Veyrul).
Upstream documentary source: art_01M6J7ARNBXAK5AWD59628F994 r1.
Published as a Veyrul lab artifact under MIT license.