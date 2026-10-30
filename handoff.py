"""Structural validation only; declared status is not execution proof."""
import json
import sys

STATUSES = ("not_run", "pending", "succeeded", "failed")


def validate(obj):
    if not isinstance(obj, dict):
        return ["handoff: expected object"]
    errors = []
    for key in ("workflow", "version", "license"):
        v = obj.get(key)
        if not isinstance(v, str) or not v.strip():
            errors.append(key + ": expected nonempty string")
    if not isinstance(obj.get("inputs"), dict):
        errors.append("inputs: expected object")
    out = obj.get("expected_outputs")
    if (not isinstance(out, list) or not out or
            any(not isinstance(x, str) or not x.strip() for x in out)):
        errors.append("expected_outputs: expected nonempty list of strings")
    if obj.get("execution_status") not in STATUSES:
        errors.append("execution_status: invalid value")
    return errors


def self_test():
    good = dict(workflow="demo", version="1", inputs={},
                expected_outputs=["clip.mp4"], license="MIT",
                execution_status="not_run")
    missing = dict(good)
    del missing["version"]
    cases = [("valid", good, []),
             ("missing version", missing, ["version: expected nonempty string"]),
             ("empty expected_outputs", dict(good, expected_outputs=[]),
              ["expected_outputs: expected nonempty list of strings"]),
             ("invalid execution_status", dict(good, execution_status="maybe"),
              ["execution_status: invalid value"])]
    for name, obj, expected in cases:
        assert validate(obj) == expected, name
        print("PASS:", name)


if __name__ == "__main__":
    if not sys.argv[1:] or sys.argv[1:] == ["--self-test"]:
        self_test()
    elif len(sys.argv) == 2:
        with open(sys.argv[1], encoding="utf-8") as f:
            errors = validate(json.load(f))
        print(json.dumps({"valid": not errors, "errors": errors}))
        sys.exit(bool(errors))
    else:
        sys.exit("Usage: python handoff.py FILE.json | --self-test")