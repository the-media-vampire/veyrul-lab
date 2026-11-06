"""Stem layout probe template for FxNorm-Automix.

Purpose: determine the stem count, order and expected format before
attempting inference. The README does not state these; this script
template prints what the inference script actually loads.

Usage (after environment setup and weight-term confirmation):
    python probe_stem_layout.py --repo /path/to/fxnorm-automix

This is a template only; fill in the import path once the repo is cloned.
Do not run before confirming weight and data licence terms.
"""
import argparse
import sys

def probe(repo_path: str) -> None:
    sys.path.insert(0, repo_path)
    # Attempt to import inference entry point and inspect its argument parser
    # or its data-loading function to surface stem expectations.
    # Replace the placeholder below with the actual module name from the repo.
    try:
        import importlib
        # Common patterns in research releases:
        for candidate in ["inference", "run_inference", "test", "mixing"]:
            try:
                mod = importlib.import_module(candidate)
                print(f"Found module: {candidate}")
                # Print all top-level callables and their signatures
                import inspect
                for name, obj in inspect.getmembers(mod, callable):
                    try:
                        sig = inspect.signature(obj)
                        print(f"  {name}{sig}")
                    except (ValueError, TypeError):
                        pass
                break
            except ModuleNotFoundError:
                continue
        else:
            print("No standard inference module found. Inspect repo manually.")
    except Exception as exc:
        print(f"Probe failed: {exc}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Probe FxNorm-Automix stem layout")
    parser.add_argument("--repo", required=True, help="Path to cloned fxnorm-automix repo")
    args = parser.parse_args()
    probe(args.repo)