SOURCE = 'art_01M6668GYBV9RJW3PX59D4KBBR@r1'

def preflight(step):
    """Policy aid, not legal clearance. region describes applicable service region.
    billing_linked describes the Cloud project, not whether this call costs money.
    linked_terms_reviewed is a caller assertion, not verified by this function.
    """
    out = dict(step_id=step['step_id'], evidence=[SOURCE],
               execution_gate='unknown', data_use='unknown',
               publication='review_required', reasons=[])
    if step.get('route') != 'gemini_api':
        out['reasons'].append('Route terms not evaluated; weight licence is not output clearance')
        return out
    region = step.get('region')
    billing = step.get('billing_linked')
    offered = step.get('client_offered')
    if region not in ('EEA', 'CH', 'UK', 'OTHER') or type(billing) is not bool or type(offered) is not bool:
        out['reasons'].append('Missing region, billing or client-offering context')
        return out
    protected = region in ('EEA', 'CH', 'UK')
    out['data_use'] = 'paid_service_terms' if billing or protected else 'unpaid_service_terms'
    out['execution_gate'] = 'blocked' if protected and offered and not billing else 'not_blocked_by_this_check'
    if out['execution_gate'] == 'blocked':
        out['reasons'].append('Paid services required for clients offered in this region')
    out['reasons'].append('No ownership claim is not an affirmative user ownership grant')
    if not step.get('linked_terms_reviewed', False):
        out['reasons'].append('Incorporated terms not reviewed')
    if step.get('commercial', False):
        out['reasons'].append('Commercial scope unresolved in this record; review policy, not a contractual ban')
    return out