from audit import audit
import json
cases = {'rain_clip_reported': dict(match=16, mismatch=0, ambiguous=6, not_verified=4),
         'final_folder_clip_reported': dict(match=8, mismatch=3, ambiguous=3, not_verified=1),
         'synthetic_all_resolved': dict(match=26, mismatch=0, ambiguous=0, not_verified=0)}
results = {name: audit(c) for name, c in cases.items()}
assert results['rain_clip_reported']['baseline_zero_mismatch_accept']
assert results['rain_clip_reported']['audit_decision'] == 'unresolved'
assert results['final_folder_clip_reported']['audit_decision'] == 'observed_failure'
assert results['synthetic_all_resolved']['audit_decision'] == 'fully_resolved_match'
for bad in [dict(match=0,mismatch=0,ambiguous=0,not_verified=0), dict(match=-1,mismatch=0,ambiguous=0,not_verified=0)]:
    try: audit(bad)
    except ValueError: pass
    else: raise AssertionError('Invalid input accepted')
print(json.dumps({'results': results, 'checks_passed': 6}, indent=2))