import json
N=144
LOCKS=((0,48),(96,144)) # zero-based half-open, synthetic 6 s at 24 fps
locked=[i for a,b in LOCKS for i in range(a,b)]
sparse=set(round(i*(N-1)/11) for i in range(12))
boundary={0,47,96,143}
full=set(locked)
def rate(samples,cases):
    hits=sum(bool(samples.intersection(c)) for c in cases)
    return {'detected':hits,'cases':len(cases),'fraction':round(hits/len(cases),6)}
single=[{i} for i in locked]
bursts=[set(range(i,i+4)) for a,b in LOCKS for i in range(a,b-3)]
results={name:{'locked_frames_checked':len(samples.intersection(locked)), 'single_frame':rate(samples,single),'four_frame':rate(samples,bursts)} for name,samples in [('12_uniform_stills',sparse),('boundary_only',boundary),('all_locked_frames',full)]}
hidden=next(i for i in locked if i not in sparse)
source=[0]*N
output=source.copy(); output[hidden]=1
assert all(source[i]==output[i] for i in sparse.intersection(locked))
assert any(source[i]!=output[i] for i in locked)
assert results['12_uniform_stills']['single_frame']['detected']==8
assert results['all_locked_frames']['four_frame']['detected']==90
print(json.dumps({'sample_indices':sorted(sparse),'hidden_changed_frame_zero_based':hidden,'results':results,'assertions':'passed'},indent=2))