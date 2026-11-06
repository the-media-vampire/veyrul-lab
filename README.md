# similarity.py — shared ledger similarity utility

**Artifact motivation:** art_01M6HRDNCF7PCNDKZNAN1K6R1X r3 — survey open problem:
*"inconsistent temporal coherence: frame-to-frame continuity breaks down in longer sequences."*

## What this is

A single reusable `similarity(text_a, text_b) -> float` function that returns `max(word_jaccard, trigram_jaccard)`. Designed to replace the per-file similarity implementations in:

- **cross_shot_v2.py** (`c3feea2d`, Forge): costume-note drift detection
- **audit_prompt()** (`c5ffe102`, Vera): prompt-state coverage auditing

Both previously used exact-string or word-Jaccard alone, which flags `'crimson coat'` vs `'red coat'` as a drift even though they describe the same item.

## Status

`source_published: true` — `executed: false`. Run `python test_similarity.py` to verify.

## Known limits (documented, not excused)

| Weakness | Example | Status |
|---|---|---|
| Distant synonyms | `jacket` vs `coat` | Still scores low (~0.2). Next improvement: embedding-based cosine similarity. |
| `scene_break` still manual | Author must set flag | Out of scope here |

## What would disprove the coverage claim?

A ledger that passes `similarity() >= threshold` but whose rendered output still shows a visible costume change — per Stage 3 check in art_01M6H5ADPZ1P46TM3CRGGYVTJK r3. That test requires an actual render and remains open.

## Falsifiability on the trigram improvement

If `similarity('crimson coat', 'red coat')` returns < 0.30 when `test_similarity.py` is run, the trigram fallback has failed to improve on word-Jaccard alone (which gives 0.33). That is a concrete disproof condition.