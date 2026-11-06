"""probe_stem_layout_extended.py — stem-layout probe. Not executed. Set REPO_ROOT.
Extends 5a438a01/probe_stem_layout.py; writes stem_layout.json.
Source: art_01M6JV03D8SRF5T8MH86SJWF0N rev 2.
"""
import json, ast, sys
from pathlib import Path

REPO_ROOT = Path("PATH_TO_FXNORM_AUTOMIX")  # set before running
CANDIDATES = ["inference.py", "infer.py", "run_inference.py", "test.py"]

def find_entry(root):
    for name in CANDIDATES:
        p = root / name
        if p.exists(): return p
    for p in root.rglob("inference*.py"): return p
    return None

def stem_hints(src):
    hits = []
    try:
        for node in ast.walk(ast.parse(src)):
            if isinstance(node, ast.Assign):
                for t in node.targets:
                    if getattr(t, "id", "").lower() in ("stems","sources","instruments","stem_names"):
                        if isinstance(node.value, ast.List):
                            hits.append({"var": t.id, "values": [e.s for e in node.value.elts if isinstance(e, ast.Constant)]})
    except SyntaxError as e:
        hits.append({"error": str(e)})
    return hits

entry = find_entry(REPO_ROOT)
result = {"entry_point": str(entry), "entry_found": entry is not None and entry.exists(), "stem_hints": []}
if result["entry_found"]:
    result["stem_hints"] = stem_hints(entry.read_text())
Path("stem_layout.json").write_text(json.dumps(result, indent=2))
print(json.dumps(result, indent=2))
sys.exit(0 if result["entry_found"] else 1)