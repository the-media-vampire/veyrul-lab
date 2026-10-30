"""Summarise a ShotOrderComplianceLog JSON file.

Usage: python compliance_summary.py log.json

The schema is defined in compliance_log_schema.json.
Upstream authoring contract: artifact 8670325a (Theo, this task).
Source observation: art_01M64VKF6MVCCAAVV3YZS2A2TY r2.
"""
import json, sys
from collections import Counter

VERDICT_ORDER = ["match", "mismatch", "open_call", "unverifiable"]

def summarise(path: str) -> None:
    with open(path) as f:
        log = json.load(f)

    print(f"Source : {log['source_record']} r{log['source_revision']}")
    print(f"Method : {log['inspection_method']}")
    if log.get('upstream_contract'):
        print(f"Authoring contract: {log['upstream_contract']}")
    print()

    for run in log["runs"]:
        counts: Counter = Counter()
        print(f"Run: {run['run_id']}")
        for clause in run["clauses"]:
            v = clause["verdict"]
            counts[v] += 1
            tc = f" @ {clause['timecodes']}s" if clause.get("timecodes") else ""
            note = f" — {clause['note']}" if clause.get("note") else ""
            print(f"  {clause['clause']:30s}  {v}{tc}{note}")
        print(f"  Totals: { {k: counts[k] for k in VERDICT_ORDER if k in counts} }")
        print()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python compliance_summary.py <log.json>")
        sys.exit(1)
    summarise(sys.argv[1])