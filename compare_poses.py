"""Compare canonical world-space pose CSVs. Python standard library only.
No Blender or Godot execution is performed by this program.
"""
import argparse
import csv
import json
import math

FIELDS = ['frame', 'x', 'y', 'z', 'qw', 'qx', 'qy', 'qz']

def load(path):
    poses = {}
    with open(path, newline='', encoding='utf-8') as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames != FIELDS:
            raise ValueError('Expected columns: ' + ','.join(FIELDS))
        for row in reader:
            frame = int(row['frame'])
            if frame in poses:
                raise ValueError('Duplicate frame')
            values = [float(row[k]) for k in FIELDS[1:]]
            if not all(math.isfinite(v) for v in values):
                raise ValueError('Nonfinite pose')
            position, quaternion = values[:3], values[3:]
            norm = math.sqrt(sum(q*q for q in quaternion))
            if norm < 1e-12:
                raise ValueError('Zero quaternion')
            poses[frame] = (position, [q/norm for q in quaternion])
    if not poses:
        raise ValueError('Empty pose file')
    return poses

def compare(reference, candidate, pos_limit, angle_limit):
    if set(reference) != set(candidate):
        raise ValueError('Frame sets differ; do not silently drop samples')
    errors = []
    for frame in sorted(reference):
        p, q = reference[frame]
        r, s = candidate[frame]
        distance = math.sqrt(sum((a-b)**2 for a, b in zip(p, r)))
        dot = min(1.0, abs(sum(a*b for a, b in zip(q, s))))
        angle = math.degrees(2*math.acos(dot))
        errors.append((frame, distance, angle))
    worst_position = max(errors, key=lambda e: e[1])
    worst_angle = max(errors, key=lambda e: e[2])
    return {
        'samples': len(errors),
        'position_rms_m': math.sqrt(sum(e[1]**2 for e in errors)/len(errors)),
        'position_max_m': worst_position[1],
        'position_worst_frame': worst_position[0],
        'rotation_max_degrees': worst_angle[2],
        'rotation_worst_frame': worst_angle[0],
        'pass_sampled_position_rotation_only':
            worst_position[1] <= pos_limit and worst_angle[2] <= angle_limit,
    }

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('reference')
    parser.add_argument('candidate')
    parser.add_argument('--position-limit-m', required=True, type=float)
    parser.add_argument('--angle-limit-deg', required=True, type=float)
    args = parser.parse_args()
    limits = [args.position_limit_m, args.angle_limit_deg]
    if not all(math.isfinite(v) and v >= 0 for v in limits):
        parser.error('Limits must be finite and nonnegative')
    result = compare(load(args.reference), load(args.candidate), *limits)
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result['pass_sampled_position_rotation_only'] else 1)