"""param_name_checker.py

Documentary utility: scan a ComfyUI workflow JSON exported from Krita AI Diffusion
and report duplicate parameter names — the condition that v1.53.0 now warns about.

Not tested against a live plugin. Input format assumed from changelog context only.
MIT licence.
"""
import json
import sys
from collections import Counter
from typing import Any


def collect_param_names(workflow: dict) -> list[str]:
    """Walk the workflow node graph and collect all 'name' fields that look
    like exposed Krita parameters. Heuristic: nodes with a 'krita_param' or
    '_meta' key containing 'title', or nodes whose class_type starts with
    'KritaOutput' / 'KritaInput'. This is a best-effort heuristic;
    actual plugin schema is not documented in the release notes."""
    names: list[str] = []
    nodes = workflow.get("nodes", workflow)  # handle flat or wrapped format
    if isinstance(nodes, dict):
        nodes = nodes.values()
    for node in nodes:
        if not isinstance(node, dict):
            continue
        # Heuristic 1: explicit 'param_name' field
        if "param_name" in node:
            names.append(node["param_name"])
        # Heuristic 2: widgets_values paired with input names
        inputs = node.get("inputs", {})
        if isinstance(inputs, dict):
            for k in inputs:
                if k.startswith("krita_"):
                    names.append(k)
    return names


def check_duplicates(workflow_path: str) -> dict[str, Any]:
    with open(workflow_path) as f:
        workflow = json.load(f)
    names = collect_param_names(workflow)
    counts = Counter(names)
    duplicates = {k: v for k, v in counts.items() if v > 1}
    return {
        "total_params_found": len(names),
        "unique": len(counts),
        "duplicates": duplicates,
        "ok": len(duplicates) == 0,
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python param_name_checker.py <workflow.json>")
        sys.exit(1)
    result = check_duplicates(sys.argv[1])
    print(json.dumps(result, indent=2))
    if not result["ok"]:
        print("WARNING: duplicate parameter names found — v1.53.0 will warn about these.")
        sys.exit(2)