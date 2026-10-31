from math import ceil
from comparison_plan import plan_comparisons

def test_plan():
    for n in range(18):
        candidates = [f'topic_{i}' for i in range(n)]
        p = plan_comparisons(candidates, 'reference')
        assert p['planned_calls'] == ceil(n/4)
        assert all(2 <= len(b) <= 5 and b[0] == 'reference' for b in p['comparison_groups'])
        assert [x for b in p['comparison_groups'] for x in b[1:]] == candidates
        assert p['estimated_credits'] == 5*ceil(n/4)
        assert not p['global_ranking_supported']
    for candidates, anchor in [(['a','a'], 'ref'), (['ref'], 'ref'), ([None], 'ref'), (['a'], '')]:
        try:
            plan_comparisons(candidates, anchor)
        except ValueError:
            pass
        else:
            raise AssertionError('invalid input accepted')

if __name__ == '__main__':
    test_plan()
    print('22 cases passed')