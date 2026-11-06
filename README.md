# cross_shot_v2 — Jaccard costume-note drift checker

Survey source: art_01M6HRDNCF7PCNDKZNAN1K6R1X r3 (arXiv:2507.07202v1, CC BY 4.0).
Open problem addressed: 'inconsistent temporal coherence: frame-to-frame continuity
breaks down in longer sequences.'

## Improvement over exact-string baseline

| Method | Paraphrase of same costume | Genuine change |
|---|---|---|
| Exact-string | flags (false positive) | flags |
| Jaccard >= 0.5 | does not flag | flags |

## Limits
- Jaccard is order-insensitive but not synonym-aware ('crimson' vs 'red' still flags).
- scene_break must be set explicitly by the author.
- Checks authored ledger data only; no rendering engine queried.
- Next improvement: character-ngram or embedding similarity to handle synonyms.

## Usage
    from cross_shot_v2 import Shot, cross_shot_check
    shots = [Shot('S01','Maya','red coat gold belt'), Shot('S02','Maya','gold belt red coat')]
    print(cross_shot_check(shots))  # consistent, not flagged