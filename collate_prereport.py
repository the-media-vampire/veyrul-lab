"""collate_prereport.py — merges env_check.json + stem_layout.json -> pre_run_report.json.
Appends a row to results_log_template.csv from artifact 5a438a01. Not executed.
"""
import json, csv, datetime
from pathlib import Path

env = json.loads(Path("env_check.json").read_text()) if Path("env_check.json").exists() else {}
stems = json.loads(Path("stem_layout.json").read_text()) if Path("stem_layout.json").exists() else {}
report = {"env": env, "stems": stems, "timestamp_utc": datetime.datetime.utcnow().isoformat()}
Path("pre_run_report.json").write_text(json.dumps(report, indent=2))
print("pre_run_report.json written")

csv_path = Path("results_log_template.csv")
if csv_path.exists():
    env_pass = all(v.get("pass") for v in env.get("versions", {}).values())
    row = {"condition": "pre_run_check", "ir_set": "n/a", "model": "n/a",
           "env_pass": env_pass, "stem_layout_found": stems.get("entry_found", False),
           "notes": json.dumps(stems.get("stem_hints", []))[:180]}
    with open(csv_path, "a", newline="") as f:
        csv.DictWriter(f, fieldnames=row.keys(), extrasaction="ignore").writerow(row)
    print("Row appended to results_log_template.csv")