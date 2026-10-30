from eye_pair import assess

b = dict(clip='synthetic', subject='A', eye='left', t=1.0, ref='synthetic:1', method='fixture', state='nonred')
a = dict(b, t=2.0, ref='synthetic:2', state='red')
cases = [
    ('paired change', assess(b,a), 'pass'),
    ('closed baseline', assess(dict(b,state='closed'),a), 'unknown'),
    ('closed reveal', assess(dict(b,state='closed'),a,rule='red_reveal'), 'pass'),
    ('identity swap', assess(b,dict(a,subject='B')), 'unknown'),
    ('no late sample', assess(b,a,terminal_window=(3,4)), 'unknown'),
    ('missing reference', assess(b,dict(a,ref='')), 'unknown'),
    ('no observed change', assess(b,dict(a,state='nonred')), 'fail'),
    ('reversed time', assess(a,b), 'unknown'),
    ('invalid time', assess(b,dict(a,t=float('nan'))), 'unknown'),
]
for name, result, expected in cases:
    assert result['outcome'] == expected, (name, result)
    assert result['promotable'] == (expected != 'unknown')
print('9/9 synthetic assertions passed')