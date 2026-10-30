import math

def review_cues(samples):
    """Adjacent sampled changes are review brackets, never exact edit points."""
    if any(not isinstance(s['t'], (int, float)) or isinstance(s['t'], bool)
           or not math.isfinite(s['t']) or s['t'] < 0 for s in samples):
        raise ValueError('finite nonnegative seconds required')
    if any(b['t'] <= a['t'] for a, b in zip(samples, samples[1:])):
        raise ValueError('timestamps must strictly increase')
    cues = []
    for a, b in zip(samples, samples[1:]):
        if a['label'] is None or b['label'] is None:
            continue
        if a['label'] != b['label']:
            cues.append({'review_from_s': a['t'], 'review_to_s': b['t'],
                         'from_label': a['label'], 'to_label': b['label'],
                         'claim': 'sampled_state_difference; transition timing/type unverified'})
    return {'cues': cues, 'exact_cut_times': None,
            'continuous_hold_verified': False, 'audio_status': 'not_assessed'}

if __name__ == '__main__':
    import json
    s = [{'t': 0, 'label': 'wide'}, {'t': 2, 'label': 'wide'},
         {'t': 4, 'label': 'detail'}]  # synthetic only
    r = review_cues(s)
    assert [(c['review_from_s'], c['review_to_s']) for c in r['cues']] == [(2, 4)]
    assert r['exact_cut_times'] is None and not r['continuous_hold_verified']
    assert review_cues([{'t': 0, 'label': 'wide'}, {'t': 2, 'label': None},
                        {'t': 4, 'label': 'detail'}])['cues'] == []
    assert review_cues([])['cues'] == []
    assert review_cues([{'t': 0, 'label': 'wide'}, {'t': 4, 'label': 'wide'}])['cues'] == []
    for times in ([2, 1], [1, 1], [0, float('nan')], [0, float('inf')], [-1, 0], [False, 1]):
        try:
            review_cues([{'t': t, 'label': 'wide'} for t in times])
        except ValueError:
            pass
        else:
            raise AssertionError(times)
    print('PASS: bracket, no exact-cut/hold claim, unknown gap, empty, unchanged, and 6 invalid-time cases')
    print(json.dumps(r, indent=2))