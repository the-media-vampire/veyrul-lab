"""nvfp4_size_estimator.py

Estimates the expected file size of an NVFP4 group-16 quantized safetensors
checkpoint from the known bf16 original size.

Calibration source
------------------
BennyDaBall/PiD-1.5-flux2-nvfp4-comfy at commit 536ef872c371
  bf16 original : 2.61 GB  (card-stated)
  NVFP4 file    : 1,091,499,246 bytes  (tree listing)
  Reduction     : 58.2%
  Implied bf16_fraction (quality-critical layers kept full-precision): 0.154

Source record: art_01M6EA07T9KRDAS7559V91MCA7 revision 1
Execution receipt: f6b9a678-0cf9-482a-bdb1-dac4200b796f (exit 0)
"""

_BYTES_PER_PARAM_BF16    = 2.0
_BYTES_PER_PARAM_FP4G16  = 0.5 + (2.0 / 16)  # 4-bit data + group-16 bf16 scale

# Fraction of parameters kept in bf16 (quality-critical layers).
# Calibrated from PiD 1.5 FLUX.2 NVFP4 observed sizes.
PID_CALIBRATED_BF16_FRACTION = 0.154


def estimate_nvfp4_size(
    bf16_bytes: float,
    bf16_fraction: float = PID_CALIBRATED_BF16_FRACTION,
) -> dict:
    """Estimate NVFP4-group16 checkpoint size from the bf16 original.

    Parameters
    ----------
    bf16_bytes    : Total bf16 safetensors file size in bytes.
    bf16_fraction : Fraction of parameters kept in bf16 (0.0–1.0).
                    Default is PID_CALIBRATED_BF16_FRACTION (0.154).

    Returns
    -------
    dict with keys:
        bf16_bytes              – input
        estimated_nvfp4_bytes   – integer estimate
        estimated_nvfp4_gb      – rounded to 3 d.p.
        blended_ratio           – NVFP4 / bf16 size ratio
        saving_pct              – percentage file-size reduction
    """
    if not 0.0 <= bf16_fraction <= 1.0:
        raise ValueError("bf16_fraction must be in [0, 1]")

    quant_fraction = 1.0 - bf16_fraction
    blended_ratio = (
        bf16_fraction * 1.0  # bf16 layers stay at 1× cost
        + quant_fraction * (_BYTES_PER_PARAM_FP4G16 / _BYTES_PER_PARAM_BF16)
    )
    est_bytes = bf16_bytes * blended_ratio
    return {
        "bf16_bytes": bf16_bytes,
        "estimated_nvfp4_bytes": round(est_bytes),
        "estimated_nvfp4_gb": round(est_bytes / 1e9, 3),
        "blended_ratio": round(blended_ratio, 4),
        "saving_pct": round((1.0 - blended_ratio) * 100, 1),
    }


if __name__ == "__main__":
    import sys

    bf16_gb = float(sys.argv[1]) if len(sys.argv) > 1 else 2.61
    result = estimate_nvfp4_size(bf16_gb * 1e9)
    print(f"bf16 input     : {bf16_gb:.3f} GB")
    print(f"NVFP4 estimate : {result['estimated_nvfp4_gb']:.3f} GB")
    print(f"Reduction      : {result['saving_pct']}%")