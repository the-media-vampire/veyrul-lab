#!/usr/bin/env python3
"""Temporal luma summariser.

Usage:
    python luma_temporal.py luma_fixture.csv --threshold 5

Reads a CSV with a 'frame' column and one or more luma columns.
For each luma column prints: range, transition count (abs diff > threshold)
and mean absolute step across adjacent frames.

Expected results for luma_fixture.csv (threshold=5):
  stable:          range 105-105, transitions=0, mean_step=0.00
  repeated_change: range 100-110, transitions=7, mean_step=10.00
  single_step:     range 100-110, transitions=1, mean_step=1.43

These expected values are derived from the fixture by hand arithmetic.
No FFmpeg execution is implied or performed here.
"""
import csv, sys, argparse

def analyse(values, threshold):
    lo, hi = min(values), max(values)
    diffs = [abs(values[i+1] - values[i]) for i in range(len(values)-1)]
    transitions = sum(1 for d in diffs if d > threshold)
    mean_step = sum(diffs) / len(diffs) if diffs else 0.0
    return lo, hi, transitions, mean_step

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('csv_file')
    parser.add_argument('--threshold', type=float, default=5.0,
                        help='Abs diff threshold for counting a transition (default 5)')
    args = parser.parse_args()

    with open(args.csv_file, newline='') as f:
        rows = list(csv.DictReader(f))

    if not rows:
        print('ERROR: no data rows found', file=sys.stderr)
        sys.exit(1)

    cols = [k for k in rows[0] if k != 'frame']
    print(f'threshold={args.threshold}  rows={len(rows)}')
    print(f'{"column":<20} {"min":>5} {"max":>5} {"transitions":>12} {"mean_step":>10}')
    print('-' * 60)
    for col in cols:
        vals = [float(r[col]) for r in rows]
        lo, hi, tr, ms = analyse(vals, args.threshold)
        print(f'{col:<20} {lo:>5.0f} {hi:>5.0f} {tr:>12} {ms:>10.2f}')

if __name__ == '__main__':
    main()