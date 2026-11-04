"""assert_fixture.py
Run: python3 assert_fixture.py reveal-test-abc.json
Verifies structural invariants for the three-variant reveal-test fixture.
Execution confirmed: artifact 9613d31f-6d59-4f0f-89f0-69a251ee505f
"""
import json, hashlib, sys

path = sys.argv[1] if len(sys.argv) > 1 else "reveal-test-abc.json"
with open(path) as f:
    data = json.load(f)

variants = data["variants"]
reveal = data["reveal_beat"]
pre_window = set(range(4, 8))

results = []
for name, v in variants.items():
    onsets = v["note_onsets_beats"]
    pre = [o for o in onsets if o in pre_window]
    at_reveal = reveal in onsets
    sha = hashlib.sha256(json.dumps(onsets).encode()).hexdigest()[:16]
    results.append({"name": name, "onsets": onsets, "pre": pre, "at_reveal": at_reveal, "sha": sha})
    print(f"{name}: onsets={onsets} pre={pre} at_reveal={at_reveal} sha={sha}")

# Discriminating assertions
A = next(r for r in results if "withheld" in r["name"])
B = next(r for r in results if "steady" in r["name"])
C = next(r for r in results if "sparse" in r["name"])

asserts = [
    (A["pre"] == [], "A is silent before reveal"),
    (C["pre"] == [], "C is silent before reveal"),
    (bool(B["pre"]), "B is active before reveal"),
    (A["at_reveal"] and B["at_reveal"] and C["at_reveal"], "All fire at reveal beat"),
    (len({A["sha"], B["sha"], C["sha"]}) == 3, "All onset lists are byte-distinct"),
    (len(A["onsets"]) != len(C["onsets"]), "Note count confound present (C != A) — document it"),
]

print()
all_pass = True
for check, label in asserts:
    status = "PASS" if check else "FAIL"
    if not check:
        all_pass = False
    print(f"  [{status}] {label}")

sys.exit(0 if all_pass else 1)