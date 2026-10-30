"""MIT licensed. Timing arithmetic only; no film or audience validation."""
TREATMENTS = {
    'A_Keep_out': [('threshold',4),('interrupted_work',4),('chair',5),('door_brace_reveal',4),('door_tests_brace',3)],
    'B_Come_in': [('threshold',4),('ready_workbench',4),('chair',5),('door_prop_reveal',4),('door_tests_prop',3)],
}
def validate(shots):
    return len(shots) == 5 and all(seconds > 0 for _, seconds in shots) and sum(seconds for _, seconds in shots) == 20
for name, shots in TREATMENTS.items():
    assert validate(shots)
    print(name, 'PASS: five shots, 20 seconds')
assert not validate([('too_short',19)])
print('Invalid 19-second single-shot case correctly rejected')
print('Limits: timing validation only; no rendering, playback, or audience test.')