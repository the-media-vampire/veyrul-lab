"""Minimal pre-import check for the doorway dual-dialogue pair.

Runs with stdlib only. Confirms:
  A: SOL cue carries ^ (dual-dialogue token present)
  B: SOL cue has no ^ (sequential)
  Dialogue wording: identical across variants
  SHA-256 prefixes: distinct (different files)

Execution evidence: run_python artifact 92129848-8d5e-4afd-b2a0-e6fda09ca688
"""
import re, hashlib

FILES = {
    "A_simultaneous": "doorway-simultaneous.fountain",
    "B_sequential": "doorway-sequential.fountain",
}

def sha256_prefix(text, n=16):
    return hashlib.sha256(text.encode()).hexdigest()[:n]

def dual_cues(text):
    return re.findall(r'^([A-Z][A-Z0-9 ]*)\s*\^$', text, re.MULTILINE)

def dialogue_lines(text):
    return re.findall(r'^[A-Z][A-Z0-9 ]*(?:\s*\^)?\n(.+)$', text, re.MULTILINE)

results = {}
for label, path in FILES.items():
    with open(path) as f:
        src = f.read()
    results[label] = {
        "sha256_prefix": sha256_prefix(src),
        "dual_cues": dual_cues(src),
        "dialogue": dialogue_lines(src),
    }

a, b = results["A_simultaneous"], results["B_sequential"]
assert a["dual_cues"], "FAIL: A missing dual-dialogue cue"
assert not b["dual_cues"], "FAIL: B should have no dual-dialogue cue"
assert a["dialogue"] == b["dialogue"], "FAIL: dialogue wording differs"
assert a["sha256_prefix"] != b["sha256_prefix"], "FAIL: files are byte-identical"

print("PASS")
for label, r in results.items():
    print(f"  {label}: sha={r['sha256_prefix']} dual={r['dual_cues']} lines={r['dialogue']}")