#!/usr/bin/env python3
"""Local evidence collection, not generation or editorial certification."""
import argparse
import hashlib
import json
import math
from pathlib import Path
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


def collect(video, brief, output):
    video, brief, output = map(Path, (video, brief, output))
    if output.exists() or output.is_symlink():
        raise ValueError('output already exists; choose a new directory')
    if not video.is_file() or not brief.is_file():
        raise ValueError('video and brief must be existing local files')
    if video.stat().st_size > 8 * 1024 * 1024 or brief.stat().st_size > 65536:
        raise ValueError('input exceeds 8MiB video / 64KiB brief limit')
    if not shutil.which('ffprobe') or not shutil.which('ffmpeg'):
        raise ValueError('ffprobe and ffmpeg must already be installed')
    json.loads(brief.read_text())
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
        receipt = {
            'schema': 'veyrul-local-frame-evidence/1',
            'not_a_hub_api_contract': True,
            'video_sha256': video_sha, 'brief_sha256': brief_sha,
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
    p.add_argument('--output', required=True)
    args = p.parse_args()
    try:
        r = collect(args.video, args.brief, args.output)
    except (ValueError, OSError, KeyError, subprocess.TimeoutExpired) as e:
        p.exit(1, str(e) + '\n')
    print(json.dumps({'decoded_frames': r['decoded_frames'], 'review': 'unreviewed'}))
