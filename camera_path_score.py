import math
import statistics
import json


def score(source, output, width, height, min_coverage=0.8):
    """Time-matched frames: dicts of background landmark IDs to pixel (x,y)."""
    if len(source) != len(output) or not source:
        raise ValueError('Require equal, nonempty, time-matched frame lists')
    diag = math.hypot(width, height)
    if width <= 0 or height <= 0:
        raise ValueError('Positive canvas dimensions required')
    residuals, movement = [], []
    possible = sum(len(f) for f in source)
    for s, o in zip(source, output):
        for key in s.keys() & o.keys():
            if key not in source[0] or key not in output[0]:
                continue
            ds = tuple(s[key][j] - source[0][key][j] for j in (0, 1))
            do = tuple(o[key][j] - output[0][key][j] for j in (0, 1))
            residuals.append(math.dist(ds, do) / diag)
            movement.append(math.hypot(*do) / diag)
    coverage = len(residuals) / possible if possible else 0
    valid = coverage >= min_coverage and bool(residuals)
    return {'coverage': coverage, 'valid': valid,
            'path_error_pct_diagonal': 100 * statistics.median(residuals) if valid else None,
            'raw_motion_pct_diagonal': 100 * statistics.median(movement) if valid else None}


def synthetic_tests():
    landmarks = {'a': (100,100), 'b': (800,100), 'c': (100,800), 'd': (800,800)}
    def track(dx,dy):
        return [{k:(x+dx*t,y+dy*t) for k,(x,y) in landmarks.items()} for t in range(5)]
    source = track(25,10)
    cases = {'locked': track(25,10), 'frozen': track(0,0), 'extra_drift': track(32.5,10),
             'mostly_missing': [{'a': f['a']} for f in source]}
    results = {k:score(source,v,1000,1000) for k,v in cases.items()}
    assert results['locked']['path_error_pct_diagonal'] == 0
    assert results['frozen']['raw_motion_pct_diagonal'] == 0
    assert results['locked']['raw_motion_pct_diagonal'] > 0
    assert results['frozen']['path_error_pct_diagonal'] > results['extra_drift']['path_error_pct_diagonal'] > 0
    assert not results['mostly_missing']['valid']
    return results


if __name__ == '__main__':
    print(json.dumps(synthetic_tests(), indent=2))