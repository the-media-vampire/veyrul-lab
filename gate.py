# Original adapter by Patch / OpenAI. MIT.
# Gate reasons about evidence sufficiency, not whether a reviewer is correct.
def gate(rule, observations):
    relevant = [o for o in observations if o['rule'] == rule['id']]
    valid = [o for o in relevant if all(o.get(k) for k in ('source', 'revision', 'locator', 'reviewer', 'method', 'take')) and o['take'] == rule['take']]
    failures = [o for o in valid if o['verdict'] == 'fail' and o['kind'] in rule['witness_kinds']]
    if failures:
        return {'outcome': 'fail', 'reason': 'counterexample', 'evidence': failures}
    for o in valid:
        if o['verdict'] != 'pass':
            continue
        if rule['scope'] == 'endpoint':
            sufficient = o['kind'] == 'endpoint' and o.get('endpoint_verified') is True
        else:
            sufficient = (o['kind'] == 'continuous_review' and o.get('complete') is True
                          and o.get('span') == rule['span'])
        if sufficient:
            return {'outcome': 'pass', 'reason': 'scope_covered', 'evidence': [o]}
    return {'outcome': 'unknown', 'reason': 'missing_or_insufficient_coverage', 'evidence': valid}


def tests():
    rule = {'id': 'offcentre', 'take': 'synthetic-A', 'scope': 'throughout', 'span': [0, 30], 'witness_kinds': ['still', 'continuous_review']}
    base = {'rule': 'offcentre', 'take': 'synthetic-A', 'source': 'synthetic-fixture', 'revision': 1, 'locator': 'frame-A', 'reviewer': 'test', 'method': 'synthetic', 'kind': 'still', 'verdict': 'pass'}
    cases = []
    cases.append(('sparse_pass_is_unknown', gate(rule, [base])['outcome'], 'unknown'))
    cases.append(('one_counterexample_fails', gate(rule, [dict(base, verdict='fail')])['outcome'], 'fail'))
    cases.append(('uncited_failure_is_unknown', gate(rule, [dict(base, verdict='fail', source='')])['outcome'], 'unknown'))
    cases.append(('other_take_is_unknown', gate(rule, [dict(base, verdict='fail', take='other')])['outcome'], 'unknown'))
    endpoint = dict(rule, scope='endpoint', witness_kinds=['endpoint'])
    final = dict(base, kind='endpoint', endpoint_verified=True)
    cases.append(('verified_endpoint_passes', gate(endpoint, [final])['outcome'], 'pass'))
    cases.append(('approximate_last_still_is_unknown', gate(endpoint, [dict(final, endpoint_verified=False)])['outcome'], 'unknown'))
    full = dict(base, kind='continuous_review', complete=True, span=[0,30])
    cases.append(('complete_review_passes', gate(rule, [full])['outcome'], 'pass'))
    cases.append(('gap_without_citation_is_valid_unknown', gate(rule, [])['outcome'], 'unknown'))
    for name, actual, expected in cases:
        assert actual == expected, (name, actual, expected)
    print({'tests_passed': len(cases), 'cases': cases})

if __name__ == '__main__':
    tests()