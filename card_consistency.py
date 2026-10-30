"""card_consistency.py
Internal consistency checks for model-card stated figures.
Source: art_01M66YP3XWTDRSW8X0YA8R8AQV r1 (all figures are card statements).
MIT — Vera / Veyrul lab.

Checks:
  1. FLUX 3: bf16 bytes-per-param vs stated file size
  2. Distilled-vs-undistilled models: step count matches distillation label
  3. Distilled FLUX variants: guidance=1.0 as expected by the card convention
  4. Qwen: simultaneous true-CFG and guidance axes flagged (not a failure, a note)

What would disprove a PASS here:
  - A ratio outside [0.9, 1.3] for the file-size check (suggesting param count or dtype is wrong)
  - A distilled model claiming >20 steps without explanation
  - A distilled FLUX variant claiming guidance != 1.0 without a stated reason
"""

RESULTS = []

# ── 1. FLUX 3 file size vs bf16 arithmetic ───────────────────────────────────
params_B = 5.6e9
bytes_per_param_bf16 = 2
expected_gb = params_B * bytes_per_param_bf16 / 1e9
card_file_gb = 11.1
ratio = card_file_gb / expected_gb

RESULTS.append({
    "check": "FLUX3 bf16 file size vs param count",
    "expected_naive_gb": round(expected_gb, 2),
    "card_states_gb": card_file_gb,
    "ratio": round(ratio, 3),
    "consistent": 0.9 <= ratio <= 1.3,
})

# ── 2 & 3. Step/distillation coherence and guidance checks ──────────────────
MODELS = [
    {"name": "Qwen-Image-Edit-2511",          "distilled": False, "steps": 40, "guidance": 4.0,  "true_cfg": True},
    {"name": "FLUX.2 klein 4B",               "distilled": True,  "steps": 4,  "guidance": 1.0,  "true_cfg": False},
    {"name": "FLUX.2 klein 9B",               "distilled": True,  "steps": 4,  "guidance": 1.0,  "true_cfg": False},
    {"name": "FLUX.2 klein 9B-KV",            "distilled": True,  "steps": 4,  "guidance": 1.0,  "true_cfg": False},
    {"name": "FLUX3 Klein Base (undistilled)", "distilled": False, "steps": 50, "guidance": 3.5,  "true_cfg": False},
    {"name": "FLUX3 Klein distilled",          "distilled": True,  "steps": 16, "guidance": None, "true_cfg": False},
]

DISTILLED_STEP_THRESHOLD = 20

for m in MODELS:
    step_ok = (m["distilled"] == (m["steps"] <= DISTILLED_STEP_THRESHOLD))
    RESULTS.append({"check": f"distill/step — {m['name']}", "coherent": step_ok,
                    "distilled": m["distilled"], "steps": m["steps"]})
    if m["distilled"] and m["guidance"] is not None:
        RESULTS.append({"check": f"guidance=1.0 — {m['name']}",
                        "expected_1_0": m["guidance"] == 1.0,
                        "guidance": m["guidance"]})

# ── 4. Flag Qwen dual-axis conditioning ──────────────────────────────────────
qwen = MODELS[0]
RESULTS.append({"check": "Qwen true-CFG + guidance axes",
                "flag": "Two separate conditioning axes stated; not an error but verify architecture",
                "true_cfg": qwen["true_cfg"], "cfg_scale": qwen["guidance"]})


def run_checks():
    passed = failed = flagged = 0
    for r in RESULTS:
        verdict = r.get("consistent", r.get("coherent", r.get("expected_1_0", None)))
        if verdict is True:
            tag = "PASS"; passed += 1
        elif verdict is False:
            tag = "FAIL"; failed += 1
        else:
            tag = "FLAG"; flagged += 1
        print(f"[{tag}] {r['check']}")
    print(f"\nSummary: {passed} PASS | {failed} FAIL | {flagged} FLAG")
    return failed == 0


if __name__ == "__main__":
    ok = run_checks()
    raise SystemExit(0 if ok else 1)