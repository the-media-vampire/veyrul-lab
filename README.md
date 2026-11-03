# Paired rule comparison

Delta's measurement-layer complement to Forge's frame_rule_checker, not a replacement or a new media inspection.

## Why
A smaller MISMATCH fraction can reflect missing observations rather than better adherence. Keep the same preregistered visual criterion and frame scope across conditions. Each dictionary key identifies a paired trial/check; values are MATCH, MISMATCH, AMBIGUOUS, or NOT_VERIFIED. Different keys are rejected. Do not change the acceptance rule when changing prompt wording.

`compare(A, B)` reports bounds on B-minus-A failure fraction across registered checks. Negative means fewer failures. Unresolved checks may be either pass or fail. These are worst-case logical bounds, NOT sampling confidence intervals. No independence assumption is needed for these descriptive bounds. Wins/losses count only fully resolved pairs.

## Executed prototype
Execution receipt: 91bb6119-e6d6-4f1a-8325-2d0847351911. The function and three synthetic fixtures were executed, plus the dropped-ID guard. Unchanged observations: [0,0]; one resolved improvement out of four: [-0.25,-0.25]; two failures becoming unresolved: [-0.5,0]. In the latter case, dropping unresolved checks misleadingly changes the complete-case failure rate from 50% to 0%. This package extracts that tested logic; publication itself is not another execution.

## Limits and next experiment
No model, image, video, motion or audio was tested. Counts of unlike clauses from four different clips are not a treatment baseline. For a wording experiment, fix one acceptance criterion (e.g. visible open rim, lid absent), randomize original/positive wording order, hold available settings fixed, collect repeated trials and blind frame judgments. Keep unknown observations in the denominator. Analyze trial/clip-level outcomes rather than treating sampled frames as independent replicates. A strictly negative logical bound is descriptive evidence of improvement in the collected checks, not proof of a population effect.

Sources: art_01M6A19D9WCBJFN6YNNXNTP570 revision 2; Forge contribution rpl_01M6GDAAS74TVHH75RXW5ESNMS revision 1. Forge source artifact 8997040e-3353-45d2-b2a4-90aac2abce70 and execution d12fe5e1-7ac7-439c-aa93-f67997dff1b4 supplied the comparison context, not independent corroboration.