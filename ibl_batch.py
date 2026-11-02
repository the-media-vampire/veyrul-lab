import json, re
from pathlib import PurePosixPath
SOURCE = {'record_id':'art_01M6F25MHDZ019EYGX9CNFZYRE','revision':1,'commit':'bd32f8a9ae502df5797ad18c705312eda247dbfd'}
def plan(executable, input_path, output_dir, passes):
    """Return argv lists only. Paths are POSIX lexical paths, not filesystem checks."""
    if not all(isinstance(x,str) and x and '\x00' not in x for x in (executable,input_path,output_dir)):
        raise ValueError('nonempty NUL-free paths required')
    if not passes:
        raise ValueError('at least one pass required')
    jobs, occupied = [], set()
    for name, distribution in passes:
        if not isinstance(name,str) or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]{0,63}',name):
            raise ValueError('unsafe pass name')
        if distribution not in ('GGX','Lambertian','Charlie'):
            raise ValueError('undocumented distribution')
        cube = str(PurePosixPath(output_dir) / (name+'.ktx2'))
        lut = str(PurePosixPath(output_dir) / (name+'-lut.png'))
        for path in (cube,lut):
            key = path.casefold()
            if key in occupied:
                raise ValueError('output collision')
            occupied.add(key)
        argv = [executable,'-inputPath',input_path,'-outCubeMap',cube,
                '-outLUT',lut,'-distribution',distribution,'-sampleCount','1024',
                '-targetFormat','R16G16B16A16_SFLOAT']
        jobs.append({'name':name,'distribution':distribution,'argv':argv,
                     'planned_outputs':{'cube':cube,'lut':lut}})
    return {'source':dict(SOURCE),'state':'planned_not_executed','jobs':jobs,
            'consumer_contract':'Consumer must confirm distribution, roughness/LOD mapping, orientation and KTX support; filenames do not establish compatibility.'}

def tests():
    passed = 0
    p = plan('/tools/cli','HDR inputs/studio.hdr','build/IBL assets',[('specular','GGX'),('diffuse','Lambertian')])
    assert len(p['jobs']) == 2; passed += 1
    paths = [v for j in p['jobs'] for v in j['planned_outputs'].values()]
    assert len(set(paths)) == 4; passed += 1
    assert p['jobs'][0]['argv'][2] == 'HDR inputs/studio.hdr'; passed += 1
    assert p['state'] == 'planned_not_executed'; passed += 1
    for passes in ([('A','GGX'),('a','Lambertian')],[('../escape','GGX')],[('x','unknown')],[]):
        try: plan('cli','a.hdr','out',passes)
        except ValueError: passed += 1
        else: raise AssertionError(passes)
    assert json.loads(json.dumps(p)) == p; passed += 1
    print(json.dumps({'tests_passed':passed,'sampler_executed':False,'example':p},indent=2))
if __name__ == '__main__': tests()