"""Original interval comparator. Seconds; closed conservative bounds."""

def compare(base, candidate):
    """Inputs are (last verified absent, first present), or None.

    Use only for a consistently defined beat with no earlier missed occurrence.
    These are conservative brackets, not probability distributions.
    """
    if base is None or candidate is None:
        return {'status': 'unknown', 'shift_bounds_s': None}
    for lo, hi in (base, candidate):
        if lo > hi:
            raise ValueError('reversed interval')
    low = round(candidate[0] - base[1], 6)
    high = round(candidate[1] - base[0], 6)
    status = 'earlier' if high < 0 else ('later' if low > 0 else 'unresolved')
    return {'status': status, 'shift_bounds_s': [low, high]}

if __name__ == '__main__':
    cases = [
        ('missing', None, None, 'unknown'),
        ('same', (14.2,15.9), (14.2,15.9), 'unresolved'),
        ('adjacent', (14.2,15.9), (12.5,14.2), 'unresolved'),
        ('separated', (14.2,15.9), (9.2,10.9), 'earlier'),
        ('later', (14.2,15.9), (17.6,19.3), 'later'),
    ]
    for name, base, candidate, expected in cases:
        result = compare(base, candidate)
        assert result['status'] == expected
        print(name, result)