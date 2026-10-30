"""summarise.py — print verdict counts and mismatches from a compliance log."""
import json, sys
from collections import Counter
from pathlib import Path

data = json.loads(Path(sys.argv[1] if len(sys.argv)>1 else "compliance_log_example.json").read_text())
counts = Counter(e["verdict"] for e in data["entries"])
print(f"Clip: {data['clip_label']} | source: {data['source_record_id']} r{data['source_revision']}")
print(f"Inspection: {data['inspection_method']} | stills: {data.get('still_count')} | lanes: {data.get('lanes')}")
print("Verdicts:", dict(counts))
for v in ("mismatch","open_call","unverifiable"):
    items = [e for e in data["entries"] if e["verdict"]==v]
    if items:
        print(f"\n{v.upper()}:")
        for e in items:
            print(f"  block {e['block']}: {e['clause']}")
            if e.get("conservative"): print("    (conservative label)")
print("\nNOTE: mismatches are model-compliance failures, not authoring errors.")