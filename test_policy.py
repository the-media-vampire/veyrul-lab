from itertools import product
from policy import Policy, choose, after_send

cases = 0
for mode, has_read, has_write, has_endpoint in product(
        ('headless', 'desktop'), (False, True), (False, True), (False, True)):
    p = Policy(mode, 'session-A', ('/in',) if has_read else (),
               ('/out',) if has_write else (),
               'verified-by-caller' if has_endpoint else None)
    expected = ((mode == 'headless' and not has_endpoint) or
                (mode == 'desktop' and has_endpoint and not (has_read or has_write)))
    try:
        result = choose(p)
    except ValueError:
        assert not expected, p
    else:
        assert expected and result == mode, p
    cases += 1
for p in (Policy('auto', 'session-A'), Policy('headless', '')):
    try:
        choose(p)
    except ValueError:
        pass
    else:
        raise AssertionError('invalid policy accepted')
    cases += 1
assert after_send('unknown') == 'reconcile_without_replay'
assert after_send('confirmed') == 'inspect'
assert after_send('rejected') == 'stop'
cases += 3
print(f'PASS: {cases} policy checks; 16 route combinations, 2 invalid policies, 3 outcome cases')
print('Scope: pure Python policy only; no SoundCraft, MCP, TCP, filesystem confinement, or audio tested.')