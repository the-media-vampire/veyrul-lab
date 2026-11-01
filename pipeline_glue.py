"""Illustrative Python glue for the attach-and-verify stage.
Documentary only — not run. Requires c2pa-python>=0.38.3, Python>=3.10.
See README.md for interface contract and assumptions.
"""
from __future__ import annotations
import json, sys
from pathlib import Path

class C2PAStageError(Exception):
    def __init__(self, code: str, detail: str):
        self.code = code
        super().__init__(f"{code}: {detail}")

def attach_and_verify(
    asset_path: Path,
    manifest_def: Path,
    output_path: Path,
    signer_config: Path,
    trust_anchor: str | None = None,
) -> dict:
    """Returns manifest report dict on success; raises C2PAStageError on failure."""
    if not asset_path.exists():
        raise C2PAStageError("FORMAT_UNSUPPORTED", f"not found: {asset_path}")
    cfg = json.loads(signer_config.read_text())
    if "private_key" in cfg:
        raise C2PAStageError("KEY_CONFIG_ERR", "Embedded key; use KMS/HSM.")
    # Real code: call c2pa.Builder to sign, then c2pa.Reader to verify.
    # builder = Builder(manifest_def=manifest_def.read_text())
    # builder.sign(asset_path, output_path, signer_config=cfg)
    # report = Reader(str(output_path)).json()
    report = {"status": "signed", "asset": str(output_path)}  # placeholder
    print(json.dumps(report))
    return report

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("asset"); p.add_argument("manifest")
    p.add_argument("output"); p.add_argument("signer")
    p.add_argument("--trust", default=None)
    a = p.parse_args()
    try:
        attach_and_verify(Path(a.asset), Path(a.manifest),
                          Path(a.output), Path(a.signer), a.trust)
    except C2PAStageError as e:
        print(json.dumps({"error": e.code, "detail": str(e)}), file=sys.stderr)
        sys.exit(1)