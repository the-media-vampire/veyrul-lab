def gate(contract, observations):
    by_id = {o['clause_id']: o for o in observations}
    results = {}
    for clause in contract['clauses']:
        obs = by_id.get(clause['id'])
        if not obs or obs['method'] not in clause['accepted_methods']:
            results[clause['id']] = 'unknown'
        elif obs['verdict'] == 'mismatch':
            results[clause['id']] = 'fail'
        elif obs['verdict'] == 'match':
            results[clause['id']] = 'pass'
        else:
            results[clause['id']] = 'unknown'
    status = 'fail' if 'fail' in results.values() else ('unknown' if 'unknown' in results.values() else 'pass')
    return {'status': status, 'clauses': results,
            'handoff_ready': status == 'pass' and contract.get('story_order_confirmed') is True}