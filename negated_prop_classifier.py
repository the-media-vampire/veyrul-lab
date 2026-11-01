from collections import Counter

def classify_negated_prop(verdicts: list[str]) -> dict:
    """
    Classify negated-prop compliance from a list of per-still inspection verdicts.

    verdicts: list of strings, each 'present' | 'absent' | 'ambiguous'
      - 'present'   : the negated prop was visible in this still
      - 'absent'    : the negated prop was not seen in this still
      - 'ambiguous' : could not determine from this still

    Returns:
      classification: 'always_present' | 'sometimes_present' | 'never_present'
                      | 'ambiguous_only' | 'no_data'
      present, absent, ambiguous, total: int counts
      falsified: bool or None — True if any still shows prop present
      coverage_pct: float — percentage of stills with a determinate verdict

    Source: art_01M6A5NN0JFR92YNZ3YG1V3B85 r1 (HF-PKG-014 negated-prop finding).
    Execution receipt: 53b2d852-968f-4e10-8306-6557a275a452, exit 0.
    """
    counts = Counter(verdicts)
    total = len(verdicts)
    present = counts.get('present', 0)
    absent = counts.get('absent', 0)
    ambiguous = counts.get('ambiguous', 0)

    if total == 0:
        return {"classification": "no_data", "falsified": None,
                "present": 0, "absent": 0, "ambiguous": 0,
                "total": 0, "coverage_pct": 0.0}

    if present == total:
        classification = "always_present"
    elif present == 0 and absent > 0:
        classification = "never_present"
    elif present > 0 and absent > 0:
        classification = "sometimes_present"
    else:
        classification = "ambiguous_only"

    falsified = present > 0
    coverage_pct = round(100 * (present + absent) / total, 1)

    return {
        "classification": classification,
        "present": present,
        "absent": absent,
        "ambiguous": ambiguous,
        "total": total,
        "falsified": falsified,
        "coverage_pct": coverage_pct,
    }


if __name__ == "__main__":
    examples = [
        ("HF-PKG-014 baseline (all stills show lid)", ['present'] * 5),
        ("Partial (3 of 5 show lid)",                ['present', 'present', 'present', 'absent', 'absent']),
        ("Negation respected (0 of 5 show lid)",     ['absent'] * 5),
        ("All ambiguous",                            ['ambiguous'] * 5),
    ]
    print(f"{'Case':<40} {'Classification':<22} {'Falsified':<10} {'Coverage%'}")
    for label, v in examples:
        r = classify_negated_prop(v)
        print(f"{label:<40} {r['classification']:<22} {str(r['falsified']):<10} {r['coverage_pct']}")