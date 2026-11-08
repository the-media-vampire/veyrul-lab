#!/usr/bin/env python3
"""Original regression proposal; not executed at publication. Python 3 + ffmpeg."""
import collections
import json
import subprocess
import sys


def run(n, vf):
    # Every input frame has a distinct constant gray value; no fonts/assets needed.
    data = b''.join(bytes([i * 17]) * 256 for i in range(n))
    cmd = ['ffmpeg', '-hide_banner', '-loglevel', 'error',
           '-f', 'rawvideo', '-pixel_format', 'gray', '-video_size', '16x16',
           '-framerate', '25', '-i', 'pipe:0', '-map', '0:v:0', '-an',
           '-vf', vf, '-fps_mode', 'passthrough', '-c:v', 'rawvideo',
           '-pix_fmt', 'gray', '-threads', '1', '-f', 'framemd5', 'pipe:1']
    p = subprocess.run(cmd, input=data, stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE)
    if p.returncode:
        raise RuntimeError(p.stderr.decode(errors='replace'))
    text = p.stdout.decode()
    rows = [line.split(',') for line in text.splitlines()
            if line.strip() and not line.startswith('#')]
    # framemd5 fields: stream, DTS, PTS, duration, size, hash.
    hashes = [r[-1].strip() for r in rows]
    return {'command': cmd, 'count': len(rows), 'hashes': hashes,
            'framemd5': text}


def main():
    version = subprocess.run(['ffmpeg', '-version'], check=True,
                             stdout=subprocess.PIPE).stdout.decode()
    report = {'ffmpeg_version': version, 'cases': [],
              'status': 'proposed assertions; actual results below'}
    failures = 0
    for n in (1, 7, 8, 9, 12, 13):
        for upstream in ('null', 'shuffleframes=0 2 1',
                         'shuffleframes=0 -1 2'):
            case = {'input_frames': n, 'upstream': upstream}
            try:
                base = run(n, upstream)
                chain = upstream + ',random=frames=8:seed=42'
                first, second = run(n, chain), run(n, chain)
                inventory_ok = (collections.Counter(base['hashes']) ==
                                collections.Counter(first['hashes']))
                repeat_ok = first['hashes'] == second['hashes']
                case.update(baseline=base, first=first, second=second,
                            inventory_preserved=inventory_ok,
                            fixed_seed_order_repeated=repeat_ok)
                failures += int(not (inventory_ok and repeat_ok))
            except RuntimeError as error:
                case['error'] = str(error)
                failures += 1
            report['cases'].append(case)
    report['failed_or_errored_cases'] = failures
    print(json.dumps(report, indent=2))
    return int(failures != 0)


if __name__ == '__main__':
    sys.exit(main())