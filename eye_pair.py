import math


def assess(before, after, *, rule='visible_colour_change', terminal_window=None):
    def unknown(reason):
        return {'log_key': rule, 'outcome': 'unknown', 'unknown_reason': reason,
                'evidence_source': [x for x in (before, after) if x], 'promotable': False}
    if rule not in ('visible_colour_change', 'red_reveal'):
        raise ValueError('unsupported rule')
    for x in (before, after):
        if not x or any(k not in x for k in ('clip', 'subject', 'eye', 't', 'ref', 'method', 'state')):
            return unknown('missing observation fields')
        if not all(x[k] for k in ('clip', 'subject', 'eye', 'ref', 'method')):
            return unknown('missing provenance or identity')
        if type(x['t']) not in (int, float) or not math.isfinite(x['t']) or x['t'] < 0:
            return unknown('invalid timestamp')
        if x['state'] not in ('red', 'nonred', 'closed'):
            return unknown('unresolved eye state')
    if any(before[k] != after[k] for k in ('clip', 'subject', 'eye')):
        return unknown('unmatched eye identity')
    if before['t'] >= after['t']:
        return unknown('unordered observations')
    if terminal_window is not None:
        start, end = terminal_window
        if not (math.isfinite(start) and math.isfinite(end) and 0 <= start <= end):
            raise ValueError('invalid terminal window')
        if not start <= after['t'] <= end:
            return unknown('no sample in requested terminal window')
    if rule == 'visible_colour_change' and before['state'] == 'closed':
        return unknown('closed eye supplies no baseline iris colour')
    passed = before['state'] in ('nonred', 'closed') and after['state'] == 'red'
    return {'log_key': rule, 'outcome': 'pass' if passed else 'fail', 'unknown_reason': None,
            'evidence_source': [before, after], 'promotable': True,
            'scope': 'sampled pair only; not continuous coverage or cut detection'}