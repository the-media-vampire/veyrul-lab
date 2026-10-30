from gate import gate
contract = {'story_order_confirmed': False, 'clauses': [
    {'id': 'panel_dim_sampled', 'accepted_methods': ['stills', 'playback']},
    {'id': 'orbit_complete_unbroken', 'accepted_methods': ['playback']}]}
stills = [
    {'clause_id': 'panel_dim_sampled', 'method': 'stills', 'verdict': 'match'},
    {'clause_id': 'orbit_complete_unbroken', 'method': 'stills', 'verdict': 'match'}]
a = gate(contract, stills)
assert a['status'] == 'unknown' and not a['handoff_ready']
b = gate(contract, [dict(stills[0], verdict='mismatch'), stills[1]])
assert b['status'] == 'fail' and b['clauses']['orbit_complete_unbroken'] == 'unknown'
c = gate(contract, [stills[0], dict(stills[1], method='playback')])
assert c['status'] == 'pass' and not c['handoff_ready']
d = gate(dict(contract, story_order_confirmed=True), [stills[0], dict(stills[1], method='playback')])
assert d['handoff_ready']
assert gate(contract, [])['status'] == 'unknown'
print('5 assertions passed (synthetic fixtures only)')