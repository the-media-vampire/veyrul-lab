"""Fixed-check comparison. Bounds are logical uncertainty, not confidence intervals."""
VALID = {'MATCH', 'MISMATCH', 'AMBIGUOUS', 'NOT_VERIFIED'}

def interval(v):
    if v not in VALID:
        raise ValueError('invalid verdict')
    return (0, 0) if v == 'MATCH' else (1, 1) if v == 'MISMATCH' else (0, 1)

def compare(a, b):
    # Same ID means same registered criterion, frame scope, and paired trial.
    # Key equality cannot itself enforce that semantic requirement.
    if not a or a.keys() != b.keys():
        raise ValueError('require the same nonempty registered checks')
    lo = hi = wins = losses = resolved = 0
    for k in a:
        al, ah = interval(a[k]); bl, bh = interval(b[k])
        lo += bl - ah; hi += bh - al
        if al == ah and bl == bh:
            resolved += 1
            wins += al > bl
            losses += bl > al
    n = len(a)
    return {'checks': n, 'resolved_pairs': resolved, 'wins': wins, 'losses': losses,
            'delta_failure_bounds': [lo/n, hi/n]}

if __name__ == '__main__':
    # SYNTHETIC fixtures: no generated media or source observations.
    a = {'pair1': 'MISMATCH', 'pair2': 'MISMATCH', 'pair3': 'MATCH', 'pair4': 'MATCH'}
    cases = {
        'unchanged_observations': (a.copy(), [0.0, 0.0]),
        'one_resolved_improvement': ({**a, 'pair1': 'MATCH'}, [-0.25, -0.25]),
        'failures_become_unverified': ({**a, 'pair1': 'NOT_VERIFIED', 'pair2': 'AMBIGUOUS'}, [-0.5, 0.0]),
    }
    for name, (b, expected) in cases.items():
        result = compare(a, b)
        assert result['delta_failure_bounds'] == expected
        print(name, result)
    try:
        compare(a, {'pair3': 'MATCH', 'pair4': 'MATCH'})
    except ValueError:
        print('dropped-check IDs: correctly rejected')
    else:
        raise AssertionError('should reject changed denominator')