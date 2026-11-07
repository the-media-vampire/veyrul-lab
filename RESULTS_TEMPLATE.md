# Results — Learning-Path Experiment

Fill in after running compile_check.sh on each attempt.

| Function | Condition C errors | Condition H errors | Winner |
|---|---|---|---|
| DrawTextureRec | | | |
| DrawTextPro | | | |
| GenTextureCellular | | | |

## Observations (technical only)
- List exact compiler error messages here, not paraphrases.
- Note if a function is absent from the cheatsheet entirely.

## Taste judgments (keep separate)
- Readability of cheatsheet vs. header as a learning resource.
- Subjective ease of locating the function.

## Relation to Scout's flip experiment (4211cb11)
Scout tests pixel-level equivalence of two rendering API calls.
This experiment tests discovery-path correctness before the call is written.
The two are complementary: Scout's diff_check.py is the downstream judge;
this compile_check.sh is the upstream judge.