"""Concrete comparison: same editing task, two routes.

Shows how the tier-gate contract surfaces different risk
postures for the same downstream publication decision.
"""
from gemini_tier_contract import (
    GeminiOutputProvenance, GeminiTier,
    OpenWeightOutputProvenance
)

# --- Route A: Gemini API, unpaid tier ---
route_a = GeminiOutputProvenance(
    tier=GeminiTier.UNPAID,
    prompt_contains_sensitive_data=False,
    intended_use_commercial=True,
)
print("=== Route A: Gemini unpaid, commercial intent ===")
for k, v in route_a.summary().items():
    print(f"  {k}: {v}")

# --- Route B: Gemini API, paid tier ---
route_b = GeminiOutputProvenance(
    tier=GeminiTier.PAID,
    prompt_contains_sensitive_data=True,
    intended_use_commercial=False,
)
print("\n=== Route B: Gemini paid, sensitive data, non-commercial ===")
for k, v in route_b.summary().items():
    print(f"  {k}: {v}")

# --- Route C: Qwen-Image-Edit-2511, Apache-2.0 ---
route_c = OpenWeightOutputProvenance(
    model_id="Qwen/Qwen2.5-VL-Image-Edit-2511",
    weight_license="Apache-2.0",
    output_commercial_allowed=True,  # Apache-2.0 does not restrict outputs
    source_record="art_01M5Z9WPX7FY4WPTTW9T1VXS34",
)
print("\n=== Route C: Qwen-Image-Edit-2511, Apache-2.0 ===")
for k, v in route_c.summary().items():
    print(f"  {k}: {v}")

# --- Route D: FLUX.2 klein 9B, non-commercial weights ---
route_d = OpenWeightOutputProvenance(
    model_id="black-forest-labs/FLUX.2-klein-9B",
    weight_license="FLUX Non-Commercial License",
    output_commercial_allowed=None,  # not established in art_01M5ZAFS2Z0A54WCZ18WQM4H57
    source_record="art_01M5ZAFS2Z0A54WCZ18WQM4H57",
)
print("\n=== Route D: FLUX.2-klein-9B, non-commercial weights ===")
for k, v in route_d.summary().items():
    print(f"  {k}: {v}")

print("\n--- Publish gate summary ---")
for label, route in [("A",route_a),("B",route_b),("C",route_c),("D",route_d)]:
    print(f"  Route {label} publish_blocked={route.is_publish_blocked()}")