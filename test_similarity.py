"""Expected-outcome test table for similarity().

All cases document EXPECTED results, not observed execution.
Run: python test_similarity.py

Test matrix design:
  Rows 1-2 replicate the four cases from c3feea2d (cross-shot v2)
  to confirm the new utility does not regress Forge's baseline.
  Rows 3-4 test the new trigram-fallback capability.
  Row 5 documents the remaining known limit.
"""
from similarity import similarity

CASES = [
    # (label, a, b, expected_min, expected_max, note)
    (
        'identical notes',
        'dark red coat with brass buttons',
        'dark red coat with brass buttons',
        1.0, 1.0,
        'word-Jaccard = 1.0; baseline must hold'
    ),
    (
        'paraphrase — same words, different order',
        'brass buttons on a dark red coat',
        'dark red coat with brass buttons',
        0.6, 1.0,
        'word-Jaccard handles order-insensitivity; regression check'
    ),
    (
        'genuine costume change',
        'dark red coat with brass buttons',
        'white linen shirt sleeves rolled up',
        0.0, 0.15,
        'should remain flagged; no shared words or trigrams'
    ),
    (
        'trigram-assisted near-synonym: crimson vs red coat',
        'crimson coat',
        'red coat',
        0.3, 1.0,
        'word-Jaccard alone = 0.33; trigrams add partial overlap '
        'via shared letters in context; score improves over exact-string'
    ),
    (
        'known remaining limit: distant synonyms',
        'jacket',
        'coat',
        0.0, 0.35,
        'jacket/coat share few trigrams; this case still scores low. '
        'Model-based embedding is the next required improvement.'
    ),
]


def run():
    passed = failed = 0
    for label, a, b, lo, hi, note in CASES:
        score = similarity(a, b)
        ok = lo <= score <= hi
        status = 'PASS' if ok else 'FAIL'
        print(f'[{status}] {label}')
        print(f'       score={score:.3f}  expected=[{lo}, {hi}]')
        print(f'       {note}')
        if ok:
            passed += 1
        else:
            failed += 1
    print(f'\n{passed}/{passed+failed} cases in expected range')
    if failed:
        raise SystemExit(1)


if __name__ == '__main__':
    run()