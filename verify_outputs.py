"""Verify diff PNGs from Scout's run_experiment.sh.

Usage:
    python verify_outputs.py --out-dir ./out

Expected files in --out-dir:
    diff_nearest_vs_linear.png
    diff_linear_vs_cubic.png
    diff_linear_vs_default.png

Exit codes:
    0  all checks ran (results printed; non-zero diffs are not failures)
    1  a required file is missing
"""
import argparse
import sys
from pathlib import Path

def check_image(path: Path) -> dict:
    try:
        from PIL import Image
        import numpy as np
    except ImportError:
        return {"error": "pillow/numpy not installed"}
    if not path.exists():
        return {"error": f"file not found: {path}"}
    img = Image.open(path).convert("L")
    arr = np.array(img, dtype=float)
    return {
        "max": int(arr.max()),
        "mean": round(float(arr.mean()), 4),
        "all_black": bool(arr.max() == 0),
        "pixels": arr.size,
    }

CHECKS = [
    {
        "file": "diff_nearest_vs_linear.png",
        "note": "Non-zero expected: 4-entry LUT should show quantisation with nearest",
        "expect_nonzero": True,
    },
    {
        "file": "diff_linear_vs_cubic.png",
        "note": "Informational: zero means cubic adds no refinement at 4 entries",
        "expect_nonzero": None,
    },
    {
        "file": "diff_linear_vs_default.png",
        "note": "All-black -> default is linear; non-zero -> default is a different mode",
        "expect_nonzero": None,
    },
]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out-dir", default="./out")
    args = ap.parse_args()
    out = Path(args.out_dir)
    missing = []
    for c in CHECKS:
        path = out / c["file"]
        stats = check_image(path)
        status = "MISSING" if "error" in stats and "not found" in stats.get("error","") else ""
        if status:
            missing.append(c["file"])
        verdict = ""
        if "error" not in stats:
            if c["expect_nonzero"] is True:
                verdict = "PASS" if stats["max"] > 0 else "FAIL (unexpectedly all-black)"
            else:
                verdict = "all-black" if stats["all_black"] else f"non-zero (max={stats['max']})"
        print(f"\n{c['file']}")
        print(f"  note   : {c['note']}")
        if "error" in stats:
            print(f"  error  : {stats['error']}")
        else:
            print(f"  max    : {stats['max']}")
            print(f"  mean   : {stats['mean']}")
            print(f"  verdict: {verdict}")
    if missing:
        print(f"\nMissing files: {missing}. Run Scout's run_experiment.sh first.")
        sys.exit(1)

if __name__ == "__main__":
    main()