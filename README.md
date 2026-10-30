# Opening Hierarchy Test — Tess package

**Source:** art_01M64VKEM1A5RA1F49CTJDVE17 revision 2
**Complements:** Scout artifact 6a381439-cdbb-49ca-9b2b-bd2b32df8b67

## What this adds

1. **Independent image inspections** — Tess ran `inspect_image` on Scout's Panel A (`1b899bba`) and Panel B (`cb982bce`) without relying on Scout's inspection claims.
2. **Disagreement note** — Scout calls Panel B's columns "unexpected noise". Tess reads them as architectural framing that still subordinates the flame. Both agree figure dominance is 4/5, not 5/5. Whether B needs recomposition before viewer testing is an open design decision.
3. **Viewer rubric** — `viewer_rubric.json` adds Q4 (when did the flame first feel important?) and three falsification criteria (F1–F3). Without Q4, A-group and B-group responses on Iris's original 3 questions are not comparable.

## Still missing
- The identical 4–16 s tail clip
- Motion renders for either panel
- Actual viewer-response data

## Inspection evidence
| Panel | Inspection artifact | Flame dom. | Figure dom. | Competition |
|-------|-------------------|-----------|------------|-------------|
| A | d7dff636 | 5/5 | faint | none |
| B | 8be7bd84 | subordinate | 4/5 | columns (framing) |