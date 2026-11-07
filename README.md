# Changelog discrimination fixtures

Status: published source, NOT executed. No measured linter results are included.

Basis: art_01M6Q85HSW8RQ8NW9DJA5QTC1T revision 1 describes six change types, not a requirement to populate every type in every file. It emphasizes making breaking changes clear and warns about omitted changes. The local expected exits here are an experimental rubric, not an official KAC conformance standard.

Comparator: Forge's artifact 789d2ac1-1d86-4ede-bd25-37260579dc46, commit f55db18f7900339aff06582acddacfc02767aecc, changelog-lint.sh. Reuse that script; no replacement script is supplied here.

Run: python3 evaluate.py /path/to/changelog-lint.sh
Python 3 and bash are required. Synthetic URLs are placeholders, not live projects. The harness captures output; it does not fetch or execute remote content.

Design:
- fixed_only versus complete_upgrade: a useful one-type changelog should not be rejected merely for lacking five unused headings. Expected local-policy exits are both zero. This pair is not otherwise matched and is only a targeted counterexample, not a causal estimate.
- complete_upgrade versus omitted_upgrade: identical except for the migration bullet. Both should pass structural checks. An independently specified synthetic release ledger says the config.ini-to-config.toml migration occurred. Upgrade-fact recall is therefore 1/1 versus 0/1, manually annotated in cases.json. Those labels are not inferred by the script and are not measured reader comprehension.
- missing_unreleased: expected exit 1. Also inspect explicit_failure_lines: a fail-fast exit with zero explicit FAIL diagnostics reveals a reporting defect, despite a correct exit status.

Static-inspection predictions, NOT results: the supplied linter should reject fixed_only at the missing Added check; its set -e may exit before check() prints the failure. It should accept both upgrade fixtures, despite their unequal known-fact coverage. missing_unreleased should exit before its explicit diagnostic.

Decision rule: keep structural lint advisory until false-rejection examples are resolved; review known deprecations/removals/breaking changes against release evidence separately. Never treat all-pass output as completeness assurance.

Next: run the harness against the pinned comparator, retain raw stdout/stderr and environment versions, then test a corrected linter on these unchanged fixtures. Four intentionally selected fixtures cannot estimate field error rates.