"""Rhubarb Lip Sync output validator.

Checks three structural invariants from the documented spec
(art_01M6DT6179CWW876NPJ5MY0MV7 r1):
  1. TSV: first timestamp is 0.00
  2. XML/JSON: each cue's end equals the next cue's start (no gaps)
  3. All shape values are in {A, B, C, D, E, F, G, H, X}

Usage:
    python rhubarb_validate.py output.tsv
    python rhubarb_validate.py output.xml
    python rhubarb_validate.py output.json

Exits 0 if valid, 1 if issues found.
"""
import sys, json, xml.etree.ElementTree as ET

VALID_SHAPES = set("ABCDEFGHX")


def validate_tsv(text):
    issues = []
    lines = [l for l in text.strip().splitlines() if l.strip()]
    if not lines:
        return ["file is empty"]
    first_ts = float(lines[0].split("\t")[0])
    if first_ts != 0.0:
        issues.append(f"first timestamp {first_ts} != 0.0")
    for i, line in enumerate(lines):
        parts = line.split("\t")
        if len(parts) != 2:
            issues.append(f"line {i}: expected 2 columns, got {len(parts)}")
            continue
        shape = parts[1].strip()
        if shape not in VALID_SHAPES:
            issues.append(f"line {i}: unknown shape '{shape}'")
    return issues


def validate_xml(text):
    issues = []
    root = ET.fromstring(text)
    cues = root.findall("mouthCue")
    for i, (a, b) in enumerate(zip(cues, cues[1:])):
        end_a = float(a.get("end"))
        start_b = float(b.get("start"))
        if abs(end_a - start_b) > 1e-9:
            issues.append(f"cue {i}: end {end_a} != next start {start_b}")
        shape = a.get("value", "")
        if shape not in VALID_SHAPES:
            issues.append(f"cue {i}: unknown shape '{shape}'")
    if cues:
        shape = cues[-1].get("value", "")
        if shape not in VALID_SHAPES:
            issues.append(f"last cue: unknown shape '{shape}'")
    return issues


def validate_json(text):
    issues = []
    data = json.loads(text)
    cues = data.get("mouthCues", [])
    for i, (a, b) in enumerate(zip(cues, cues[1:])):
        if abs(a["end"] - b["start"]) > 1e-9:
            issues.append(f"cue {i}: end {a['end']} != next start {b['start']}")
        if a["value"] not in VALID_SHAPES:
            issues.append(f"cue {i}: unknown shape '{a['value']}'")
    if cues and cues[-1]["value"] not in VALID_SHAPES:
        issues.append(f"last cue: unknown shape '{cues[-1]['value']}'")
    return issues


def validate_file(path):
    with open(path) as fh:
        text = fh.read()
    ext = path.rsplit(".", 1)[-1].lower()
    if ext == "tsv" or ext == "txt":
        return validate_tsv(text)
    elif ext == "xml":
        return validate_xml(text)
    elif ext == "json":
        return validate_json(text)
    else:
        return [f"unrecognised extension '{ext}'; use .tsv/.txt, .xml or .json"]


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: python rhubarb_validate.py <file>")
        sys.exit(1)
    issues = validate_file(sys.argv[1])
    if issues:
        for iss in issues:
            print("ERROR:", iss)
        sys.exit(1)
    print("OK")
    sys.exit(0)