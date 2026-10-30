def audit(counts):
    keys = ('match', 'mismatch', 'ambiguous', 'not_verified')
    if set(counts) != set(keys):
        raise ValueError('Expected exactly four evidence labels')
    if any(type(counts[k]) is not int or counts[k] < 0 for k in keys):
        raise ValueError('Counts must be nonnegative integers')
    n = sum(counts.values())
    if not n:
        raise ValueError('Empty evidence')
    m, f, a, u = (counts[k] for k in keys)
    return {'rows': n, 'baseline_zero_mismatch_accept': f == 0,
            'audit_decision': 'observed_failure' if f else ('fully_resolved_match' if a + u == 0 else 'unresolved'),
            'confirmed_match_fraction': round(m / n, 4),
            'unresolved_fraction': round((a + u) / n, 4),
            'possible_match_fraction_bounds': [round(m / n, 4), round((m + a + u) / n, 4)]}