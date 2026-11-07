#!/usr/bin/env python3
"""Run with Python 3: python3 evaluate.py /path/to/changelog-lint.sh
Unexecuted source. Requires bash. Uses only synthetic local fixtures.
"""
import json
import pathlib
import subprocess
import sys
import tempfile

cases = json.loads(pathlib.Path(__file__).with_name('cases.json').read_text())
script = pathlib.Path(sys.argv[1]).resolve()
results = []
with tempfile.TemporaryDirectory() as directory:
    for case in cases:
        path = pathlib.Path(directory) / (case['id'] + '.md')
        path.write_text(case['text'])
        run = subprocess.run(['bash', str(script), str(path)], capture_output=True, text=True)
        explicit_failures = sum(line.strip().startswith('FAIL  ') for line in run.stdout.splitlines())
        results.append({
            'case': case['id'], 'actual_exit': run.returncode,
            'local_rubric_expected_exit': case['expected_exit'],
            'exit_matches_rubric': run.returncode == case['expected_exit'],
            'explicit_failure_lines': explicit_failures,
            'known_upgrade_fact_recall': case['fact_recall'],
            'stdout': run.stdout, 'stderr': run.stderr,
        })
print(json.dumps(results, indent=2))
# Report, rather than silently turning a mismatch into a new conformance rule.