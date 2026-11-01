from preflight import preflight

fixture = {'nodes': [{'id': 2, 'type': 'LoadImage', 'outputs': [
    {'type': 'IMAGE', 'links': [22]}, {'type': 'MASK', 'links': [1]}]}]}
verified = {'semantics_verified': True}
a = preflight(fixture, 2, {'IMAGE': verified})
assert a['missing_output_types'] == ['MASK'] and not a['ready_to_attempt']
b = preflight(fixture, 2, {'IMAGE': verified, 'MASK': {}})
assert b['structural_candidate'] and b['unverified_semantics'] == ['MASK'] and not b['ready_to_attempt']
c = preflight(fixture, 2, {'IMAGE': verified, 'MASK': verified})
assert c['ready_to_attempt'] and not c['runtime_validated']
unused = {'nodes': [{'id': 2, 'outputs': [{'type': 'IMAGE', 'links': [1]}, {'type': 'MASK', 'links': []}]}]}
assert preflight(unused, 2, {'IMAGE': verified})['required_output_types'] == ['IMAGE']
try:
    preflight(fixture, 999, {})
    raise AssertionError('missing node accepted')
except ValueError:
    pass
print('5 synthetic cases passed')