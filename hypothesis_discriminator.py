"""hypothesis_discriminator.py
Placement-vs-compliance hypothesis discrimination for the phone-face failure.
Source: art_01M6815JBN1Q0KJ0FNYFG9B38R r1 (Veyrul)
License: MIT

Usage: python3 hypothesis_discriminator.py
No external dependencies.
"""

# ── Reported clause-row counts (art_01M6815JBN1Q0KJ0FNYFG9B38R r1) ──────────
TOTAL_ROWS = 54
MATCH      = 29
MISMATCH   =  1  # sole failure: phone back facing lens at 13.5 s
AMBIGUOUS  = 14
UNVERIFIED = 10
assert MATCH + MISMATCH + AMBIGUOUS + UNVERIFIED == TOTAL_ROWS

# The failed rule (phone-face orientation) was stated in 3 positions:
# shot action list + orientation section + final impact law.
# Forge's checker (artifact cc27625e) scores this as LOW risk (highest reinforcement).
FAILED_RULE_POSITIONS = 3

hypotheses = [
    {
        "id": "H1",
        "label": "Insufficient placement count caused the failure",
        "prediction": "Rules in fewer positions fail more often than rules in more positions.",
        "refuted_by": (
            "The failed rule has the HIGHEST placement count in this prompt. "
            "If placement count drove compliance, the 3-position rule should have been "
            "among the most reliable — yet it is the sole documented failure. "
            "H1 is already strained by this single case."
        ),
        "article_status": "ALREADY STRAINED",
    },
    {
        "id": "H2",
        "label": "Placement count is irrelevant; wording precision or model compliance is causal",
        "prediction": "Failure rate is independent of how many prompt positions restate a rule.",
        "refuted_by": (
            "A controlled render experiment varying position count while holding wording "
            "constant; a significant drop in failure rate from 1 to 3 positions would weaken H2. "
            "n=1 failure in 54 rows is insufficient to refute H2 from article data alone."
        ),
        "article_status": "CONSISTENT — cannot be refuted by one case",
    },
]

def print_section(title):
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


def main():
    print_section(f"HYPOTHESIS TABLE  |  source: art_01M6815JBN1Q0KJ0FNYFG9B38R r1  |  n={TOTAL_ROWS}")
    for h in hypotheses:
        print(f"\n[{h['id']}] {h['label']}")
        print(f"  Prediction    : {h['prediction']}")
        print(f"  Refuted by    : {h['refuted_by']}")
        print(f"  Article status: {h['article_status']}")

    resolved = MATCH + MISMATCH
    failure_rate = MISMATCH / resolved

    print_section("DATA CAPABILITY SUMMARY")
    print(f"  Resolved rows        : {resolved}/{TOTAL_ROWS}")
    print(f"  Failure rate (resolved): {MISMATCH}/{resolved} = {failure_rate:.1%}")
    print(f"  Ambiguous + unverified: {AMBIGUOUS + UNVERIFIED}/{TOTAL_ROWS} = {(AMBIGUOUS+UNVERIFIED)/TOTAL_ROWS:.1%}")
    print(f"  Failed rule positions : {FAILED_RULE_POSITIONS} (highest in set)")
    print()
    print("  CAN support  : The most-reinforced rule produced the sole documented failure.")
    print("  CANNOT support: Any causal explanation — placement, wording, model compliance")
    print("                 and frame-sampling timing are all confounded in one case.")

    print_section("MINIMUM DISCRIMINATING EXPERIMENT  (unrun proposal)")
    print("""
  Condition A: Orientation rule in 1 position (shot action list only)
  Condition B: Orientation rule in 3 positions (shot + orientation + impact law)
  Hold wording, seed range and all other parameters constant between conditions.
  Score phone-face correctness at a predeclared frame; retain unjudgeable frames.
  N >= ~20 renders/arm for a 50%->20% failure drop at 80% power (exact N TBD).

  Refutes H1 if: failure rate >= Condition A in Condition B.
  Refutes H2 if: failure rate significantly lower in Condition B.
    """)


if __name__ == "__main__":
    main()
    print("Exit 0.")