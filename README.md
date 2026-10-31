# Clause audit

Run `python clause_audit.py` (standard library only).

Input example: reported aggregate labels in art_01M6815JBN1Q0KJ0FNYFG9B38R revision 1: 29 MATCH, 1 MISMATCH, 14 AMBIGUOUS, 10 not verified. No third-party media or prompt reproduced.

The same audit_counts function was executed in lab receipt e3a50bd2-ec0f-45d5-aa04-fd7bf0715bab (exit 0), with seven checks covering empty input, all-unresolved input, fully resolved input, three invalid input cases, and source totals. Publication is not another execution.

Resolved-only match fraction is 29/30 = 96.7%; all-row confirmed match fraction is 29/54 = 53.7%; unresolved fraction is 24/54 = 44.4%. These have different denominators and meanings. Logical final-match bounds are 29/54 through 53/54, conditional on the current resolved labels remaining fixed and every unresolved row eventually being classified. They are not statistical confidence limits or video-quality scores.

Rows are not independent trials and are not equally important to the story. No model comparison, media inspection, causal effect of prompt placement, or generation success rate is measured.

Important source correction: revision 1 says the failed orientation rule was already stated in the shot, orientation section, and final impact law. Therefore a three-position presence score cannot justify calling that clip low risk, and adding a shot mention is not an established remedy.

Next proposed measurement: blind-label visible phone face at predeclared moments in repeated renders, compare identical prompts differing only in rule placement, and report unjudgeable cases separately. No such render experiment was run here.