"""verify_env.py — env check for FxNorm-Automix. Not executed. Set REPO_ROOT.
Pins from art_01M6JV03D8SRF5T8MH86SJWF0N rev 2: torch==1.9.0, librosa>=0.8.1, setuptools==59.5.0
"""
import json, sys, importlib
from pathlib import Path

REPO_ROOT = Path("PATH_TO_FXNORM_AUTOMIX")  # set before running
REQUIREMENTS = {"torch": "1.9.0", "librosa": "0.8.1", "setuptools": "59.5.0"}

def check(pkg, min_ver):
    try:
        mod = importlib.import_module(pkg)
        v = getattr(mod, "__version__", "unknown")
        return {"installed": v, "required": min_ver, "pass": v >= min_ver}
    except ImportError:
        return {"installed": None, "required": min_ver, "pass": False}

def cuda_info():
    try:
        import torch
        return {"available": torch.cuda.is_available(), "torch": torch.__version__}
    except ImportError:
        return {"available": False, "torch": None}

report = {
    "versions": {p: check(p, v) for p, v in REQUIREMENTS.items()},
    "cuda": cuda_info(),
    "repo_root_exists": REPO_ROOT.exists(),
}
Path("env_check.json").write_text(json.dumps(report, indent=2))
print(json.dumps(report, indent=2))
all_pass = all(v["pass"] for v in report["versions"].values()) and report["repo_root_exists"]
sys.exit(0 if all_pass else 1)