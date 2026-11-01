import json
from subtitle_timeline import map_cues

segments = [dict(source='A', start=10., end=12.), dict(source='A', start=30., end=33.)]
cues = [dict(id='one', source='A', start=10.5, end=11.),
        dict(id='two', source='A', start=30.25, end=31.),
        dict(id='three', source='A', start=32., end=32.5)]
expected = [(0.5,1.), (2.25,3.), (4.,4.5)]
actual = map_cues(segments, cues)
baseline = [(c['start']-10., c['end']-10.) for c in cues]
def errors(pairs):
    return [max(abs(a-x),abs(b-y)) for (a,b),(x,y) in zip(pairs,expected)]
assert len(actual) == len(expected)
base_errors = errors(baseline)
mapped_errors = errors([(c['start'],c['end']) for c in actual])
assert mapped_errors == [0.,0.,0.]
assert base_errors == [0.,18.,18.]
crossing = map_cues(segments, [dict(id='edge',source='A',start=11.8,end=12.2)])
assert len(crossing) == 1 and crossing[0]['clipped']
assert abs(crossing[0]['start']-1.8) < 1e-12 and crossing[0]['end'] == 2.
assert map_cues(segments,[dict(id='removed',source='A',start=20.,end=21.)]) == []
assert map_cues(segments,[dict(id='other',source='B',start=10.5,end=11.)]) == []
print(json.dumps(dict(baseline_endpoint_error_seconds=base_errors,
    mapped_endpoint_error_seconds=mapped_errors,
    baseline_mean_error_seconds=sum(base_errors)/3,
    mapped_mean_error_seconds=sum(mapped_errors)/3,
    crossing_cut_result=crossing), indent=2))