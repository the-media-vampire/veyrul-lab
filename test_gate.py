from portal_gate import gate

cases=[
 ('counterexample_without_reference',gate([{'t':0,'door_closed':False,'evidence':'synthetic:open'}]),'reject'),
 ('sparse_positive',gate([{'t':0,'door_closed':True},{'t':2.9,'door_closed':True}]),'review'),
 ('unknown_not_false',gate([{'t':0,'door_closed':None}]),'review'),
 ('crossing_counterexample',gate([{'t':1.7,'door_closed':False,'crossing':True}]),'reject'),
 ('empty',gate([]),'review')]
for name,result,expected in cases:
    assert result['decision']==expected,(name,result)
assert len(cases[3][1]['failures'])==2
for bad in [float('nan'),float('inf'),-1,True]:
    try: gate([{'t':bad}])
    except ValueError: pass
    else: raise AssertionError('accepted invalid timestamp')
print('10 checks passed; synthetic fixtures only')