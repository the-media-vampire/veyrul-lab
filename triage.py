"""Card statements only; not runtime feasibility or legal clearance.
Source: art_01M66YP3XWTDRSW8X0YA8R8AQV revision 1.
"""
import json
MODELS = {
 'Qwen-2511': (None, 'apache'),
 'FLUX.2-4B': (13, 'apache'),
 'FLUX.2-9B': (29, 'noncommercial'),
 'FLUX.2-9B-KV': (29, 'noncommercial'),
 'FLUX-3-mirror': (None, 'conditional'),
}
def triage(name, budget_gb, commercial=False):
    """Card-based triage only; not runtime feasibility or legal clearance."""
    gb, licence = MODELS[name]
    memory = 'unknown' if gb is None else ('within_card_estimate' if gb <= budget_gb else 'above_budget')
    use = ('excluded' if licence == 'noncommercial' else 'review_required' if licence == 'conditional' else 'card_permits') if commercial else 'not_screened'
    return {'memory': memory, 'use': use}

def shortlist(budget, commercial):
    return {n for n in MODELS if triage(n,budget,commercial)['memory']=='within_card_estimate' and triage(n,budget,commercial)['use'] in ('card_permits','not_screened')}

if __name__ == '__main__':
    checks = 0
    for commercial in (False, True):
        previous = set()
        for budget in (0, 12, 13, 16, 28, 29, 32):
            current = shortlist(budget, commercial)
            assert previous <= current
            previous = current
            checks += 1
    for budget in (12,16,32):
        for name in MODELS:
            assert triage(name,budget,False)['memory'] == triage(name,budget,True)['memory']
            checks += 1
    assert shortlist(13,True)=={'FLUX.2-4B'}
    assert shortlist(29,False)=={'FLUX.2-4B','FLUX.2-9B','FLUX.2-9B-KV'}
    assert all('FLUX-3-mirror' not in shortlist(b,True) for b in (12,16,32))
    checks += 3
    print(json.dumps({'assertions_passed':checks,'commercial_12GB':{n:triage(n,12,True) for n in MODELS},'commercial_shortlists':{str(b):sorted(shortlist(b,True)) for b in (12,16,32)},'unknown_memory_baseline':['Qwen-2511','FLUX-3-mirror']},indent=2))