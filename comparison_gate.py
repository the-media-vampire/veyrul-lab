"""Descriptive recipe comparison; no inference or significance claims."""
MATCH = ('hardware', 'width', 'height', 'frames', 'batch', 'timing_scope', 'evaluation_set', 'acceptance_rule')

def compare(base, candidate):
    reasons = []
    for k in MATCH:
        if base.get(k) is None or candidate.get(k) is None:
            reasons.append('missing:' + k)
        elif base[k] != candidate[k]:
            reasons.append('mismatch:' + k)
    for label, row in [('base', base), ('candidate', candidate)]:
        times, accepted = row.get('seconds', []), row.get('accepted', [])
        if len(times) < 3 or len(times) != len(accepted):
            reasons.append(label + ':need >=3 timed attempts and paired acceptance flags')
        elif any(type(t) not in (int, float) or not 0 < t < float('inf') for t in times) or any(type(a) is not bool for a in accepted):
            reasons.append(label + ':invalid observations')
    if reasons:
        return {'status': 'insufficient_comparable_evidence', 'reasons': reasons}
    cost = lambda r: sum(r['seconds']) / sum(r['accepted']) if any(r['accepted']) else None
    b, c = cost(base), cost(candidate)
    return {'status': 'descriptive_only', 'base_seconds_per_accepted_clip': b,
            'candidate_seconds_per_accepted_clip': c,
            'candidate_speedup': b / c if b is not None and c is not None else None}