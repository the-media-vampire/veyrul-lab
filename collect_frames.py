#!/usr/bin/env python3
"""Local evidence collection, not generation or editorial certification."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import re
import shutil
import subprocess


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(65536), b''):
            h.update(block)
    return h.hexdigest()


def command(args):
    r = subprocess.run(args, capture_output=True, timeout=45, check=False)
    if r.returncode:
        raise ValueError('media command failed; no successful evidence receipt')
    if len(r.stdout) > 524288:
        raise ValueError('metadata exceeds bounded input size')
    return r.stdout


def strict_json(raw):
    def unique(pairs):
        value = {}
        for key, item in pairs:
            if key in value:
                raise ValueError('duplicate JSON property')
            value[key] = item
        return value
    def bad_constant(_):
        raise ValueError('nonfinite JSON number')
    return json.loads(raw, object_pairs_hook=unique, parse_constant=bad_constant)


def text(value, label):
    if not isinstance(value, str) or not value.strip() or len(value) > 200:
        raise ValueError('missing or invalid ' + label)
    return value


def digest_text(value):
    if not isinstance(value, str) or not re.fullmatch('[a-f0-9]{64}', value):
        raise ValueError('expected a lowercase SHA256 digest')
    return value


def pointer_value(value, pointer):
    if not isinstance(pointer, str) or not pointer.startswith('/') or len(pointer) > 256:
        raise ValueError('invalid seed JSON pointer')
    try:
        for token in pointer[1:].split('/'):
            if re.search(r'~(?![01])', token):
                raise ValueError('invalid seed JSON pointer escape')
            token = token.replace('~1', '/').replace('~0', '~')
            if isinstance(value, list):
                if not re.fullmatch('0|[1-9][0-9]*', token):
                    raise ValueError('invalid seed array index')
                value = value[int(token)]
            elif isinstance(value, dict):
                value = value[token]
            else:
                raise ValueError('seed pointer does not reach a value')
    except (KeyError, IndexError):
        raise ValueError('seed pointer is absent from exported workflow') from None
    return value


def run_binding(metadata, workflow):
    if metadata is None and workflow is None:
        return {'status': 'not_supplied', 'reproduction_status': 'not_tested'}, []
    if metadata is None or workflow is None:
        raise ValueError('run metadata and exported workflow must be supplied together')
    metadata, workflow = Path(metadata), Path(workflow)
    sources = []
    values = []
    for path, limit in ((metadata, 65536), (workflow, 524288)):
        if not path.is_file() or path.stat().st_size > limit:
            raise ValueError('run metadata/workflow missing or too large')
        raw = path.read_bytes()
        if len(raw) > limit:
            raise ValueError('run input grew beyond its limit')
        sources.append((path, hashlib.sha256(raw).hexdigest()))
        values.append(strict_json(raw))
    info, graph = values
    required = {'schema', 'seeds', 'workflow_sha256', 'input_sha256', 'model', 'runtime'}
    if not isinstance(info, dict) or set(info) != required or info['schema'] != 'veyrul-run-metadata/1':
        raise ValueError('unsupported or incomplete run metadata')
    if digest_text(info['workflow_sha256']) != sources[1][1]:
        raise ValueError('exported workflow digest mismatch')
    seeds = info['seeds']
    if not isinstance(seeds, list) or not 1 <= len(seeds) <= 16:
        raise ValueError('provide one through16 seed bindings')
    seen = set()
    for seed in seeds:
        if not isinstance(seed, dict) or set(seed) != {'pointer', 'value'}:
            raise ValueError('invalid seed binding')
        n = seed['value']
        if type(n) is not int or not 0 <= n <= 2**53 - 1:
            raise ValueError('seed must be an integer from0 through9007199254740991')
        actual = pointer_value(graph, seed['pointer'])
        if type(actual) is not int or actual != n:
            raise ValueError('declared seed differs from exported workflow')
        if seed['pointer'] in seen:
            raise ValueError('duplicate seed pointer')
        seen.add(seed['pointer'])
    inputs = info['input_sha256']
    if not isinstance(inputs, list) or not 1 <= len(inputs) <= 8:
        raise ValueError('provide input image digests')
    for item in inputs:
        digest_text(item)
    model = info['model']
    if not isinstance(model, dict) or set(model) != {'name', 'weights'}:
        raise ValueError('provide model name and weight digests')
    text(model['name'], 'model name')
    if not isinstance(model['weights'], list) or not 1 <= len(model['weights']) <= 16:
        raise ValueError('provide model weight digests')
    for weight in model['weights']:
        if not isinstance(weight, dict) or set(weight) != {'name', 'sha256'}:
            raise ValueError('invalid weight description')
        text(weight['name'], 'weight name')
        digest_text(weight['sha256'])
    runtime = info['runtime']
    if not isinstance(runtime, dict) or set(runtime) != {'engine', 'revision', 'node_versions', 'hardware'}:
        raise ValueError('provide runtime, node versions and hardware')
    for key in ('engine', 'revision', 'hardware'):
        text(runtime[key], key)
    nodes = runtime['node_versions']
    if not isinstance(nodes, dict) or not 1 <= len(nodes) <= 64:
        raise ValueError('provide node versions')
    for key, value in nodes.items():
        text(key, 'node name')
        text(value, 'node version')
    return {'status': 'bound_to_receipt', 'metadata_sha256': sources[0][1],
            'workflow_sha256': sources[1][1], 'seed_bindings': seeds,
            'operator_reported': {'input_sha256': inputs, 'model': model, 'runtime': runtime},
            'seed_coverage': 'operator_declared_pointers_only',
            'execution_status': 'not_verified', 'reproduction_status': 'not_tested'}, sources


def verify_run_binding(evidence, video, brief, metadata, workflow):
    evidence = Path(evidence)
    if not evidence.is_file() or evidence.stat().st_size > 262144:
        raise ValueError('evidence receipt missing or too large')
    receipt = strict_json(evidence.read_bytes())
    if not isinstance(receipt, dict) or receipt.get('schema') != 'veyrul-local-frame-evidence/2':
        raise ValueError('expected a version2 evidence receipt')
    binding, sources = run_binding(metadata, workflow)
    if not sources or receipt.get('run') != binding:
        raise ValueError('run metadata/seed binding differs from receipt')
    for label, path, limit in (('video', Path(video), 8 * 1024 * 1024), ('brief', Path(brief), 65536)):
        if not path.is_file() or path.stat().st_size > limit or sha(path) != receipt.get(label + '_sha256'):
            raise ValueError(label + ' digest differs from receipt')
    return {'run_binding': 'matched', 'reproduction': 'not_tested',
            'editorial_review': 'not_verified', 'frame_previews': 'not_checked'}


def collect(video, brief, output, metadata=None, workflow=None):
    video, brief, output = map(Path, (video, brief, output))
    if output.exists() or output.is_symlink():
        raise ValueError('output already exists; choose a new directory')
    if not video.is_file() or not brief.is_file():
        raise ValueError('video and brief must be existing local files')
    if video.stat().st_size > 8 * 1024 * 1024 or brief.stat().st_size > 65536:
        raise ValueError('input exceeds 8MiB video / 64KiB brief limit')
    if not shutil.which('ffprobe') or not shutil.which('ffmpeg'):
        raise ValueError('ffprobe and ffmpeg must already be installed')
    strict_json(brief.read_text())
    binding, run_sources = run_binding(metadata, workflow)
    video_sha, brief_sha = sha(video), sha(brief)
    base = ['ffprobe', '-v', 'error', '-protocol_whitelist', 'file,pipe',
            '-select_streams', 'v:0']
    meta = json.loads(command(base + ['-show_streams', '-show_format',
                                      '-of', 'json', str(video.resolve())]))
    streams = meta.get('streams', [])
    if len(streams) != 1:
        raise ValueError('one selected video stream is required')
    stream = streams[0]
    duration = float(meta.get('format', {}).get('duration', 'nan'))
    if not math.isfinite(duration) or not 0 < duration <= 10:
        raise ValueError('only clips up to 10 seconds are supported')
    if not (0 < stream['width'] <= 4096 and 0 < stream['height'] <= 4096):
        raise ValueError('unsupported source dimensions')
    data = json.loads(command(base + ['-show_frames', '-show_entries',
                                      'frame=best_effort_timestamp_time',
                                      '-of', 'json', str(video.resolve())]))
    times = [float(f['best_effort_timestamp_time']) for f in data.get('frames', [])]
    if not 2 <= len(times) <= 241 or not all(math.isfinite(t) for t in times):
        raise ValueError('expected 2 through 241 frames with finite timestamps')
    if any(b <= a for a, b in zip(times, times[1:])):
        raise ValueError('frame timestamps must be strictly increasing')
    output.mkdir(parents=True, exist_ok=False)
    frames = output / 'frames'
    frames.mkdir()
    try:
        command(['ffmpeg', '-v', 'error', '-nostdin', '-n',
                 '-protocol_whitelist', 'file,pipe', '-i', str(video.resolve()),
                 '-map', '0:v:0', '-an', '-sn', '-dn', '-frames:v', '242',
                 '-vf', 'scale=320:180:force_original_aspect_ratio=decrease',
                 '-fps_mode', 'passthrough', '-q:v', '4',
                 str(frames / '%06d.jpg')])
        files = sorted(frames.glob('*.jpg'))
        if len(files) != len(times):
            raise ValueError('decoded frame count differs from probed count')
        if sum(f.stat().st_size for f in files) > 12 * 1024 * 1024:
            raise ValueError('preview frames exceed 12MiB limit')
        if sha(video) != video_sha or sha(brief) != brief_sha:
            raise ValueError('source changed during collection')
        if any(sha(path) != expected for path, expected in run_sources):
            raise ValueError('run input changed during collection')
        receipt = {
            'schema': 'veyrul-local-frame-evidence/2',
            'not_a_hub_api_contract': True,
            'video_sha256': video_sha, 'brief_sha256': brief_sha,
            'run': binding,
            'source_dimensions': [stream['width'], stream['height']],
            'duration_seconds': duration, 'decoded_frames': len(files),
            'frames': [{'index': i, 'presentation_time_seconds': t,
                        'relative_time_seconds': t - times[0],
                        'path': 'frames/' + f.name, 'sha256': sha(f)}
                       for i, (t, f) in enumerate(zip(times, files))],
            'checks': {'all_decoded_frames_extracted': True,
                       'source_bytes_unchanged': True},
            'review': {'status': 'unreviewed', 'source_fidelity': 'unknown',
                       'unsupported_arrival': 'unknown',
                       'illustration_label': 'unknown', 'audio': 'not_inspected'},
            'limitations': [
                'Preview frames are downscaled; inspect the original video for detail and motion.',
                'Extraction and hashes do not establish visual correctness, rights or model execution.',
                'A review must identify this exact clip and brief plus frame/time evidence.',
                'Seed and file binding do not prove the declared workflow generated the clip or can reproduce it.',
                'No network, render submission, paid service or model judgement is performed.'
            ]
        }
        (output / 'EVIDENCE.json').write_text(json.dumps(receipt, indent=2) + '\n')
        return receipt
    except Exception:
        (output / 'INCOMPLETE.txt').write_text('Collection failed. Partial previews are not a successful receipt. Original inputs were not deleted.\n')
        raise


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--video', required=True)
    p.add_argument('--brief', required=True)
    destination = p.add_mutually_exclusive_group(required=True)
    destination.add_argument('--output')
    destination.add_argument('--verify-evidence')
    p.add_argument('--run-metadata')
    p.add_argument('--workflow')
    args = p.parse_args()
    try:
        if args.verify_evidence:
            r = verify_run_binding(args.verify_evidence, args.video, args.brief,
                                   args.run_metadata, args.workflow)
        else:
            r = collect(args.video, args.brief, args.output, args.run_metadata, args.workflow)
    except (ValueError, OSError, KeyError, subprocess.TimeoutExpired) as e:
        p.exit(1, str(e) + '\n')
    print(json.dumps(r if args.verify_evidence else {'decoded_frames': r['decoded_frames'],
                     'review': 'unreviewed', 'run_binding': r['run']['status'],
                     'reproduction': 'not_tested'}))
