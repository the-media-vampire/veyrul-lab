"""Synthetic instrument test, not observations of generated media."""
import json


def score(frames):
    if not frames or any(x not in (0, 1, None) for x in frames):
        raise ValueError('Use nonempty sequences of 0, 1, or None')
    observed = [x for x in frames if x is not None]
    hits = sum(observed)
    return {
        'sampled_recurrence': True if hits else (False if len(observed) == len(frames) else None),
        'observed_occupancy': hits / len(observed) if observed else None,
        'coverage': len(observed) / len(frames),
        'eight_of_twelve': (hits >= 8) if len(frames) == 12 and len(observed) == 12 else None
    }


if __name__ == '__main__':
    cases = {
        'absent': [0]*12,
        'late_only': [0]*11+[1],
        'early_only': [1]+[0]*11,
        'persistent': [1]*12,
        'unobserved': [None]*12,
        'partial_no_hit': [0]*6+[None]*6
    }
    results = {name: score(frames) for name, frames in cases.items()}
    assert results['late_only']['sampled_recurrence'] is True
    assert results['late_only']['eight_of_twelve'] is False
    assert results['early_only']['observed_occupancy'] == 1/12
    assert results['persistent']['eight_of_twelve'] is True
    assert results['absent']['sampled_recurrence'] is False
    assert results['unobserved']['sampled_recurrence'] is None
    assert results['partial_no_hit']['sampled_recurrence'] is None
    bounds = {str(n): 0.025**(1/n) for n in (3, 36)}
    print(json.dumps({'synthetic_results': results, 'assertions_passed': 7,
        'illustrative_all_success_lower_95': bounds,
        'warning': 'IID random sampling is not established for historical runs; 36 is a counterexample, not a valid sample size.'}, indent=2))