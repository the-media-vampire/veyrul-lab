"""Aggregate clause labels without discarding unresolved evidence."""
import json


def audit_counts(match, mismatch, ambiguous, unverified):
    counts = (match, mismatch, ambiguous, unverified)
    if any(type(x) is not int or x < 0 for x in counts):
        raise ValueError('counts must be nonnegative integers')
    total = sum(counts)
    resolved = match + mismatch
    unknown = ambiguous + unverified
    return {
        'total': total,
        'resolved': resolved,
        'unresolved': unknown,
        'match_fraction_all_rows': match / total if total else None,
        'match_fraction_resolved_only': match / resolved if resolved else None,
        'unresolved_fraction': unknown / total if total else None,
        'possible_final_match_fraction': [match / total, (match + unknown) / total] if total else None,
        'interval_type': 'logical bounds, not a confidence interval'
    }


if __name__ == '__main__':
    print(json.dumps(audit_counts(29, 1, 14, 10), indent=2))