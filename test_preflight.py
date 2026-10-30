from preflight import preflight, SOURCE

base = dict(step_id='edit-1', route='gemini_api', region='OTHER', billing_linked=False,
            client_offered=True, commercial=True)
cases = [
    ('unpaid', {}, 'unpaid_service_terms', 'not_blocked_by_this_check'),
    ('billing-linked free quota', {'billing_linked': True}, 'paid_service_terms', 'not_blocked_by_this_check'),
    ('EEA unpaid offered client', {'region': 'EEA'}, 'paid_service_terms', 'blocked'),
    ('UK unpaid non-client', {'region': 'UK', 'client_offered': False}, 'paid_service_terms', 'not_blocked_by_this_check'),
    ('CH paid client', {'region': 'CH', 'billing_linked': True}, 'paid_service_terms', 'not_blocked_by_this_check'),
    ('unknown region', {'region': None}, 'unknown', 'unknown'),
    ('local Apache route not auto-cleared', {'route': 'local_apache'}, 'unknown', 'unknown'),
]
for name, patch, data, gate in cases:
    result = preflight(dict(base, **patch))
    assert result['data_use'] == data, (name, result)
    assert result['execution_gate'] == gate, (name, result)
    assert result['publication'] == 'review_required', (name, result)
    assert result['step_id'] == 'edit-1' and result['evidence'] == [SOURCE]
    print('PASS:', name)
print('7 cases passed; no API calls, legal clearance, or media tests performed.')