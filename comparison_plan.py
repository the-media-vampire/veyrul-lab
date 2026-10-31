"""Offline request planning, NOT a verified provider API schema."""

def plan_comparisons(candidates, anchor):
    if not isinstance(anchor, str) or not anchor.strip():
        raise ValueError('anchor must be a nonempty string')
    if not isinstance(candidates, list) or any(not isinstance(x, str) or not x.strip() for x in candidates):
        raise ValueError('candidates must be a list of nonempty strings')
    if len(set(candidates)) != len(candidates) or anchor in candidates:
        raise ValueError('duplicate candidates or anchor overlap')
    batches = [[anchor] + candidates[i:i+4] for i in range(0, len(candidates), 4)]
    return {'comparison_groups': batches, 'planned_calls': len(batches),
            'estimated_credits': 5*len(batches),
            'global_ranking_supported': False}